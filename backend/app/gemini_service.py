import os
import re
from pydantic import BaseModel
from .config import settings

class MerchantCleaningResponse(BaseModel):
    cleaned_merchant: str

class CategorizationResponse(BaseModel):
    category: str  # Needs, Debt, Wants, Investments

def _fallback_clean(raw_narration: str) -> str:
    parts = re.split(r'[/_\-\s:]+', raw_narration)
    meaningful = [p for p in parts if len(p) > 2 and not p.isdigit() and p.lower() not in ['upi', 'pos', 'neft', 'rtgs', 'imps', 'tx', 'txn', 'pay']]
    if meaningful:
        return meaningful[-1].capitalize()
    return raw_narration.strip().title()

def _fallback_categorize(raw_narration: str, amount: float) -> str:
    text = raw_narration.lower()
    if any(k in text for k in ['emi', 'loan', 'credit card', 'interest', 'debt', 'mortgage']):
        return "Debt"
    if any(k in text for k in ['mutual fund', 'sip', 'zerodha', 'groww', 'stock', 'invest', 'nps', 'ppf']):
        return "Investments"
    if any(k in text for k in ['swiggy', 'zomato', 'netflix', 'amazon', 'starbucks', 'movie', 'game', 'pub', 'party', 'apparel', 'shopping', 'dine']):
        return "Wants"
    return "Needs"

async def clean_merchant(raw_narration: str) -> MerchantCleaningResponse:
    if settings.GEMINI_API_KEY:
        try:
            from google import genai
            client = genai.Client(api_key=settings.GEMINI_API_KEY)
            prompt = f"Clean this transaction narration to just the merchant name: '{raw_narration}'"
            response = client.models.generate_content(
                model='gemini-2.5-flash',
                contents=prompt,
            )
            cleaned = response.text.strip()
            if cleaned:
                return MerchantCleaningResponse(cleaned_merchant=cleaned)
        except Exception as e:
            # Handles 429 Too Many Requests / ResourceExhausted gracefully
            pass
    return MerchantCleaningResponse(cleaned_merchant=_fallback_clean(raw_narration))

async def categorize_transaction(raw_narration: str, amount: float) -> CategorizationResponse:
    if settings.GEMINI_API_KEY:
        try:
            from google import genai
            client = genai.Client(api_key=settings.GEMINI_API_KEY)
            prompt = f"Categorize transaction '{raw_narration}' of amount {amount} into exactly one of: Needs, Debt, Wants, Investments. Return only the category name."
            response = client.models.generate_content(
                model='gemini-2.5-flash',
                contents=prompt,
            )
            cat = response.text.strip()
            for valid in ["Needs", "Debt", "Wants", "Investments"]:
                if valid.lower() in cat.lower():
                    return CategorizationResponse(category=valid)
        except Exception:
            pass
    return CategorizationResponse(category=_fallback_categorize(raw_narration, amount))

def classify_necessity_and_reasoning(category_name: str, merchant: str, amount: float, raw_narration: str) -> tuple[str, str]:
    """Classifies transaction into one of four necessity tiers:
    - Necessary
    - Unnecessary
    - Important
    - Can Be Resolved

    And returns non-judgmental behavioral coaching reasoning.
    Handles 429 Too Many Requests gracefully with robust rule-based logic.
    """
    text = (raw_narration + " " + merchant + " " + category_name).lower()

    if any(k in text for k in ['rent', 'electricity', 'utility', 'power', 'water', 'gas', 'groceries', 'hospital', 'medicine']):
        if 'power' in text or 'electricity' in text or 'gas' in text or 'rent' in text:
            return (
                "Necessary",
                f"Essential fixed living expense. ${amount:.2F} paid for essential utility service to maintain shelter and health."
            )
        return (
            "Important",
            f"Core recurring operational cost. ${amount:.2f} allocated for household sustenance."
        )

    if any(k in text for k in ['sip', 'stock', 'mutual fund', 'zerodha', 'groww', 'nps', 'invest']):
        return (
            "Important",
            f"Wealth accumulation outflow. ${amount:.2f} committed to compounding asset growth and long-term financial security."
        )

    if any(k in text for k in ['emi', 'loan', 'credit card']):
        return (
            "Important",
            f"Contractual liability obligation. ${amount:.2f} servicing debt to maintain credit health and reduce principal."
        )

    if any(k in text for k in ['swiggy', 'zomato', 'starbucks', 'coffee', 'dining', 'bistro', 'restaurant', 'bar', 'pub', 'club']):
        return (
            "Can Be Resolved",
            f"Discretionary convenience dining. ${amount:.2f} spend at {merchant}. Could be resolved by meal planning or home coffee brewing."
        )

    if any(k in text for k in ['netflix', 'spotify', 'amazon', 'shopping', 'game', 'apparel', 'movie']):
        return (
            "Unnecessary",
            f"Discretionary entertainment subscription/shopping. ${amount:.2f} spent on non-essential recreation. High candidate for budget compromise."
        )

    # Fallback default rule
    if amount > 100:
        return (
            "Important",
            f"Significant expenditure of ${amount:.2f} at {merchant}. Recommended for periodic review."
        )
    return (
        "Can Be Resolved",
        f"Flexible lifestyle outlay of ${amount:.2f}. Potential candidate for reallocation into savings."
    )
