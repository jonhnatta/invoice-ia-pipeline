import os
import sys
from src.extractor import Extractor

def main():
    print("Iniciando Pipeline de ETL de Notas Fiscais...")

    if not os.path.exists("data"):
        print("Não encontrei a pasta 'data'. Coloque seus PDFs lá e rode novamente.")
        return

    extractor = Extractor()
    extractor.process_folder("data")
    
    print("Pipeline finalizado.")

if __name__ == "__main__":
    main()
