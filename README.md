# xrpl-tax-csv
Open-source tool to export XRPL transactions to a tax-ready CSV file
# XRPL Tax CSV Exporter

Open-source tool to export XRPL transactions to a tax-ready CSV file.

## Features
- Fetches full mainnet transaction history from any XRPL address
- Accurate ledger close dates (Ripple epoch conversion)
- Transaction fees in XRP
- Received amounts + historical USD cost basis (CoinGecko API)
- Basic classification (acquisition vs non-taxable events)
- Taxable? (Yes/No) column
- Sorted newest first
- Summary row with totals

## How to run
1. Install Python 3 (if not already installed)  
   Download from: https://www.python.org/downloads/

2. Install required libraries:
pip install xrpl-py requests
text3. **Important: Add your own XRPL address**  
Open the file `xrpl_tax_exporter.py` in any text editor (Notepad, VS Code, etc.)  
Look for this line near the top:
ADDRESS = "rEHHkaRTfQQZTxDkbDNM7hKgqqPHxQTZ3z"
textReplace the example address with your own XRPL address (classic or X-address format).  
Example:
ADDRESS = "rYourAddressHere1234567890"
text**Security note**: Never share your script file after adding your real address — it contains your wallet public address (not private key, so it's safe to share the blank version, but not with your address filled in).

4. Save the file, then run the script:
python xrpl_tax_exporter.py
text5. Output CSV appears in the `reports/` folder

## Sample output
See [`sample_output.csv`](sample_output.csv) for a real mainnet example (16 transactions from a test address).

## Feedback & Roadmap
This is an early prototype built for XRPL / Xaman users who need easier tax reporting.

What would make this useful for you?
- Koinly / CoinTracker import format?
- Memo / flags parsing?
- Live transaction monitoring?
- Canadian / US-specific tax notes?
- Paid version (monthly / one-time)?

Open an issue here, or DM me on X: [@Goose5Star](https://x.com/Goose5Star)

MIT License – contributions welcome!

Built with ❤️ for the XRPL community.
