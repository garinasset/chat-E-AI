class UtilsCalculate:

    @staticmethod
    def cal_token_cost(prompt_tokens, completion_tokens, model: dict) -> float:
        token_cost = ((prompt_tokens * model["PriceInput"] + completion_tokens * model["PriceOutput"]) / model["UnitPrice"])
        return token_cost
