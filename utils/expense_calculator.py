class Calculator:
    @staticmethod
    def multiply(a: float, b: float) -> float:
        return float(a) * float(b)

    @staticmethod
    def calculate_total(*x: float) -> float:
        return sum(x)

    @staticmethod
    def calculate_daily_budget(total: float, days: int) -> float:
        return total / days if days > 0 else 0