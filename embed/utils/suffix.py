from config.settings import USER_SUFFIX, USER_SUFFIX_SOURCE, USER_SUFFIX_COST


class EUtilsSuffix:
    @staticmethod
    def add_suffix(response_ai):
        reply = response_ai.answer
        if USER_SUFFIX_SOURCE or USER_SUFFIX_COST:
            if USER_SUFFIX_SOURCE:
                reply += f"\n\n#{response_ai.source}"
            if USER_SUFFIX_COST:
                reply += f"\n{USER_SUFFIX}\n{response_ai.aiCostCurrency} {round(response_ai.aiCost, 6)}"
        return reply
