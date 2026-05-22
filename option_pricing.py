class BlackScholesModel:
    # ...（现有代码）...

    def get_calculation_steps(self):
        steps = {
            "Input Parameters": {
                "Spot Price": self.S,
                "Strike Price": self.K,
                "Time to Maturity (days)": self.T,
                "Risk-free Rate": self.r,
                "Volatility": self.sigma
            },
            "Intermediate Calculations": {
                "d1": self.d1,
                "d2": self.d2,
                "N(d1)": self.N_d1,
                "N(d2)": self.N_d2,
                "N(-d1)": self.N_minus_d1,
                "N(-d2)": self.N_minus_d2
            },
            "Final Calculations": {
                "Call Option Price": self.call_price,
                "Put Option Price": self.put_price
            }
        }
        return steps

# 同样，可以为 MonteCarloPricing 和 BinomialTreeModel 类添加 get_calculation_steps() 方法。
