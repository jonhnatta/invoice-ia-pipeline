from sqlalchemy.orm import Session
from src.models.models import InvoiceModel, InvoiceItemModel
from schemas.schemas import Invoice

class InvoiceService:
    def __init__(self, db: Session):
        self.db = db

    def save_invoice(self, invoice_data: Invoice):
        try:
            # dados da nota
            new_invoice = InvoiceModel(
                invoice_number=invoice_data.invoice_number,
                series=invoice_data.series,
                issue_date=invoice_data.issue_date,
                issuer_name=invoice_data.issuer_name,
                issuer_tax_id=invoice_data.issuer_tax_id,
                recipient_name=invoice_data.recipient_name,
                recipient_tax_id=invoice_data.recipient_tax_id,
                total_amount=invoice_data.total_amount,
                tax_amount=invoice_data.tax_amount
            )
            
            # Itens da nota
            for item in invoice_data.items:
                new_item = InvoiceItemModel(
                    cod_product=item.cod_product,
                    description=item.description,
                    quantity=item.quantity,
                    unit_price=item.unit_price,
                    total_price=item.total_price
                )
                new_invoice.items.append(new_item)
            
            self.db.add(new_invoice)
            self.db.commit()
            return new_invoice
            
        except Exception as e:
            self.db.rollback()
            print(f"Erro ao salvar no banco: {e}")
            raise e
