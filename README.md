# 期权定价模型 Web 应用

这是一个基于 Streamlit 的期权定价演示项目，用于计算欧式期权价格，并对不同定价模型的结果进行比较。

项目当前支持三种定价方法：

1. Black-Scholes 模型
2. 蒙特卡洛模拟
3. 二叉树模型

应用会通过 `yfinance` 从 Yahoo Finance 获取股票历史行情和最近收盘价，并将股票价格作为期权定价中的标的资产现货价格。

## 功能

- 输入股票代码，例如 `AAPL`、`TSLA`
- 自动获取股票最近价格和历史行情
- 支持设置期权参数：
  - 行权价
  - 无风险利率
  - 波动率
  - 到期日
  - 蒙特卡洛模拟次数
  - 二叉树时间步数
- 展示历史价格走势图
- 计算看涨期权和看跌期权价格
- 对蒙特卡洛模拟路径进行可视化

## 定价模型

### Black-Scholes 模型

Black-Scholes 模型用于计算欧式期权的理论价格。模型假设标的资产收益服从对数正态分布，并使用现货价格、行权价、到期时间、无风险利率和波动率计算期权价格。

### 蒙特卡洛模拟

蒙特卡洛方法通过随机生成大量可能的未来价格路径，估算期权到期时的收益，并将平均收益折现为当前价格。

### 二叉树模型

二叉树模型将标的资产价格的变化拆分为多个离散时间步，每一步价格可以上涨或下跌。模型从到期日收益开始反向递推，最终得到当前期权价格。

## 项目结构

```text
.
├── option_pricing/              # 期权定价模型实现
│   ├── BlackScholesModel.py     # Black-Scholes 模型
│   ├── MonteCarloSimulation.py  # 蒙特卡洛模拟模型
│   ├── BinomialTreeModel.py     # 二叉树模型
│   ├── base.py                  # 定价模型抽象基类
│   └── ticker.py                # 股票行情获取和绘图工具
├── media/                       # 应用演示 GIF
├── streamlit_app.py             # Streamlit Web 应用入口
├── option_pricing_test.py       # 简单测试脚本
├── requirements.txt             # Python 依赖
├── data_cache/                  # 已缓存的本地行情数据
├── Dockerfile                   # Docker 运行配置
└── app.yaml                     # Google Cloud App Engine 配置
```

## 本地运行

推荐使用 Conda 创建独立 Python 环境。

### 1. 创建并激活环境

```powershell
conda create -n option-pricing-models python=3.12 -y
conda activate option-pricing-models
```

### 2. 安装依赖

```powershell
pip install -r requirements.txt
```

### 3. 启动应用

```powershell
streamlit run streamlit_app.py
```

启动后在浏览器打开：

```text
http://localhost:8501
```

之后再次启动项目时，只需要：

```powershell
conda activate option-pricing-models
streamlit run streamlit_app.py
```

## Docker 运行

如果已经安装 Docker，也可以通过容器运行：

```powershell
docker build -t options-pricing:latest .
docker run -p 8080:8080 options-pricing:latest
```

然后打开：

```text
http://127.0.0.1:8080
```

## 数据来源

项目优先读取 `data_cache/` 中的本地行情缓存。缓存不存在时，才会使用 `yfinance` 从 Yahoo Finance 获取行情数据，并在请求成功后写入本地缓存。

仓库中已包含默认示例股票的缓存数据：

```text
data_cache/AAPL_history.csv
data_cache/TSLA_history.csv
```

典型调用方式如下：

```python
import yfinance as yf

data = yf.Ticker("AAPL").history(period="1d")
current_price = data["Close"].iloc[-1]
```

`history()` 返回的是 `pandas.DataFrame`，常见字段包括：

```text
Open, High, Low, Close, Volume, Dividends, Stock Splits
```

其中项目主要使用 `Close` 作为标的资产价格。

如果需要刷新某只股票的缓存，可以删除对应的 `data_cache/{TICKER}_history.csv` 文件，然后重新运行应用；下一次成功请求 Yahoo Finance 后会重新生成缓存。

需要注意的是，`yfinance` 是第三方开源库，不是 Yahoo 官方 API。它适合个人学习、研究和课程项目使用；如果要用于商业产品、批量抓取或对外提供行情数据，应使用正式授权的数据服务。

## 依赖版本

核心依赖记录在 `requirements.txt` 中：

```text
streamlit
matplotlib
numpy
pandas
scipy
yfinance
```

当前项目已调整为可在 Python 3.12 环境下运行。

## 演示

### Black-Scholes 模型

![Black-Scholes 演示](media/Black_Scholes_Model.gif)

### 蒙特卡洛期权定价

![蒙特卡洛演示](media/Monte_Carlo_Option_Pricing.gif)

### 二叉树模型

![二叉树演示](media/Binomial_Model.gif)
