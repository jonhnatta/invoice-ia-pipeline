import pytest
from schemas.schemas import Invoice, InvoiceItem

def test_invoice_validation_success():
    """Testa se uma nota fiscal é instanciada corretamente"""
    item = InvoiceItem(
        description="item 1",
        quantity=10,
        unit_price=100.0,
        total_price=1000.0
    )
    
    invoice = Invoice(
        issuer_name="Empresa 1",
        total_amount=1000.0,
        items=[item]
    )
    
    assert invoice.issuer_name == "Empresa 1"
    assert invoice.total_amount == 1000.0
    assert len(invoice.items) == 1
    assert invoice.items[0].description == "item 1"

def test_invoice_validation_failure_missing_field():
    """Testa se lança erro quando falta campo obrigatório"""
    with pytest.raises(Exception):
        Invoice(
            total_amount=500.0
        )