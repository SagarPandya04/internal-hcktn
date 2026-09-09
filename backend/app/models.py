# app/models.py
"""SQLAlchemy ORM models for the FinTech platform."""

import enum
from sqlalchemy import Column, Integer, String, Float, DateTime, Enum, ForeignKey, Text
from sqlalchemy.orm import relationship
from .database import Base

# ---------------------------------------------------------------------------
# Enum definitions
# ---------------------------------------------------------------------------
class RoleEnum(str, enum.Enum):
    admin = "admin"
    user = "user"
    advisor = "advisor"

class TransactionType(str, enum.Enum):
    credit = "credit"
    debit = "debit"

class NecessityTier(str, enum.Enum):
    necessary = "Necessary"
    unnecessary = "Unnecessary"
    important = "Important"
    can_be_resolved = "Can Be Resolved"

class LimitPeriod(str, enum.Enum):
    monthly = "monthly"
    weekly = "weekly"

class SubscriptionInterval(str, enum.Enum):
    monthly = "monthly"
    yearly = "yearly"

class CoolingStatus(str, enum.Enum):
    pending = "pending"
    purchased = "purchased"
    saved = "saved"

class AnomalyType(str, enum.Enum):
    spike = "spike"
    frequency = "frequency"

# ---------------------------------------------------------------------------
# Core models
# ---------------------------------------------------------------------------
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    full_name = Column(String, nullable=True)
    role = Column(Enum(RoleEnum), default=RoleEnum.user, nullable=False)

    # Relationships
    transactions = relationship("Transaction", back_populates="owner", cascade="all, delete-orphan")
    merchant_limits = relationship("MerchantLimit", back_populates="user", cascade="all, delete-orphan")
    subscriptions = relationship("Subscription", back_populates="user", cascade="all, delete-orphan")
    cooling_off_items = relationship("CoolingOffItem", back_populates="user", cascade="all, delete-orphan")
    goal_buckets = relationship("GoalBucket", back_populates="user", cascade="all, delete-orphan")
    anomaly_insights = relationship("AnomalyInsight", back_populates="user", cascade="all, delete-orphan")

class Transaction(Base):
    __tablename__ = "transactions"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    timestamp = Column(DateTime, nullable=False)
    amount = Column(Float, nullable=False)
    type = Column(Enum(TransactionType), nullable=False)
    raw_narration = Column(Text, nullable=False)
    cleaned_merchant = Column(String, nullable=True)
    category = Column(String, nullable=True)  # Needs, Debt, Wants, Investments
    necessity_type = Column(Enum(NecessityTier), nullable=True)
    reasoning = Column(Text, nullable=True)

    owner = relationship("User", back_populates="transactions")

# ---------------------------------------------------------------------------
# Additional feature models
# ---------------------------------------------------------------------------
class MerchantLimit(Base):
    __tablename__ = "merchant_limits"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    merchant_name = Column(String, nullable=False)
    period = Column(Enum(LimitPeriod), nullable=False)
    cap_amount = Column(Float, nullable=False)
    spent_amount = Column(Float, default=0.0)
    period_start = Column(DateTime, nullable=False)

    user = relationship("User", back_populates="merchant_limits")

class Subscription(Base):
    __tablename__ = "subscriptions"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    merchant_name = Column(String, nullable=False)
    amount = Column(Float, nullable=False)
    interval = Column(Enum(SubscriptionInterval), nullable=False)
    next_due = Column(DateTime, nullable=False)
    last_amount = Column(Float, nullable=True)

    user = relationship("User", back_populates="subscriptions")

class CoolingOffItem(Base):
    __tablename__ = "cooling_off_items"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    description = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    added_at = Column(DateTime, nullable=False)
    unlock_at = Column(DateTime, nullable=False)
    status = Column(Enum(CoolingStatus), default=CoolingStatus.pending)

    user = relationship("User", back_populates="cooling_off_items")

class GoalBucket(Base):
    __tablename__ = "goal_buckets"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    name = Column(String, nullable=False)
    target_amount = Column(Float, nullable=False)
    current_amount = Column(Float, default=0.0)
    target_date = Column(DateTime, nullable=False)

    user = relationship("User", back_populates="goal_buckets")

class AnomalyInsight(Base):
    __tablename__ = "anomaly_insights"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    category = Column(String, nullable=False)
    date = Column(DateTime, nullable=False)
    amount = Column(Float, nullable=False)
    description = Column(Text, nullable=True)
    type = Column(Enum(AnomalyType), nullable=False)

    user = relationship("User", back_populates="anomaly_insights")
