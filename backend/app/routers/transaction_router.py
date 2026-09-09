# app/routers/transaction_router.py
"""Routes for managing transactions."""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from .. import schemas, models, auth, database

router = APIRouter()

@router.post("/", response_model=schemas.TransactionRead)
async def create_transaction(
    tx_in: schemas.TransactionCreate,
    db: AsyncSession = Depends(database.get_db),
    current_user: models.User = Depends(auth.get_current_active_user),
):
    db_tx = models.Transaction(
        user_id=current_user.id,
        timestamp=tx_in.timestamp,
        amount=tx_in.amount,
        type=tx_in.type,
        raw_narration=tx_in.raw_narration,
        cleaned_merchant=tx_in.cleaned_merchant,
        category=tx_in.category,
    )
    db.add(db_tx)
    await db.commit()
    await db.refresh(db_tx)
    return schemas.TransactionRead.from_orm(db_tx)

@router.get("/", response_model=list[schemas.TransactionRead])
async def list_transactions(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(database.get_db),
    current_user: models.User = Depends(auth.get_current_active_user),
):
    result = await db.execute(
        select(models.Transaction)
        .where(models.Transaction.user_id == current_user.id)
        .offset(skip)
        .limit(limit)
    )
    transactions = result.scalars().all()
    return [schemas.TransactionRead.from_orm(t) for t in transactions]

@router.get("/{tx_id}", response_model=schemas.TransactionRead)
async def get_transaction(
    tx_id: int,
    db: AsyncSession = Depends(database.get_db),
    current_user: models.User = Depends(auth.get_current_active_user),
):
    result = await db.execute(
        select(models.Transaction)
        .where(models.Transaction.id == tx_id, models.Transaction.user_id == current_user.id)
    )
    tx = result.scalar_one_or_none()
    if not tx:
        raise HTTPException(status_code=404, detail="Transaction not found")
    return schemas.TransactionRead.from_orm(tx)
