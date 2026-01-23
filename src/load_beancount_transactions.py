from beancount.loader import load_file
import pandas as pd

def load_beancount_transactions(file_path):
    """
    Load transactions from a Beancount ledger file into a pandas DataFrame.

    Parameters:
    - file_path (str): Path to the Beancount file.

    Returns:
    - pd.DataFrame: DataFrame containing transaction details.
    """
    entries, _, _ = load_file(file_path)

    txns = []
    for entry in entries:
        if entry.__class__.__name__ == "Transaction":
            txn_id = id(entry)  # new unique ID for this transaction
            for posting in entry.postings:
                txns.append({
                    "transaction_id": txn_id,
                    "date": entry.date,
                    "narration": entry.narration,
                    "meta": entry.meta,
                    "account": posting.account,
                    "units": posting.units.number,
                    "item": posting.units.currency
                })
    df = pd.DataFrame(txns)
    # Convert date to datetime
    df["date"] = pd.to_datetime(df["date"])  
    # Convert transaction size to numeric
    df['units'] = pd.to_numeric(df['units'], errors='raise')
    # Get type of the posting from meta
    df['type'] = df['meta'].apply(lambda m: m.get('type') if isinstance(m, dict) else None)
    df = df.drop(columns=['meta'])
    
    return df