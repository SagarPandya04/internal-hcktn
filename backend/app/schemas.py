from pydantic import BaseModel, Field, EmailStr, ConfigDict
from datetime import datetime
from typing import Optional, Literal, List, Dict

# User schemas
class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8)
    full_name: Optional[str] = None
    role: Literal["admin", "user", "advisor"] = "user"

class UserRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    email: EmailStr
    full_name: Optional[str] = None
    role: str

# Token schemas
class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class TokenData(BaseModel):
    user_id: Optional[int] = None
    role: Optional[str] = None

# Transaction schemas
class TransactionCreate(BaseModel):
    timestamp: datetime
    amount: float
    type: Literal["credit", "debit"]
    raw_narration: str
    cleaned_merchant: Optional[str] = None
    category: Optional[str] = None

class TransactionRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    timestamp: datetime
    amount: float
    type: str
    raw_narration: str
    cleaned_merchant: Optional[str] = None
    category: Optional[str] = None

# Gemini structured response models
class MerchantCleaningResponse(BaseModel):
    cleaned_merchant: str = Field(..., description="Human readable merchant name")

class CategorizationResponse(BaseModel):
    category: Literal["Needs", "Debt", "Wants", "Investments"]

# Analytics response models
class CashFlowSummary(BaseModel):
    daily_earn: float
    daily_burn: float
    monthly_net_margin: float
    annualized_extrapolation: float

class DebtMetrics(BaseModel):
    dti: float
    debt_drag_percentage: float
    monthly_emi_total: float

class BehavioralInsights(BaseModel):
    weekend_spike: bool
    post_payday_surge: bool
    subscription_monthly_total: float

class SimulationResult(BaseModel):
    delta_savings: float
    future_value_1y: float
    future_value_3y: float
    future_value_5y: float
    tenure_reduction_months: int
    interest_saved: float

# Wealth Distribution Schemas
class SubCategoryBreakdown(BaseModel):
    name: str  # Necessary, Unnecessary, Important, Can Be Resolved
    amount: float
    count: int
    percentage: float

class CategorizedTransactionDetail(BaseModel):
    id: int
    timestamp: datetime
    amount: float
    merchant: str
    raw_narration: str
    necessity_tier: Literal["Necessary", "Unnecessary", "Important", "Can Be Resolved"]
    reasoning: str

class CategoryDistribution(BaseModel):
    category: str
    total_amount: float
    transaction_count: int
    pie_chart_data: List[SubCategoryBreakdown]
    transactions: List[CategorizedTransactionDetail]

class WealthDistributionResponse(BaseModel):
    categories: List[str]
    category_data: Dict[str, CategoryDistribution]
