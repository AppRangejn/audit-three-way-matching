import random
import pandas as pd
import numpy as np

def generate_data(count=10000):
    np.random.seed(42)
    random.seed(42)

    order_ids = [f"PO_{i+1:06d}" for i in range(count)]
    vendor_ids = [f"VEND_{random.randint(100, 150):04d}" for _ in range(count)]
    item_ids = [f"ITEM_{random.randint(1, 80):03d}" for _ in range(count)]
    quantities = np.random.randint(5, 500, size=count)
    prices = np.round(np.random.uniform(10.0, 500.0, size=count), 2)

    orders = pd.DataFrame({
        'order_id': order_ids,
        'vendor_id': vendor_ids,
        'item_id': item_ids,
        'quantity': quantities,
        'price': prices,
        'total': np.round(quantities * prices, 2)
    })

    receipt_quantities = quantities.copy()
    shortage_index = np.random.choice(count, size=300, replace=False)
    receipt_quantities[shortage_index] = np.maximum(1, receipt_quantities[shortage_index] - np.random.randint(1, 10, size=300))

    receipts = pd.DataFrame({
        'receipt_id': [f"GR_{i+1:06d}" for i in range(count)],
        'order_id': order_ids,
        'quantity_received': receipt_quantities
    })

    invoice_prices = prices.copy()
    bump_index = np.random.choice(count, size=400, replace=False)
    invoice_prices[bump_index] = np.round(invoice_prices[bump_index] * np.random.uniform(1.10, 1.35, size=400), 2)

    invoices = pd.DataFrame({
        'invoice_id': [f"INV_{i+1:06d}" for i in range(count)],
        'order_id': order_ids,
        'vendor_id': vendor_ids,
        'quantity_billed': quantities.copy(),
        'price_billed': invoice_prices,
        'total': np.round(quantities * invoice_prices, 2)
    })

    fake_invoices = pd.DataFrame({
        'invoice_id': [f"INV_FAKE_{i+1:03d}" for i in range(15)],
        'order_id': [f"PO_FAKE_{i+1:03d}" for i in range(15)],
        'vendor_id': [f"VEND_FAKE_{i+1:02d}" for i in range(15)],
        'quantity_billed': np.random.randint(10, 100, size=15),
        'price_billed': np.round(np.random.uniform(50.0, 300.0, size=15), 2),
    })
    fake_invoices['total'] = np.round(fake_invoices['quantity_billed'] * fake_invoices['price_billed'], 2)
    invoices = pd.concat([invoices, fake_invoices], ignore_index=True)

    duplicates = invoices.iloc[:10].copy()
    duplicates['invoice_id'] = duplicates['invoice_id'] + "_DUP"
    invoices = pd.concat([invoices, duplicates], ignore_index=True)

    orders.to_csv('data/purchase_orders.csv', index=False)
    receipts.to_csv('data/goods_receipts.csv', index=False)
    invoices.to_csv('data/invoices.csv', index=False)

if __name__ == "__main__":
    generate_data()
