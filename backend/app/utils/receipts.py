from app.schemas import ReceiptJSON, TxOut, ClientOut
from app.models import Transaction, Client

def build_receipt_json(tx: Transaction) -> dict:
    tx_out = TxOut.model_validate(tx)
    client_out = ClientOut.model_validate(tx.client)
    receipt = ReceiptJSON(transaction=tx_out, client=client_out)
    return receipt.model_dump()
