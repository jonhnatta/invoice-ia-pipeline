from typing import List, Optional
from datetime import date
from pydantic import BaseModel, Field, field_validator

class InvoiceItem(BaseModel):
    # Item da Nota Fiscal
    cod_product: Optional[str] = Field(None, description="Código do produto")
    description: str = Field(..., description="Descrição do produto ou serviço")
    quantity: float = Field(..., description="Quantidade do item")
    unit_price: float = Field(..., description="Preço do item")
    total_price: float = Field(..., description="Preço total (quantidade * preço unitário)")

class Invoice(BaseModel):
    # Dados da Nota Fiscal
    invoice_number: Optional[str] = Field(None, description="O identificador da nota fiscal")
    series: Optional[str] = Field(None, description="Série da nota fiscal")
    issue_date: Optional[date] = Field(None, description="Data de emissão da nota")
    
    # Emissor/destinatário
    issuer_name: str = Field(..., description="Nome da empresa/pessoa que emitiu a nota")
    issuer_tax_id: Optional[str] = Field(None, description="CNPJ ou CPF do emissor")
    recipient_name: Optional[str] = Field(None, description="Nome do destinatário")
    recipient_tax_id: Optional[str] = Field(None, description="CNPJ ou CPF do destinatário")
    
    # Valor da Nota Fiscal
    total_amount: float = Field(..., description="Valor total final da nota")
    tax_amount: Optional[float] = Field(0.0, description="Valor total dos impostos")
    
    # Itens da Nota Fiscal
    items: List[InvoiceItem] = Field(default_factory=list, description="Lista de todos os itens/serviços da nota")
