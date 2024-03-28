import pdfplumber
import pandas as pd
import re
from pathlib import Path

def parse_transaction_line(line):
    # Adjusted pattern to be more general and match any transaction type
    # The pattern now captures the date, then any text up to the numeric amounts for deduction/addition and balance
    pattern = re.compile(r'(\d{2}[A-Za-zéû]{3,4}) (.*?) (\d+,\d{2}) (\d+,\d{2})$')
    match = pattern.match(line)
    if match:
        date, description, amount, balance = match.groups()
        # Normalize the amount and balance by replacing comma with a dot for decimal
        amount = amount.replace(',', '.')
        balance = balance.replace(',', '.')
        # Attempt to reinsert spaces in the description based on camel case and commas
        spaced_description = re.sub(r"([A-Z])", r"\1", description).strip()
        spaced_description = spaced_description.replace(',', ' : ')
        return {
            "Date": date,
            "Description": spaced_description,
            "Amount": amount,
            "Balance": balance
        }
    else:
        return None

def extract_transactions_from_pdf(pdf_path):
    transactions = []
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            for line in text.split('\n'):
                # Attempt to parse each line as a transaction
                parsed_line = parse_transaction_line(line)
                if parsed_line:
                    transactions.append(parsed_line)
    print(transactions)
    return transactions


def process_pdf_folder(folder_path):
    pdf_folder = Path(folder_path)
    for pdf_file in pdf_folder.glob('*.pdf'):
        transactions = extract_transactions_from_pdf(pdf_file)
        if transactions:  # Only proceed if transactions were found
            df_transactions = pd.DataFrame(transactions)
            csv_path = pdf_file.with_suffix('.csv')
            df_transactions.to_csv(csv_path, index=False)
            print(f"Extracted transactions saved to {csv_path}")

folder_path = "Rayane's Bank Statements"
process_pdf_folder(folder_path)