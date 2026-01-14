from typing import List
from langchain_core.messages import HumanMessage
from langchain_openai import ChatOpenAI
from schemas.schemas import Invoice
from dotenv import load_dotenv

# Carrega variáveis de ambiente
load_dotenv(override=True)

class InvoiceExtractorLLM:
    def __init__(self):
        """
        Inicializa o cliente OpenAI.
        """
        self.llm = ChatOpenAI(model="gpt-4o", temperature=0)
        self.structured_llm = self.llm.with_structured_output(Invoice)

    def extract(self, images_base64: List[str]) -> Invoice:
        """
        Extrai dados da Nota Fiscal a partir de imagens.
        """
        content_payload = [
            {
                "type": "text",
                "text": "Analise esta Nota Fiscal e extraia os dados. Se houver várias páginas, consolide as informações."
            }
        ]
        
        for img_b64 in images_base64:
            content_payload.append({
                "type": "image_url",
                "image_url": {
                    "url": f"data:image/png;base64,{img_b64}"
                }
            })

        msg = HumanMessage(content=content_payload)
        
        try:
            result = self.structured_llm.invoke([msg])
            return result
        except Exception as e:
            raise e
