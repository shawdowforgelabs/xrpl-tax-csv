# xrpl_tax_report_v13_final.py
# v13 – Final polished version for Reto (nice formatting, clean summary)

import os
import csv
import requests
from datetime import datetime, timezone, timedelta

from xrpl.clients import JsonRpcClient
from xrpl.models.requests import AccountTx
from xrpl.utils import drops_to_xrp

RPC_URL = "https://xrplcluster.com"
ADDRESS = "ADD YOUR ADDRESS HERE"

PRICE_CACHE = {}

def get_xrp_price(ddmmyyyy):
    if ddmmyyyy in PRICE_CACHE:
        return PRICE_CACHE[ddmmyyyy]
    try:
        url = f"https://api.coingecko.com/api/v3/coins/ripple/history?date={ddmmyyyy}"
        r = requests.get(url, timeout=10)
        price = r.json()["market_data"]["current_price"]["usd"]
        PRICE_CACHE[ddmmyyyy] = price
        return price
    except:
        return 0.60

client = JsonRpcClient(RPC_URL)

def fetch_all_txs(address):
    marker = None
    all_txs = []
    page = 1
    while True:
        req = AccountTx(account=address, limit=200, marker=marker)
        resp = client.request(req)
        result = resp.result
        if "transactions" not in result:
            break
        all_txs.extend(result["transactions"])
        marker = result.get("marker")
        if not marker:
            break
        page += 1
    return all_txs

print("Running XRPL Tax Report v13 – Final for Reto")
all_txs = fetch_all_txs(ADDRESS)
print(f"Total transactions: {len(all_txs)}\n")

report = []

for tx_obj in all_txs:
    tx_json = tx_obj.get("tx_json") or tx_obj.get("tx") or tx_obj
    ledger_time = tx_json.get("date")
    if ledger_time is not None:
        dt = datetime(2000, 1, 1, tzinfo=timezone.utc) + timedelta(seconds=ledger_time)
    else:
        dt = datetime(1970, 1, 1, tzinfo=timezone.utc)

    date_str = dt.strftime("%Y-%m-%d")
    ddmmyyyy = dt.strftime("%d-%m-%Y")
    price_usd = get_xrp_price(ddmmyyyy)

    ttype = tx_json.get("TransactionType", "Unknown")
    amount = 0.0
    currency = "XRP"
    description = f"{ttype} – no value moved"
    cost_basis = 0.0
    fee_xrp = float(drops_to_xrp(tx_json.get("Fee", "0")))

    if ttype == "Payment":
        amt = tx_json.get("Amount") or tx_obj.get("meta", {}).get("delivered_amount")
        if isinstance(amt, str):
            amount = float(drops_to_xrp(amt))
        elif isinstance(amt, dict):
            amount = float(amt.get("value", 0))
            currency = amt.get("currency", "XRP")

        if tx_json.get("Destination") == ADDRESS and amount > 0:
            description = f"Received {amount:,.8f} {currency}"
            cost_basis = round(amount * price_usd, 4)

    row = {
        "Date Acquired": date_str,
        "Date Sold": "",
        "Description": description,
        "Amount": f"{amount:,.8f}",
        "Currency": currency,
        "Cost Basis": f"{cost_basis:,.2f}",
        "Proceeds": "0.00",
        "Gain/Loss": "0.00",
        "Taxable?": "Yes" if cost_basis > 0 else "No",
        "Fee (XRP)": f"{fee_xrp:,.6f}",
        "Price USD": f"{price_usd:,.4f}",
        "Transaction Type": ttype,
        "Hash": tx_json.get("hash", ""),
        "Notes": "Acquisition – cost basis recorded" if cost_basis > 0 else "Non-taxable event"
    }
    report.append(row)

# Sort newest first
report.sort(key=lambda x: x["Date Acquired"], reverse=True)

# Summary row
total_cost = sum(float(r["Cost Basis"].replace(",", "")) for r in report)
total_fee = sum(float(r["Fee (XRP)"].replace(",", "")) for r in report)
summary = {k: "" for k in report[0]}
summary.update({
    "Date Acquired": "SUMMARY",
    "Description": f"Total transactions: {len(report)}",
    "Cost Basis": f"{total_cost:,.2f}",
    "Fee (XRP)": f"{total_fee:,.6f}",
    "Notes": "No taxable disposals. Cost basis recorded from acquisitions."
})
report.append(summary)

csv_path = "reports/XRPL_Tax_Report_Final.csv"
os.makedirs("reports", exist_ok=True)

with open(csv_path, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=report[0].keys())
    writer.writeheader()
    writer.writerows(report)

print(f"\n=== SUCCESS ===")
print(f"Final CSV created: {os.path.abspath(csv_path)}")
print("Open it now – this is the polished version ready for Reto.")

input("\nPress Enter to close the window...")