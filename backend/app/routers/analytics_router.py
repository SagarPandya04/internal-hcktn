"""Analytics router — wealth distribution endpoints.

Raw SQL strings were replaced with proper SQLAlchemy text() calls and ORM queries.
The gemini_service import is used only for necessity classification, with full
error isolation so a Gemini failure never crashes the endpoint.
"""
import time
from collections import defaultdict
from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, distinct

from .. import schemas, auth, database, models

router = APIRouter()

# ---------------------------------------------------------------------------
# Simple in-memory rate limiter (30 req/min per client IP)
# ---------------------------------------------------------------------------
_REQUEST_LOG: dict[str, list[float]] = defaultdict(list)
_MAX_REQUESTS_PER_MINUTE = 30


def rate_limiter(request: Request):
    ip = request.client.host if request.client else "unknown"
    now = time.time()
    window_start = now - 60
    timestamps = _REQUEST_LOG[ip]
    while timestamps and timestamps[0] < window_start:
        timestamps.pop(0)
    if len(timestamps) >= _MAX_REQUESTS_PER_MINUTE:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Too many requests – please retry later",
        )
    timestamps.append(now)
    return True


# ---------------------------------------------------------------------------
# Helper: classify necessity tier (rule-based fallback, no external calls)
# ---------------------------------------------------------------------------
def _classify_necessity(category: str, merchant: str, amount: float, narration: str) -> tuple[str, str]:
    try:
        from .. import gemini_service
        return gemini_service.classify_necessity_and_reasoning(
            category_name=category,
            merchant=merchant,
            amount=amount,
            raw_narration=narration,
        )
    except Exception:
        pass
    # Fallback
    text = (narration + " " + merchant + " " + category).lower()
    if any(k in text for k in ["rent", "electricity", "utility", "gas", "groceries", "hospital", "medicine"]):
        return "Necessary", f"Essential expense of ₹{amount:.2f}."
    if any(k in text for k in ["sip", "stock", "mutual fund", "invest", "zerodha", "groww"]):
        return "Important", f"Wealth-building outflow of ₹{amount:.2f}."
    if any(k in text for k in ["emi", "loan", "credit card"]):
        return "Important", f"Debt service obligation of ₹{amount:.2f}."
    if any(k in text for k in ["netflix", "spotify", "amazon", "shopping", "game", "apparel", "movie"]):
        return "Unnecessary", f"Discretionary spend of ₹{amount:.2f}."
    if any(k in text for k in ["swiggy", "zomato", "starbucks", "coffee", "dining", "restaurant"]):
        return "Can Be Resolved", f"Convenience dining spend of ₹{amount:.2f}."
    return "Can Be Resolved", f"General expense of ₹{amount:.2f}."


# ---------------------------------------------------------------------------
# Endpoints
# ---------------------------------------------------------------------------
@router.get(
    "/wealth-distribution",
    response_model=schemas.WealthDistributionResponse,
    dependencies=[Depends(rate_limiter)],
)
async def wealth_distribution(
    request: Request,
    db: AsyncSession = Depends(database.get_db),
    current_user: models.User = Depends(auth.get_current_active_user),
):
    try:
        cat_stmt = (
            select(distinct(models.Transaction.category))
            .where(models.Transaction.user_id == current_user.id)
        )
        cat_res = await db.execute(cat_stmt)
        categories = [row[0] for row in cat_res.all() if row[0]]

        category_data: dict[str, schemas.CategoryDistribution] = {}
        for cat in categories:
            category_data[cat] = await _build_category_detail(cat, current_user.id, db)

        return schemas.WealthDistributionResponse(
            categories=categories, category_data=category_data
        )
    except HTTPException:
        raise
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Analytics error: {exc}")


@router.get(
    "/wealth-distribution/{category}",
    response_model=schemas.CategoryDistribution,
    dependencies=[Depends(rate_limiter)],
)
async def category_detail(
    category: str,
    request: Request,
    db: AsyncSession = Depends(database.get_db),
    current_user: models.User = Depends(auth.get_current_active_user),
):
    return await _build_category_detail(category, current_user.id, db)


async def _build_category_detail(
    category: str, user_id: int, db: AsyncSession
) -> schemas.CategoryDistribution:
    # Totals
    agg_stmt = (
        select(
            func.sum(models.Transaction.amount).label("total"),
            func.count(models.Transaction.id).label("cnt"),
        )
        .where(
            models.Transaction.user_id == user_id,
            models.Transaction.category == category,
        )
    )
    row = (await db.execute(agg_stmt)).first()
    total_amount = float(row.total or 0.0)
    tx_count = int(row.cnt or 0)

    # All transactions in this category
    tx_stmt = select(models.Transaction).where(
        models.Transaction.user_id == user_id,
        models.Transaction.category == category,
    )
    txs = (await db.execute(tx_stmt)).scalars().all()

    breakdown: dict[str, dict] = defaultdict(lambda: {"amount": 0.0, "count": 0})
    tx_details: list[schemas.CategorizedTransactionDetail] = []

    for tx in txs:
        tier, reason = _classify_necessity(
            category=category,
            merchant=tx.cleaned_merchant or "",
            amount=tx.amount,
            narration=tx.raw_narration,
        )
        breakdown[tier]["amount"] += tx.amount
        breakdown[tier]["count"] += 1
        tx_details.append(
            schemas.CategorizedTransactionDetail(
                id=tx.id,
                timestamp=tx.timestamp,
                amount=tx.amount,
                merchant=tx.cleaned_merchant or "",
                raw_narration=tx.raw_narration,
                necessity_tier=tier,  # type: ignore[arg-type]
                reasoning=reason,
            )
        )

    grand_total = sum(v["amount"] for v in breakdown.values()) or 1.0
    pie_chart = [
        schemas.SubCategoryBreakdown(
            name=name,
            amount=data["amount"],
            count=data["count"],
            percentage=round((data["amount"] / grand_total) * 100, 2),
        )
        for name, data in breakdown.items()
    ]

    return schemas.CategoryDistribution(
        category=category,
        total_amount=total_amount,
        transaction_count=tx_count,
        pie_chart_data=pie_chart,
        transactions=tx_details,
    )
