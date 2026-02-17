# xrpl-tax-csv
Open-source tool to export XRPL transactions to a tax-ready CSV file
# XRPL Tax CSV Exporter

Simple open-source tool that turns any XRPL address into a clean tax-ready CSV file.

## Features
- Fetches full mainnet transaction history
- Accurate ledger close dates
- Fees in XRP
- Received amounts + historical USD cost basis (via CoinGecko)
- Basic classification (acquisition vs non-taxable)
- Taxable? (Yes/No) column
- Sorted newest first
- Summary row with totals

## How to run
1. Install Python 3 + xrpl-py: `pip install xrpl-py`
2. Run: `python xrpl_tax_exporter.py`
3. CSV output in `reports/` folder

## Sample output
See `sample_output.csv` for a real mainnet example (my address, 16 transactions).

## Feedback
This is an early prototype. What features are missing for your tax filing? Would you pay a small amount for a polished version? Let me know in issues or on Reddit/Discord.

MIT License – contributions welcome!
