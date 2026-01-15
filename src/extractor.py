import base64
import fitz
import json
import os
from typing import List, Set
from src.llm.llm_client import InvoiceExtractorLLM
from database.database import SessionLocal, engine, Base
from src.services.invoice_service import InvoiceService
from src.services.s3_service import S3Service

class Extractor:

    def __init__(self, history_file: str = "processed_history.json"):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        
        # Sobe um nível para sair da src
        project_root = os.path.dirname(current_dir)
        
        self.project_root = project_root
        self.history_file = os.path.join(project_root, history_file)
        self.processed_files = self._load_history()
        
        # Inicializa Cliente LLM
        self.llm_client = InvoiceExtractorLLM()
        
        # Inicializa Storage (S3)
        self.s3_service = S3Service()
        
        # Inicializa Banco de Dados
        try:
            Base.metadata.create_all(bind=engine)
        except Exception as e:
            print("O pipeline continuará rodando, mas sem salvar no banco.")
            self.db_session = None
            self.invoice_service = None
            return

        # Abre sessão
        self.db_session = SessionLocal()
        self.invoice_service = InvoiceService(self.db_session)

    def _load_history(self) -> Set[str]:
        if os.path.exists(self.history_file):
            try:
                with open(self.history_file, "r") as f:
                    return set(json.load(f))
            except json.JSONDecodeError:
                return set()
        return set()

    def _save_to_history(self, filename: str):
        self.processed_files.add(filename)
        with open(self.history_file, "w") as f:
            json.dump(list(self.processed_files), f, indent=2)

    def extract_images(self, pdf_path: str) -> List[str]:
        """
        Extrai imagens do PDF e retorna uma lista de strings base64.
        """
        try:
            doc = fitz.open(pdf_path)
            base64_images = []
            
            for page_num in range(len(doc)):
                page = doc.load_page(page_num)
                matrix = fitz.Matrix(2, 2)
                pix = page.get_pixmap(matrix=matrix)
                img_bytes = pix.tobytes("png")
                base64_str = base64.b64encode(img_bytes).decode('utf-8')
                base64_images.append(base64_str)
                
            return base64_images
        except Exception as e:
            print(f"Erro ao converter PDF em imagens")
            raise e

    def process_folder(self, folder_name: str = "data"):
        """
        Processa arquivos PDF na pasta especificada.
        """
        folder_path = os.path.join(self.project_root, folder_name)
        
        if not os.path.exists(folder_path):
            return

        supported_ext = ('.pdf', '.jpg', '.jpeg', '.png')
        all_files = [f for f in os.listdir(folder_path) if f.lower().endswith(supported_ext)]
        new_files = [f for f in all_files if f not in self.processed_files]
        
        if not new_files:
            print("Nenhum arquivo novo.")
            return

        print(f"Encontrados {len(new_files)} novos arquivos.")
        print("Processando arquivos encontrados...")

        # Output 
        output_dir = os.path.join(self.project_root, "output")
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        for filename in new_files:
            full_path = os.path.join(folder_path, filename)
            try:
                # 1. Extrai imagens
                images = self.extract_images(full_path)
                
                # 2. Envia para IA
                invoice_obj = self.llm_client.extract(images)
                
                # 3. Salva JSON no S3
                output_filename = f"{os.path.splitext(filename)[0]}.json"
                self.s3_service.upload_json(invoice_obj.model_dump(), output_filename)
                
                # 4. Salva no Banco via Service (se disponível)
                if self.invoice_service:
                    self.invoice_service.save_invoice(invoice_obj)
                    print(f"Nota {filename} salva no banco.")
                
                # 5. Marca como concluído
                self._save_to_history(filename)
                
            except Exception as e:
                print(f"Falha ao processar {filename}: {str(e)}")
