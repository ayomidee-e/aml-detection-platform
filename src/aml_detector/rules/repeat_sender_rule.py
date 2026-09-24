from collections import Counter
from tqdm import tqdm
import pandas as pd

class RepeatSenderRule:
    """
    Flags accounts that send more than N transactions.

    Why: from EDA, top laundering account sent 243 transactions.
    Normal accounts send a handful. Repeat senders are mule accounts.
    """

    rule_id = "VELOCITY_001"
    severity = "high"

    def __init__(self, max_transactions: int = 20):
        self.max_transactions = max_transactions

    def evaluate(self, data):
        """
        data: a pandas DataFrame with columns 'Account' and 'Is Laundering'.

        Returns a DataFrame with one row per account that exceeded the limit,
        plus how many of that account's transactions were laundering.
        """
        # Count how many transactions each account sent
        counts = data["Account"].value_counts()

        # Keep only accounts above the threshold
        flagged_accounts = counts[counts > self.max_transactions].index

        # For each flagged account, summarize
        results = []
        
        # Wrap the loop with tqdm to show a live progress bar in the notebook/terminal
        for account in tqdm(flagged_accounts, desc="Evaluating Accounts"):
            account_rows = data[data["Account"] == account]
            total = len(account_rows)
            laundering = int(account_rows["Is Laundering"].sum())

            results.append({
                "account": account,
                "total_transactions": total,
                "laundering_transactions": laundering,
                "rule_id": self.rule_id,
                "severity": self.severity,
            })

        # Return as a DataFrame sorted by laundering count
        results_df = pd.DataFrame(results)
        if not results_df.empty:
            results_df = results_df.sort_values(
                "laundering_transactions", ascending=False
            ).reset_index(drop=True)

        return results_df