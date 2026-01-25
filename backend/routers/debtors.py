import sys
from pathlib import Path
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

# Add parent directory to path to import from src
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from src.load_beancount_transactions import load_beancount_transactions
from config import get_settings
from dependencies import get_current_user

router = APIRouter(prefix="/api", tags=["api"])


class Debtor(BaseModel):
    username: str
    balance: float


@router.get("/debtors", response_model=list[Debtor])
async def get_debtors(current_user: str = Depends(get_current_user)) -> list[Debtor]:
    """Get list of users with negative balances (debtors), sorted by amount owed."""
    settings = get_settings()
    beancount_path = Path(settings.tab_data_path) / "bartab.beancount"

    if not beancount_path.exists():
        raise HTTPException(
            status_code=500,
            detail=f"Beancount file not found at {beancount_path}",
        )

    try:
        # Load transactions
        transactions = load_beancount_transactions(str(beancount_path))

        # Filter for EUR transactions and extract member accounts
        euro_df = transactions[transactions["item"] == "EUR"].copy()
        euro_df["account"] = euro_df["account"].str.extract(
            r"Liabilities:Bar:Members:(.*)"
        )
        euro_df = euro_df.dropna(subset=["account"])

        # Calculate balances (negative = owes money)
        user_balances = -1 * euro_df.groupby("account")["units"].sum()

        # Filter for debtors (balance < -0.1 to avoid floating point noise)
        debtors = user_balances[user_balances < -0.1].sort_values()

        return [
            Debtor(username=username, balance=round(float(balance), 2))
            for username, balance in debtors.items()
        ]

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error calculating debtors: {str(e)}",
        )
