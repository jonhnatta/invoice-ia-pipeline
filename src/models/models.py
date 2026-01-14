from sqlalchemy import Column, Integer, String, Numeric, ForeignKey, Date
from sqlalchemy.orm import relationship
from database.database import Base

class InvoiceModel(Base):
    __tablename__ = 'invoices'
    
    id = Column(Integer, primary_key=True, index=True)
    invoice_number = Column(String, nullable=True)
    series = Column(String, nullable=True)
    issue_date = Column(Date, nullable=True)
    
    issuer_name = Column(String)
    issuer_tax_id = Column(String, nullable=True)
    recipient_name = Column(String, nullable=True)
    recipient_tax_id = Column(String, nullable=True)
    
    total_amount = Column(Numeric(10, 2))
    tax_amount = Column(Numeric(10, 2), nullable=True)
    
    # Relacionamento dos dados das notas com os itens da nota
    items = relationship("InvoiceItemModel", back_populates="invoice", cascade="all, delete-orphan")

class InvoiceItemModel(Base):
    __tablename__ = 'invoice_items'
    
    id = Column(Integer, primary_key=True, index=True)
    invoice_id = Column(Integer, ForeignKey('invoices.id'))
    
    cod_product = Column(String, nullable=True)
    description = Column(String)
    quantity = Column(Numeric(10, 3))
    unit_price = Column(Numeric(10, 2))
    total_price = Column(Numeric(10, 2))
    
    invoice = relationship("InvoiceModel", back_populates="items")
