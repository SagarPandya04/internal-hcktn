from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from .. import models, schemas, auth, database

router = APIRouter()

@router.get("/", response_model=schemas.WealthDistributionResponse)
async def get_wealth_distribution(
    db: AsyncSession = Depends(database.get_db),
    current_user: models.User = Depends(auth.get_current_active_user),
):
    """Return wealth distribution across categories with pie‑chart data and transaction details.
    Handles overload by catching generic exceptions and responding with 429.
    """
    try:
        # Distinct categories for the user
        cat_stmt = select(models.Transaction.category).where(models.Transaction.user_id == current_user.id).distinct()
        cat_res = await db.execute(cat_stmt)
        categories = [row[0] for row in cat_res.all() if row[0]]

        category_data: dict[str, schemas.CategoryDistribution] = {}
        for cat in categories:
            # Aggregate total amount and count per category
            agg_stmt = (
                select(func.sum(models.Transaction.amount).label("total"), func.count(models.Transaction.id).label("cnt"))
                .where(models.Transaction.user_id == current_user.id, models.Transaction.category == cat)
            )
            total, cnt = (await db.execute(agg_stmt)).first()
            total = total or 0.0
            cnt = cnt or 0

            # Pie chart breakdown by necessity tier
            pie_stmt = (
                select(models.Transaction.necessity_type, func.sum(models.Transaction.amount), func.count(models.Transaction.id))
                .where(models.Transaction.user_id == current_user.id, models.Transaction.category == cat)
                .group_by(models.Transaction.necessity_type)
            )
            pie_rows = await db.execute(pie_stmt)
            pie_data: list[schemas.SubCategoryBreakdown] = []
            for tier, amt, c in pie_rows:
                if tier is None:
                    continue
                percentage = (amt / total) * 100 if total else 0
                pie_data.append(
                    schemas.SubCategoryBreakdown(
                        name=tier.value,
                        amount=amt,
                        count=c,
                        percentage=percentage,
                    )
                )

            # Detailed transactions for this category
            tx_stmt = select(models.Transaction).where(models.Transaction.user_id == current_user.id, models.Transaction.category == cat)
            tx_res = await db.execute(tx_stmt)
            txs = tx_res.scalars().all()
            tx_details: list[schemas.CategorizedTransactionDetail] = []
            for tx in txs:
                tx_details.append(
                    schemas.CategorizedTransactionDetail(
                        id=tx.id,
                        timestamp=tx.timestamp,
                        amount=tx.amount,
                        merchant=tx.cleaned_merchant or "",
                        raw_narration=tx.raw_narration,
                        necessity_tier=tx.necessity_type.value if tx.necessity_type else "Can Be Resolved",
                        reasoning=tx.reasoning or "",
                    )
                )

            category_data[cat] = schemas.CategoryDistribution(
                category=cat,
                total_amount=total,
                transaction_count=cnt,
                pie_chart_data=pie_data,
                transactions=tx_details,
            )
        return schemas.WealthDistributionResponse(categories=categories, category_data=category_data)
    except Exception as e:
        # In a real system you would log the exception
        raise HTTPException(status_code=429, detail="Too many requests – please try again later.")
