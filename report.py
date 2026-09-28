import pandas as pd

def generate_report(data):
    exceptions = data[data['status'] != 'OK'].copy()
    exceptions = exceptions.sort_values(by='extra_cost', ascending=False)

    exceptions.to_csv('audit_exceptions_p2p.csv', index=False)

    total_invoices = len(data)
    total_exceptions = len(exceptions)
    total_overbill = exceptions['extra_cost'].sum()

    print("AUDIT REPORT")
    print(f"Total Invoices Analyzed: {total_invoices:,}")
    print(f"Exceptions Found:        {total_exceptions:,}")
    print(f"Blocked Overbill Amount: ${total_overbill:,.2f}")
    print("Breakdown by Issue:")

    breakdown = exceptions.groupby('status')['extra_cost'].agg(['count', 'sum'])
    for status, row in breakdown.iterrows():
        print(f"{status}: {int(row['count'])} items | ${row['sum']:,.2f}")

    print("File saved: audit_exceptions_p2p.csv")
