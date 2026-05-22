"""
用于测试 option_pricing 包功能的脚本：
- 测试使用 yfinance 从 Yahoo Finance 获取股票数据
- 测试 Black-Scholes 期权定价模型
- 测试二叉树期权定价模型
- 测试蒙特卡洛模拟期权定价
"""

from option_pricing import BlackScholesModel, MonteCarloPricing, BinomialTreeModel, Ticker

# 从 Yahoo Finance 获取价格数据
data = Ticker.get_historical_data('TSLA')
print(Ticker.get_columns(data))
print(Ticker.get_last_price(data, 'Adj Close'))
Ticker.plot_data(data, 'TSLA', 'Adj Close')

# 测试 Black-Scholes 模型
BSM = BlackScholesModel(100, 100, 365, 0.1, 0.2)
print(BSM.calculate_option_price('Call Option'))
print(BSM.calculate_option_price('Put Option'))

# 测试二叉树模型
BOPM = BinomialTreeModel(100, 100, 365, 0.1, 0.2, 15000)
print(BOPM.calculate_option_price('Call Option'))
print(BOPM.calculate_option_price('Put Option'))

# 测试蒙特卡洛模拟
MC = MonteCarloPricing(100, 100, 365, 0.1, 0.2, 10000)
MC.simulate_prices()
print(MC.calculate_option_price('Call Option'))
print(MC.calculate_option_price('Put Option'))
MC.plot_simulation_results(20)


