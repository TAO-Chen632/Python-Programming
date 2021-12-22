# Functions to implement our trading strategy.
import numpy as np
import trading.process as process
import trading.indicators as indicators

def random(stock_prices_data, period = 7, amount = 5000, fees = 20, ledger = 'ledger_random.txt'):
    '''
    Randomly decide, every period, which stocks to purchase,
    do nothing, or sell (with equal probability).
    Spend a maximum of amount on every purchase.

    Input:
        stock_prices_data (ndarray): the stock price data
        period (int, default 7): how often we buy/sell (days)
        amount (float, default 5000): how much we spend on each purchase (must cover fees)
        fees (float, default 20): transaction fees
        ledger (str, default 'ledger_random.txt'): path to the ledger file

    Output: None
    '''
    # Record the shape of the stock price data
    (total_period, stock) = stock_prices_data.shape
    # Create the portfolio
    portfolio = process.create_portfolio([amount] * stock, stock_prices_data[0], fees, ledger)
    # Set the random number generator
    rng = np.random.default_rng()
    # The decision is made completely randomly, which means all kinds of decisions have equal chance.
    chance = [1/3, 1/3, 1/3]
    # Loop over a `range(1, total_period)` and the interval is `period`
    for day in range(1, total_period, period):
        # Get today's stock prices
        stock_price_today = stock_prices_data[day]
        # Clear the stock whose price is NaN in the portfolio, which means when a company is bankrupt,
        # we discard all the stocks of this company, because they are already worthless.
        portfolio = np.array(portfolio)
        portfolio[np.isnan(stock_price_today)] = 0
        portfolio = list(portfolio)
        # The period during which today is not the last day of making decisions
        if day + period < total_period:
            # Decisions are made on the stocks whose prices are not NaN.
            for i in np.where(np.isnan(stock_price_today) == False)[0]:
                # Decisions are made randomly
                strategy = rng.choice([0, 1, 2], p = chance)
                if strategy == 0:
                    process.buy(day, i, amount, stock_price_today, fees, portfolio, ledger)
                elif strategy == 1:
                    pass
                else:
                    process.sell(day, i, stock_price_today, fees, portfolio, ledger)
        # In the last day, sell all remaining stocks
        else:
            for i in np.where(np.isnan(stock_price_today) == False)[0]:
                process.sell(day, i, stock_price_today, fees, portfolio, ledger)


def crossing_averages(stock_prices_data, n = 200, m = 50, amount = 5000, fees = 20, ledger = 'ledger_cro_aver.txt'):
    '''
    This function is the implementation of the strategy of crossing averages. It decides which stocks to purchase,
    do nothing or to sell in every period according to the crossing points between the slow moving average (SMA)
    and the fast moving average (FMA). It spends a maximum of amount on every purchase.

    Input:
        stock_prices_data (ndarray): the stock price data
        n (int, default 200): the period of the slow moving average (SMA)
        m (int, default 50): the period of the fast moving average (FMA)
        amount (float, default 5000): how much we spend on each purchase (must cover fees)
        fees (float, default 20): transaction fees
        ledger (str, default 'ledger_cro_aver.txt'): path to the ledger file

    Output: None
    '''
    # Record the shape of the stock price data
    (total_period, stock) = stock_prices_data.shape
    # Create the portfolio
    portfolio = process.create_portfolio([amount] * stock, stock_prices_data[0], fees, ledger)
    # Initialize the variables SMA and FMA
    SMA = np.zeros(shape = stock_prices_data.shape)
    FMA = np.zeros(shape = stock_prices_data.shape)
    # Calculate the SMA and FMA of all types of stocks
    for i in range(stock):
        SMA[ : , i] = indicators.moving_average(stock_prices_data[ : , i], n = n)
        FMA[ : , i] = indicators.moving_average(stock_prices_data[ : , i], n = m)
    # The difference between SMA and FMA
    difference = FMA - SMA
    # Loop over a `range(1, total_period)`
    for day in range(1, total_period):
        # Get today's stock prices
        stock_price_today = stock_prices_data[day]
        # Clear the stock whose price is NaN in the portfolio, which means when a company is bankrupt,
        # we discard all the stocks of this company, because they are already worthless.
        portfolio = np.array(portfolio)
        portfolio[np.isnan(stock_price_today)] = 0
        portfolio = list(portfolio)
        # The period during which today is not the last day of making decisions
        if day < total_period - 1:
            # Decisions are made on the stocks whose prices are not NaN.
            for i in np.where(np.isnan(stock_price_today) == False)[0]:
                # Find the crossing points between the SMA and the FMA to make buying or selling decisions
                if difference[day - 1, i] < 0 and difference[day, i] > 0:
                    process.buy(day, i, amount, stock_price_today, fees, portfolio, ledger)
                elif difference[day - 1, i] > 0 and difference[day, i] < 0:
                    process.sell(day, i, stock_price_today, fees, portfolio, ledger)
        # In the last day, sell all remaining stocks
        else:
            for i in np.where(np.isnan(stock_price_today) == False)[0]:
                    process.sell(day, i, stock_price_today, fees, portfolio, ledger)

def momentum(stock_prices_data, osc_type = 'stochastic', n = 7, threshold = [0.25, 0.75], cool_down = 7, amount = 5000, fees = 20, ledger = 'ledger_momentum.txt'):
    '''
    This function is the implementation of the strategy of momentum trading using oscillators. It decides
    which stocks to purchase, do nothing or to sell in every period according to the level of a oscillator.
    It spends a maximum of amount on every purchase.

    Input:
        stock_prices_data (ndarray): the stock price data
        osc_type (str, default 'stochastic'): either 'stochastic' or 'RSI' to choose an oscillator
        n (int, default 7): the period of calculating the oscillator
        threshold (list, default [0.25, 0.75]): the thresholds to make buying and selling decisions
        cool_down (int, default 7): the cool down period after the purchase of each stock
        amount (float, default 5000): how much we spend on each purchase (must cover fees)
        fees (float, default 20): transaction fees
        ledger (str, default 'ledger_momentum.txt'): path to the ledger file

    Output: None
    '''
    # Record the shape of the stock price data
    (total_period, stock) = stock_prices_data.shape
    # Create the portfolio
    portfolio = process.create_portfolio([amount] * stock, stock_prices_data[0], fees, ledger)
    # The date of the purchase of every stock is recorded by the list `record`
    record = [0] * stock
    # Initialize the oscillator
    oscillator = np.zeros(shape = stock_prices_data.shape)
    # Calculate the oscillator of all types of stocks
    for i in range(stock):
        oscillator[ : , i] = indicators.oscillator(stock_prices_data[ : , i], n = n, osc_type = osc_type)
    # Loop over a `range(1, total_period)`
    for day in range(1, total_period):
        # Get today's stock prices
        stock_price_today = stock_prices_data[day]
        # Clear the stock whose price is NaN in the portfolio, which means when a company is bankrupt,
        # we discard all the stocks of this company, because they are already worthless.
        portfolio = np.array(portfolio)
        portfolio[np.isnan(stock_price_today)] = 0
        portfolio = list(portfolio)
        # The period during which today is not the last day of making decisions
        if day < total_period - 1:
            # Decisions are made on the stocks whose prices are not NaN.
            for i in np.where(np.isnan(stock_price_today) == False)[0]:
                # The buying and selling decisions are made depending on the low and high threshold.
                # The cool down period is utilized after each purchase but it is not needed after each sale.
                if oscillator[day, i] < threshold[0] and (record[i] == 0 or day - record[i] > cool_down):
                    process.buy(day, i, amount, stock_price_today, fees, portfolio, ledger)
                    record[i] = day
                elif oscillator[day, i] > threshold[1]:
                    process.sell(day, i, stock_price_today, fees, portfolio, ledger)
                    record[i] = day
        # In the last day, sell all remaining stocks
        else:
            for i in np.where(np.isnan(stock_price_today) == False)[0]:
                    process.sell(day, i, stock_price_today, fees, portfolio, ledger)
