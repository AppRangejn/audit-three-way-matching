import pandas as pd

def match_documents():
    orders = pd.read_csv('data/purchase_orders.csv')
    receipts = pd.read_csv('data/goods_receipts.csv')
    invoices = pd.read_csv('data/invoices.csv')

    merged = invoices.merge(orders, on='order_id', how='left', suffixes=('_invoice', '_order'))

    merged = merged.merge(receipts, on='order_id', how='left')

    merged['price_diff'] = (merged['price_billed'] - merged['price']).round(2)
    merged['qty_diff'] = merged['quantity_billed'] - merged['quantity_received']

    def get_status(row):
        if pd.isna(row['price']):
            return 'FAKE_INVOICE'
        if row['price_diff'] > 0:
            return 'PRICE_OVERBILL'
        if row['qty_diff'] > 0:
            return 'QUANTITY_OVERBILL'
        return 'OK'

    merged['status'] = merged.apply(get_status, axis=1)

    duplicates = merged.duplicated(subset=['order_id', 'total_invoice'], keep=False)
    merged.loc[duplicates & (merged['status'] == 'OK'), 'status'] = 'DUPLICATE_INVOICE'

    merged['extra_cost'] = 0.0
    price_mask = merged['status'] == 'PRICE_OVERBILL'
    qty_mask = merged['status'] == 'QUANTITY_OVERBILL'
    fake_mask = merged['status'] == 'FAKE_INVOICE'
    dup_mask = merged['status'] == 'DUPLICATE_INVOICE'

    merged.loc[price_mask, 'extra_cost'] = (merged['price_diff'] * merged['quantity_billed']).round(2)
    merged.loc[qty_mask, 'extra_cost'] = (merged['qty_diff'] * merged['price']).round(2)
    merged.loc[fake_mask, 'extra_cost'] = merged['total_invoice']
    merged.loc[dup_mask, 'extra_cost'] = merged['total_invoice']

    return merged
