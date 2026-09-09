export interface CashFlowSummary {
  daily_earn: number;
  daily_burn: number;
  monthly_net_margin: number;
  annualized_extrapolation: number;
}

export interface DebtMetrics {
  dti: number;
  debt_drag_percentage: number;
  monthly_emi_total: number;
}

export interface BehavioralInsights {
  weekend_spike: boolean;
  post_payday_surge: boolean;
  subscription_monthly_total: number;
}

export interface SimulationResult {
  delta_savings: number;
  future_value_1y: number;
  future_value_3y: number;
  future_value_5y: number;
  tenure_reduction_months: number;
  interest_saved: number;
}

export interface TransactionRead {
  id: number;
  timestamp: string;
  amount: number;
  type: 'credit' | 'debit';
  raw_narration: string;
  cleaned_merchant?: string;
  category?: string;
}
