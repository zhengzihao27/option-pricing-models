import streamlit as st
from enum import Enum
from datetime import datetime, timedelta
from option_pricing import BlackScholesModel, MonteCarloPricing, BinomialTreeModel, Ticker

class OPTION_PRICING_MODEL(Enum):
    BLACK_SCHOLES = 'Black Scholes Model'
    MONTE_CARLO = 'Monte Carlo Simulation'
    BINOMIAL = 'Binomial Model'

CACHE_TTL_SECONDS = 60 * 60

@st.cache_data(ttl=CACHE_TTL_SECONDS)
def fetch_historical_data(ticker):
    return Ticker.get_historical_data(ticker)

@st.cache_data(ttl=CACHE_TTL_SECONDS)
def fetch_current_price(ticker):
    data = fetch_historical_data(ticker)
    close_prices = data["Close"].dropna()
    if close_prices.empty:
        raise ValueError(f"No close price returned for {ticker}")
    return close_prices.iloc[-1]

def get_historical_data(ticker):
    ticker = ticker.strip().upper()
    try:
        return fetch_historical_data(ticker)
    except Exception as e:
        st.error(f"Error fetching data for {ticker}: {str(e)}")
        return None

def get_current_price(ticker):
    ticker = ticker.strip().upper()
    try:
        return fetch_current_price(ticker)
    except Exception as e:
        st.error(f"Error fetching current price for {ticker}: {str(e)}")
        return None

# 兼容旧版 Streamlit 中 st.pyplot() 的弃用提示配置。
try:
    st.set_option('deprecation.showPyplotGlobalUse', False)
except st.errors.StreamlitAPIException:
    pass

# 主标题
st.title('Option pricing')

# 用户在侧边栏选择的定价模型
pricing_method = st.sidebar.radio('Please select option pricing method', options=[model.value for model in OPTION_PRICING_MODEL])

# 显示当前选择的定价模型
st.subheader(f'Pricing method: {pricing_method}')

if pricing_method == OPTION_PRICING_MODEL.BLACK_SCHOLES.value:
    # Black-Scholes 模型参数
    ticker = st.text_input('Ticker symbol', 'AAPL')
    st.caption("Enter the stock symbol (e.g., AAPL for Apple Inc.)")

    # 获取当前价格
    current_price = get_current_price(ticker)
    
    if current_price is not None:
        st.write(f"Current price of {ticker}: ${current_price:.2f}")
        
        # 根据当前价格设置默认值、最小值和最大值
        default_strike = round(current_price, 2)
        min_strike = max(0.1, round(current_price * 0.5, 2))
        max_strike = round(current_price * 2, 2)
        
        strike_price = st.number_input('Strike price', 
                                       min_value=min_strike, 
                                       max_value=max_strike, 
                                       value=default_strike, 
                                       step=0.01)
        st.caption(f"The price at which the option can be exercised. Range: ${min_strike:.2f} to ${max_strike:.2f}")
    else:
        strike_price = st.number_input('Strike price', min_value=0.01, value=100.0, step=0.01)
        st.caption("The price at which the option can be exercised. Enter a valid ticker to see a suggested range.")

    risk_free_rate = st.slider('Risk-free rate (%)', 0, 100, 10)
    st.caption("The theoretical rate of return of an investment with zero risk. Usually based on government bonds. 0% means no risk-free return, 100% means doubling your money risk-free (unrealistic).")

    sigma = st.slider('Sigma (Volatility) (%)', 0, 100, 20)
    st.caption("A measure of the stock's price variability. Higher values indicate more volatile stocks. 0% means no volatility (unrealistic), 100% means extremely volatile.")

    exercise_date = st.date_input('Exercise date', min_value=datetime.today() + timedelta(days=1), value=datetime.today() + timedelta(days=365))
    st.caption("The date when the option can be exercised")
    
    if st.button(f'Calculate option price for {ticker}'):
        try:
            with st.spinner('Fetching data...'):
                data = get_historical_data(ticker)

            if data is not None and not data.empty:
                st.write("Data fetched successfully:")
                st.write(data.tail())
                
                fig = Ticker.plot_data(data, ticker, 'Close')
                st.pyplot(fig)

                spot_price = Ticker.get_last_price(data, 'Close')
                risk_free_rate = risk_free_rate / 100
                sigma = sigma / 100
                days_to_maturity = (exercise_date - datetime.now().date()).days

                BSM = BlackScholesModel(spot_price, strike_price, days_to_maturity, risk_free_rate, sigma)
                call_option_price = BSM.calculate_option_price('Call Option')
                put_option_price = BSM.calculate_option_price('Put Option')

                st.subheader(f'Call option price: {call_option_price:.2f}')
                st.subheader(f'Put option price: {put_option_price:.2f}')
            else:
                st.error("Unable to proceed with calculations due to data fetching error.")
        except Exception as e:
            st.error(f"Error during calculation: {str(e)}")
    else:
        st.info("Click 'Calculate option price' to see results.")

elif pricing_method == OPTION_PRICING_MODEL.MONTE_CARLO.value:
    # 蒙特卡洛模拟参数
    ticker = st.text_input('Ticker symbol', 'AAPL')
    st.caption("Enter the stock symbol (e.g., AAPL for Apple Inc.)")

    # 获取当前价格
    current_price = get_current_price(ticker)
    
    if current_price is not None:
        st.write(f"Current price of {ticker}: ${current_price:.2f}")
        
        # 根据当前价格设置默认值、最小值和最大值
        default_strike = round(current_price, 2)
        min_strike = max(0.1, round(current_price * 0.5, 2))
        max_strike = round(current_price * 2, 2)
        
        strike_price = st.number_input('Strike price', 
                                       min_value=min_strike, 
                                       max_value=max_strike, 
                                       value=default_strike, 
                                       step=0.01)
        st.caption(f"The price at which the option can be exercised. Range: ${min_strike:.2f} to ${max_strike:.2f}")
    else:
        strike_price = st.number_input('Strike price', min_value=0.01, value=100.0, step=0.01)
        st.caption("The price at which the option can be exercised. Enter a valid ticker to see a suggested range.")

    risk_free_rate = st.slider('Risk-free rate (%)', 0, 100, 10)
    st.caption("The theoretical rate of return of an investment with zero risk. Usually based on government bonds. 0% means no risk-free return, 100% means doubling your money risk-free (unrealistic).")

    sigma = st.slider('Sigma (Volatility) (%)', 0, 100, 20)
    st.caption("A measure of the stock's price variability. Higher values indicate more volatile stocks. 0% means no volatility (unrealistic), 100% means extremely volatile.")

    exercise_date = st.date_input('Exercise date', min_value=datetime.today() + timedelta(days=1), value=datetime.today() + timedelta(days=365))
    st.caption("The date when the option can be exercised")

    number_of_simulations = st.slider('Number of simulations', 100, 100000, 10000)
    st.caption("The number of price paths to simulate. More simulations increase accuracy but take longer to compute.")

    num_of_movements = st.slider('Number of price movement simulations to be visualized ', 0, int(number_of_simulations/10), 100)
    st.caption("The number of simulated price paths to display on the graph")

    if st.button(f'Calculate option price for {ticker}'):
        try:
            with st.spinner('Fetching data...'):
                data = get_historical_data(ticker)
            
            if data is not None and not data.empty:
                st.write("Data fetched successfully:")
                st.write(data.tail())
                
                fig = Ticker.plot_data(data, ticker, 'Close')
                st.pyplot(fig)

                spot_price = Ticker.get_last_price(data, 'Close')
                risk_free_rate = risk_free_rate / 100
                sigma = sigma / 100
                days_to_maturity = (exercise_date - datetime.now().date()).days

                MC = MonteCarloPricing(spot_price, strike_price, days_to_maturity, risk_free_rate, sigma, number_of_simulations)
                MC.simulate_prices()

                fig = MC.plot_simulation_results(num_of_movements)
                st.pyplot(fig)

                call_option_price = MC.calculate_option_price('Call Option')
                put_option_price = MC.calculate_option_price('Put Option')

                st.subheader(f'Call option price: {call_option_price:.2f}')
                st.subheader(f'Put option price: {put_option_price:.2f}')
            else:
                st.error("Unable to proceed with calculations due to data fetching error.")
        except Exception as e:
            st.error(f"Error during calculation: {str(e)}")
    else:
        st.info("Click 'Calculate option price' to see results.")

elif pricing_method == OPTION_PRICING_MODEL.BINOMIAL.value:
    # 二叉树模型参数
    ticker = st.text_input('Ticker symbol', 'AAPL')
    st.caption("Enter the stock symbol (e.g., AAPL for Apple Inc.)")

    # 获取当前价格
    current_price = get_current_price(ticker)
    
    if current_price is not None:
        st.write(f"Current price of {ticker}: ${current_price:.2f}")
        
        # 根据当前价格设置默认值、最小值和最大值
        default_strike = round(current_price, 2)
        min_strike = max(0.1, round(current_price * 0.5, 2))
        max_strike = round(current_price * 2, 2)
        
        strike_price = st.number_input('Strike price', 
                                       min_value=min_strike, 
                                       max_value=max_strike, 
                                       value=default_strike, 
                                       step=0.01)
        st.caption(f"The price at which the option can be exercised. Range: ${min_strike:.2f} to ${max_strike:.2f}")
    else:
        strike_price = st.number_input('Strike price', min_value=0.01, value=100.0, step=0.01)
        st.caption("The price at which the option can be exercised. Enter a valid ticker to see a suggested range.")

    risk_free_rate = st.slider('Risk-free rate (%)', 0, 100, 10)
    st.caption("The theoretical rate of return of an investment with zero risk. Usually based on government bonds. 0% means no risk-free return, 100% means doubling your money risk-free (unrealistic).")

    sigma = st.slider('Sigma (Volatility) (%)', 0, 100, 20)
    st.caption("A measure of the stock's price variability. Higher values indicate more volatile stocks. 0% means no volatility (unrealistic), 100% means extremely volatile.")

    exercise_date = st.date_input('Exercise date', min_value=datetime.today() + timedelta(days=1), value=datetime.today() + timedelta(days=365))
    st.caption("The date when the option can be exercised")

    number_of_time_steps = st.slider('Number of time steps', 5000, 100000, 15000)
    st.caption("The number of periods in the binomial tree. More steps increase accuracy but take longer to compute.")

    if st.button(f'Calculate option price for {ticker}'):
        try:
            with st.spinner('Fetching data...'):
                data = get_historical_data(ticker)
            
            if data is not None and not data.empty:
                st.write("Data fetched successfully:")
                st.write(data.tail())
                
                fig = Ticker.plot_data(data, ticker, 'Close')
                st.pyplot(fig)

                spot_price = Ticker.get_last_price(data, 'Close')
                risk_free_rate = risk_free_rate / 100
                sigma = sigma / 100
                days_to_maturity = (exercise_date - datetime.now().date()).days

                BOPM = BinomialTreeModel(spot_price, strike_price, days_to_maturity, risk_free_rate, sigma, number_of_time_steps)
                call_option_price = BOPM.calculate_option_price('Call Option')
                put_option_price = BOPM.calculate_option_price('Put Option')

                st.subheader(f'Call option price: {call_option_price:.2f}')
                st.subheader(f'Put option price: {put_option_price:.2f}')
            else:
                st.error("Unable to proceed with calculations due to data fetching error.")
        except Exception as e:
            st.error(f"Error during calculation: {str(e)}")
    else:
        st.info("Click 'Calculate option price' to see results.")
