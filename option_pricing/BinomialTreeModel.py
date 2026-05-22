# 第三方依赖
import numpy as np
from scipy.stats import norm 

# 本地包依赖
from .base import OptionPricingModel


class BinomialTreeModel(OptionPricingModel):
    """ 
    使用 BOPM（二叉树期权定价模型）计算欧式期权价格。
    该模型在估值日和行权日之间按离散时间点（格点）计算期权价格。
    定价过程分为三步：
    - 生成价格树
    - 计算最终节点的期权价值
    - 逐层回溯计算前序节点的期权价值
    """

    def __init__(self, underlying_spot_price, strike_price, days_to_maturity, risk_free_rate, sigma, number_of_time_steps):
        """
        初始化二叉树模型所需变量。

        underlying_spot_price: 股票或其他标的资产当前现货价格
        strike_price: 期权合约行权价
        days_to_maturity: 距期权到期/行权日的天数
        risk_free_rate: 无风险资产收益率（假设到期前保持不变）
        sigma: 标的资产波动率（资产对数收益率的标准差）
        number_of_time_steps: 估值日到行权日之间的时间步数
        """
        self.S = underlying_spot_price
        self.K = strike_price
        self.T = days_to_maturity / 365
        self.r = risk_free_rate
        self.sigma = sigma
        self.number_of_time_steps = number_of_time_steps

    def _calculate_call_option_price(self): 
        """根据二叉树公式计算看涨期权价格。"""
        # 时间间隔、上涨因子和下跌因子
        dT = self.T / self.number_of_time_steps                             
        u = np.exp(self.sigma * np.sqrt(dT))                 
        d = 1.0 / u                                    

        # 初始化价格向量
        V = np.zeros(self.number_of_time_steps + 1)                       

        # 不同时间点上的标的资产价格
        S_T = np.array( [(self.S * u**j * d**(self.number_of_time_steps - j)) for j in range(self.number_of_time_steps + 1)])

        a = np.exp(self.r * dT)      # 无风险复利收益
        p = (a - d) / (u - d)        # 风险中性上涨概率
        q = 1.0 - p                  # 风险中性下跌概率

        V[:] = np.maximum(S_T - self.K, 0.0)
    
        # 回溯更新期权价格
        for i in range(self.number_of_time_steps - 1, -1, -1):
            V[:-1] = np.exp(-self.r * dT) * (p * V[1:] + q * V[:-1]) 

        return V[0]

    def _calculate_put_option_price(self): 
        """根据二叉树公式计算看跌期权价格。"""
        # 时间间隔、上涨因子和下跌因子
        dT = self.T / self.number_of_time_steps                             
        u = np.exp(self.sigma * np.sqrt(dT))                 
        d = 1.0 / u                                    

        # 初始化价格向量
        V = np.zeros(self.number_of_time_steps + 1)                       

        # 不同时间点上的标的资产价格
        S_T = np.array( [(self.S * u**j * d**(self.number_of_time_steps - j)) for j in range(self.number_of_time_steps + 1)])

        a = np.exp(self.r * dT)      # 无风险复利收益
        p = (a - d) / (u - d)        # 风险中性上涨概率
        q = 1.0 - p                  # 风险中性下跌概率

        V[:] = np.maximum(self.K - S_T, 0.0)
    
        # 回溯更新期权价格
        for i in range(self.number_of_time_steps - 1, -1, -1):
            V[:-1] = np.exp(-self.r * dT) * (p * V[1:] + q * V[:-1]) 

        return V[0]
