import logging

class BudgetAgent:
    def run(self, data: dict):
        logging.info("BudgetAgent: estimating budget")
        
        # --- INPUT VALIDATION ---
        budget = data.get("budget")
        if budget is None or budget <= 0:
            raise ValueError("Invalid budget: must be greater than zero.")
        
        duration = data.get("duration", 1)
        if duration <= 0:
            raise ValueError("Invalid duration: must be greater than zero.")
        
        # --- BUDGET ESTIMATION ---
        base_daily = 100
        estimate = base_daily * duration
        flagged = budget < estimate

        data["budget_estimate"] = {"estimate": estimate, "flagged": flagged}
        logging.info(f"BudgetAgent: estimate={estimate}, flagged={flagged}")
        return data
