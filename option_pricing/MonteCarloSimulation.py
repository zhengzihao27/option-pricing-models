# 第三方依赖
import numpy as np
from scipy.stats import norm 
import matplotlib.pyplot as plt

# 本地包依赖
from .base import OptionPricingModel


class MonteCarloPricing(OptionPricingModel):
    """ 
    使用蒙特卡洛模拟计算欧式期权价格。
    通过随机过程（布朗运动）模拟标的资产在到期日的价格。
    对模拟生成的到期价格计算收益、求平均并折现，得到期权价格。
    """

    def __init__(self, underlying_spot_price, strike_price, days_to_maturity, risk_free_rate, sigma, number_of_simulations):
        """
        初始化蒙特卡洛模拟所需变量。

        underlying_spot_price: 股票或其他标的资产当前现货价格
        strike_price: 期权合约行权价
        days_to_maturity: 距期权到期/行权日的天数
        risk_free_rate: 无风险资产收益率（假设到期前保持不变）
        sigma: 标的资产波动率（资产对数收益率的标准差）
        number_of_simulations: 随机价格路径模拟次数
        """
        # 布朗运动过程参数
        self.S_0 = underlying_spot_price
        self.K = strike_price
        self.T = days_to_maturity / 365
        self.r = risk_free_rate
        self.sigma = sigma 

        # 模拟参数
        self.N = number_of_simulations
        self.num_of_steps = days_to_maturity
        self.dt = self.T / self.num_of_steps

    def simulate_prices(self):
        """
        使用布朗随机过程模拟标的资产价格路径，并保存模拟结果。
        """
        np.random.seed(20)
        self.simulation_results = None

        # 初始化价格路径矩阵：行表示时间索引，列表示不同随机价格路径。
        S = np.zeros((self.num_of_steps, self.N))        
        # 所有价格路径的初始值均为当前现货价格。
        S[0] = self.S_0

        for t in range(1, self.num_of_steps):
            # 用于模拟布朗运动的随机值（高斯分布）。
            Z = np.random.standard_normal(self.N)
            # 更新下一时间点的价格。
            S[t] = S[t - 1] * np.exp((self.r - 0.5 * self.sigma ** 2) * self.dt + (self.sigma * np.sqrt(self.dt) * Z))

        self.simulation_results_S = S

    def _calculate_call_option_price(self): 
        """
        计算看涨期权价格：对到期模拟价格的收益求和、取平均并折现。
        看涨期权收益（仅当到期价格高于行权价时行权）：max(S_t - K, 0)
        """
        if self.simulation_results_S is None:
            return -1
        return np.exp(-self.r * self.T) * 1 / self.N * np.sum(np.maximum(self.simulation_results_S[-1] - self.K, 0))
    

    def _calculate_put_option_price(self): 
        """
        计算看跌期权价格：对到期模拟价格的收益求和、取平均并折现。
        看跌期权收益（仅当到期价格低于行权价时行权）：max(K - S_t, 0)
        """
        if self.simulation_results_S is None:
            return -1
        return np.exp(-self.r * self.T) * 1 / self.N * np.sum(np.maximum(self.K - self.simulation_results_S[-1], 0))
       

    def plot_simulation_results(self, num_of_movements):
        """绘制指定数量的模拟价格路径。"""
        fig, ax = plt.subplots(figsize=(12, 8))
        ax.plot(self.simulation_results_S[:, 0:num_of_movements])
        ax.axhline(self.K, c='k', label='Strike Price')
        ax.set_xlim([0, self.num_of_steps])
        ax.set_ylabel('Simulated price movements')
        ax.set_xlabel('Days in future')
        ax.set_title(f'First {num_of_movements}/{self.N} Random Price Movements')
        ax.legend(loc='best')
        return fig
