# 第三方依赖
import numpy as np
from scipy.stats import norm 

# 本地包依赖
from .base import OptionPricingModel


class BlackScholesModel(OptionPricingModel):
    """ 
    使用 Black-Scholes 公式计算欧式期权价格。

    看涨/看跌期权价格基于以下假设计算：
    - 欧式期权只能在到期日行权。
    - 标的股票在期权有效期内不分红。
    - 无风险利率和波动率保持不变。
    - 有效市场假说：市场走势无法被预测。
    - 标的资产收益服从对数正态分布。
    """

    def __init__(self, underlying_spot_price, strike_price, days_to_maturity, risk_free_rate, sigma):
        """
        初始化 Black-Scholes 公式所需变量。

        underlying_spot_price: 股票或其他标的资产当前现货价格
        strike_price: 期权合约行权价
        days_to_maturity: 距期权到期/行权日的天数
        risk_free_rate: 无风险资产收益率（假设到期前保持不变）
        sigma: 标的资产波动率（资产对数收益率的标准差）
        """
        self.S = underlying_spot_price
        self.K = strike_price
        self.T = days_to_maturity / 365
        self.r = risk_free_rate
        self.sigma = sigma

    def _calculate_call_option_price(self): 
        """
        根据公式计算看涨期权价格。
        公式：S*N(d1) - PresentValue(K)*N(d2)
        """
        # 标准正态分布的累积分布函数（风险调整后的行权概率）
        d1 = (np.log(self.S / self.K) + (self.r + 0.5 * self.sigma ** 2) * self.T) / (self.sigma * np.sqrt(self.T))
        
        # 标准正态分布的累积分布函数（期权到期时获得股票的概率）
        d2 = (np.log(self.S / self.K) + (self.r - 0.5 * self.sigma ** 2) * self.T) / (self.sigma * np.sqrt(self.T))
        
        return (self.S * norm.cdf(d1, 0.0, 1.0) - self.K * np.exp(-self.r * self.T) * norm.cdf(d2, 0.0, 1.0))
    

    def _calculate_put_option_price(self): 
        """
        根据公式计算看跌期权价格。
        公式：PresentValue(K)*N(-d2) - S*N(-d1)
        """  
        # 标准正态分布的累积分布函数（风险调整后的行权概率）
        d1 = (np.log(self.S / self.K) + (self.r + 0.5 * self.sigma ** 2) * self.T) / (self.sigma * np.sqrt(self.T))

        # 标准正态分布的累积分布函数（期权到期时获得股票的概率）
        d2 = (np.log(self.S / self.K) + (self.r - 0.5 * self.sigma ** 2) * self.T) / (self.sigma * np.sqrt(self.T))
        
        return (self.K * np.exp(-self.r * self.T) * norm.cdf(-d2, 0.0, 1.0) - self.S * norm.cdf(-d1, 0.0, 1.0))
