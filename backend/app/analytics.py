"""Analytics utilities for the FinTech platform.
Provides functions to compute wealth distribution, categorize transactions, and generate
insights used by the frontend.
"""
import asyncio
from typing import List
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from . import models, schemas, database

async def get_wealth_distribution(user_id: int, db: AsyncSession) -> List[schemas.WealthCategory]:
    """Return aggregated spend per category for a given user.
    Expected categories: utilities, electricity, gas, stocks, food, etc.
    """
    stmt = (
        select(models.Transaction.category, func.sum(models.Transaction.amount).label("total"))
        .where(models.Transaction.user_id == user_id)
        .group_by(models.Transaction.category)
    )
    result = await db.execute(stmt)
    rows = result.all()
    return [schemas.WealthCategory(category=row[0], total=row[1]) for row in rows]

async def get_transaction_detail(tx_id: int, db: AsyncSession) -> schemas.TransactionDetail:
    """Fetch detailed info for a transaction, including merchant cleaning, categorization
    and behavioral reasoning.
    """
    result = await db.execute(select(models.Transaction).where(models.Transaction.id == tx_id))
    tx = result.scalar_one_or_none()
    if not tx:
        raise ValueError("Transaction not found")
    # Direct mapping; in real code you might enrich via gemini_service
    return schemas.TransactionDetail.from_orm(tx)

# Additional analytics functions can be added here.
