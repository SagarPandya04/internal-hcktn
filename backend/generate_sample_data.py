import asyncio
from datetime import datetime, timedelta
from app.database import AsyncSessionLocal, init_db
from app.models import User, Transaction, RoleEnum
from app.auth import get_password_hash
from sqlalchemy import select

async def seed_data():
    await init_db()
    async with AsyncSessionLocal() as session:
        # Check if users already exist
        res = await session.execute(select(User))
        if res.scalars().first():
            print("Database already seeded.")
            return

        print("Seeding database...")
        # Create users
        admin = User(
            email="admin@fintech.com",
            hashed_password=get_password_hash("admin12345"),
            full_name="Admin User",
            role=RoleEnum.admin,
        )
        user = User(
            email="user@fintech.com",
            hashed_password=get_password_hash("user12345"),
            full_name="Alex Morgan",
            role=RoleEnum.user,
        )
        session.add_all([admin, user])
        await session.commit()
        await session.refresh(user)

        # Generate sample transactions over the past 30 days
        now = datetime.now()
        sample_txs = [
            # Inflow / Salary
            (now - timedelta(days=28), 5000.0, "credit", "SALARY CREDIT TECH CORP", "Tech Corp", "Needs"),
            # EMIs / Debt
            (now - timedelta(days=25), 850.0, "debit", "ACH DEBIT HOME LOAN EMI", "Home Loan EMI", "Debt"),
            (now - timedelta(days=22), 250.0, "debit", "AUTO DEBIT CAR LOAN EMI", "Car Loan EMI", "Debt"),
            # Needs
            (now - timedelta(days=27), 400.0, "debit", "ACH RENT PAYMENT LANDLORD", "Landlord Rent", "Needs"),
            (now - timedelta(days=20), 120.0, "debit", "UPI/1092/POWER UTILITY", "Power Utility", "Needs"),
            (now - timedelta(days=15), 180.0, "debit", "POS GROCERY SUPERMARKET", "Supermarket", "Needs"),
            # Investments
            (now - timedelta(days=24), 500.0, "debit", "ACH MUTUAL FUND SIP INDEX", "Vanguard Index", "Investments"),
            (now - timedelta(days=10), 300.0, "debit", "ZERODHA EQUITY SIP STOCKS", "Zerodha", "Investments"),
            # Wants / Discretionary
            (now - timedelta(days=26), 45.0, "debit", "UPI/9842/SWIGGY FOOD DEL", "Swiggy", "Wants"),
            (now - timedelta(days=21), 65.0, "debit", "POS STARBUCKS COFFEE NY", "Starbucks", "Wants"),
            (now - timedelta(days=14), 110.0, "debit", "POS DINING ITALIAN RESTAURANT", "Bistro Restaurant", "Wants"),
            (now - timedelta(days=7), 85.0, "debit", "AMAZON ONLINE SHOPPING", "Amazon", "Wants"),
            (now - timedelta(days=3), 15.0, "debit", "NETFLIX MONTHLY SUBSCRIPTION", "Netflix", "Wants"),
            (now - timedelta(days=2), 55.0, "debit", "UPI/4512/SWIGGY FOOD DEL", "Swiggy", "Wants"),
        ]

        for ts, amt, txtype, raw, merchant, cat in sample_txs:
            session.add(
                Transaction(
                    user_id=user.id,
                    timestamp=ts,
                    amount=amt,
                    type=txtype,
                    raw_narration=raw,
                    cleaned_merchant=merchant,
                    category=cat,
                )
            )

        await session.commit()
        print("Database successfully seeded with demo user (user@fintech.com / user12345) and transactions!")

if __name__ == "__main__":
    asyncio.run(seed_data())
