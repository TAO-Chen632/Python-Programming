import numpy as np

def moving_average(stock_price, n = 7, weights = []):
    '''
    Calculates the n-day (possibly weighted) moving average for a given stock over time.

    Input:
        stock_price (ndarray): single column with the share prices over time for one stock,
            up to the current day.
        n (int, default 7): period of the moving average (in days).
        weights (list, default []): must be of length n if specified. Indicates the weights
            to use for the weighted average. If empty, return a non-weighted average.

    Output:
        ma (ndarray): the n-day (possibly weighted) moving average of the share price over time.

    Remark:
        1. For the first n-1 days, I decide to calculate the (weighted) average of the stock prices of
        the first k days (1 <= k <= n-1) to be the value of the (weighted) moving average of the day k.
        That is, in terms of the day k in the first n-1 days, the period `n` is automatically adjusted
        to k. I think this approach is sensible, because it does not reduce the amount of the data
        finally returned and it keeps the method of calculation as continuous as possible.
        2. The variable `stock_price` here is treated as a one-dimensional numpy array.
        3. When the number of stock prices data `m` is less than `n`, the length of the period `n` is
        automatically adjusted to `m` day(s) to adapt to the situations that there are very few data
        available or the length of the period `n` is very large.
        4. The sum of the components in the list `weights` need not equal to 1. The proportion of each
        component in this list will be calculated later.
    '''
    # Initialize some parameters or variables
    m = len(stock_price)
    p = len(weights)
    ma = np.array([])
    # The situation of calculating the moving average that is not weighted
    if p == 0:
        # The situation that the number of stock prices data `m` is larger than or equal to n
        if m >= n:
            # For the first n-1 days in the data, the value of the moving average of the day k
            # (1 <= k <= n-1) is set to be the average of the stock prices of the first k days.
            for i in range(n - 1):
                ma_term_i = np.mean(stock_price[ : i + 1])
                ma = np.append(ma, ma_term_i)
            # From the day n later, the value of the moving average is calculated normally, which
            # is the average of the stock prices of the previous n days up to the current day.
            for i in range(n - 1, m):
                ma_term_i = np.mean(stock_price[i - n + 1 : i + 1])
                ma = np.append(ma, ma_term_i)
            return ma
        else:
            # When the number of stock prices data `m` is less than n, the length of the period `n`
            # is automatically adjusted to `m` day(s).
            for i in range(m):
                ma_term_i = np.mean(stock_price[ : i + 1])
                ma = np.append(ma, ma_term_i)
            return ma
    # The situation of calculating the weighted moving average
    elif p == n:
        # The situation that the number of stock prices data `m` is larger than or equal to `n`
        if m >= n:
            # The idea here is similar. For the first n-1 days in the data, the value of the weighted moving average
            # of the day k (1 <= k <= n-1) is calculated as the weighted average of the stock prices of the first k
            # days and the last k components of the list `weights` are used.
            for i in range(n - 1):
                ma_term_i = np.dot(stock_price[ : i + 1], weights[n - i - 1 : ]) / np.sum(weights[n - i - 1 : ])
                ma = np.append(ma, ma_term_i)
            # From the day n later, the value of the weighted moving average is calculated normally, which
            # is the weighted average of the stock prices of the previous n days up to the current day.
            for i in range(n - 1, m):
                # The `np.dot()` and `np.sum()` functions are used here and the weighted average is calculated.
                ma_term_i = np.dot(stock_price[i - n + 1 : i + 1], weights) / np.sum(weights)
                ma = np.append(ma, ma_term_i)
            return ma
        else:
            # When the number of stock prices data `m` is less than `n`, the length of the period `n` is
            # automatically adjusted to `m` day(s).
            for i in range(m):
                ma_term_i = np.dot(stock_price[ : i + 1], weights[m - i - 1 : ]) / np.sum(weights[m - i - 1 : ])
                ma = np.append(ma, ma_term_i)
            return ma
    # If the length of the list `weights` is not equal to the length of the period `n`, stop the function and throw
    # an appropriate error message.
    else:
        print('The length of the weights must coincide with the length n of the period.')


def oscillator(stock_price, n = 7, osc_type = 'stochastic'):
    '''
    Calculates the level of the stochastic or RSI oscillator with a period of n days.

    Input:
        stock_price (ndarray): single column with the share prices over time for one stock,
            up to the current day.
        n (int, default 7): period of the moving average (in days).
        osc_type (str, default 'stochastic'): either 'stochastic' or 'RSI' to choose an oscillator.

    Output:
        osc (ndarray): the oscillator level with period $n$ for the stock over time.

    Remark:
        1. For the first n-1 days, I decide to calculate different types of oscillators using the stock
        prices of the first k days (1 <= k <= n-1). That is, in terms of the day k in the first n-1 days,
        the period variable `n` is automatically adjusted to k. I think this approach is sensible, because
        it does not reduce the amount of the data finally returned and it keeps the method of calculation
        as continuous as possible.
        2. The variable `stock_price` here is treated as a one-dimensional numpy array.
        3. When the number of stock prices data `m` is less than `n`, the length of the period `n` is
        automatically adjusted to `m` day(s) to adapt to the situations that there are very few data
        available or the length of the period `n` is very large.
    '''
    # Initialize some parameters or variables
    m = len(stock_price)
    osc = np.array([])
    # The situation of the stochastic oscillator
    if osc_type == 'stochastic':
        # The situation that the number of stock prices data `m` is larger than or equal to `n`
        if m >= n:
            # For the first n-1 days in the data, the value of the stochastic oscillator on the
            # day k (1 <= k <= n-1) is calculated using the stock prices of the first k days.
            for i in range(n - 1):
                highest_price = np.max(stock_price[ : i + 1])
                lowest_price = np.min(stock_price[ : i + 1])
                delta = stock_price[i] - lowest_price
                delta_max = highest_price - lowest_price
                if delta_max == 0:
                    osc = np.append(osc, np.nan)
                else:
                    osc = np.append(osc, delta / delta_max)
            # From the day n later, the value of the stochastic oscillator is calculated normally.
            for i in range(n - 1, m):
                # The highest and lowest prices and the variables `delta` and `delta_max`
                # are calculated as required.
                highest_price = np.max(stock_price[i - n + 1 : i + 1])
                lowest_price = np.min(stock_price[i - n + 1 : i + 1])
                delta = stock_price[i] - lowest_price
                delta_max = highest_price - lowest_price
                # If delta_max equals zero, which means the stock price in this period remains
                # constant, the stochastic oscillator does not exist, and so I set it be NaN.
                # In other cases, it will be the usual value `delta / delta_max`.
                if delta_max == 0:
                    osc = np.append(osc, np.nan)
                else:
                    osc = np.append(osc, delta / delta_max)
            return osc
        else:
            # When the number of stock prices data `m` is less than `n`, the length of the period `n` is
            # automatically adjusted to `m` day(s). The calculation process in this case is similar.
            for i in range(m):
                highest_price = np.max(stock_price[ : i + 1])
                lowest_price = np.min(stock_price[ : i + 1])
                delta = stock_price[i] - lowest_price
                delta_max = highest_price - lowest_price
                if delta_max == 0:
                    osc = np.append(osc, np.nan)
                else:
                    osc = np.append(osc, delta / delta_max)
            return osc
    # The situation of the relative strength index (RSI) oscillator
    if osc_type == 'RSI':
        # Firstly, calculate all the price differences on consecutive days over all the days.
        stock_price_diff = stock_price[1 : ] - stock_price[ : -1]
        # The price difference on the initial day (day 0) is regarded as the stock price itself on that day.
        stock_price_diff = np.concatenate([[stock_price[0]], stock_price_diff])
        # The situation that the number of stock prices data `m` is larger than or equal to `n`
        if m >= n:
            # For the first n-1 days in the data, the value of the RSI oscillator on the day k (1 <= k <= n-1)
            # is calculated using the stock price differences on consecutive days over the first k days.
            for i in range(n - 1):
                stock_price_diff_period = stock_price_diff[ : i + 1]
                sto_price_diff_peri_posi = stock_price_diff_period[stock_price_diff_period > 0]
                sto_price_diff_peri_nega = stock_price_diff_period[stock_price_diff_period < 0]
                if len(sto_price_diff_peri_posi) > 0 and len(sto_price_diff_peri_nega) > 0:
                    RS = np.mean(sto_price_diff_peri_posi) / np.mean(abs(sto_price_diff_peri_nega))
                    RSI = RS / (1 + RS)
                elif len(sto_price_diff_peri_posi) > 0 and len(sto_price_diff_peri_nega) == 0:
                    RSI = 1
                elif len(sto_price_diff_peri_posi) == 0 and len(sto_price_diff_peri_nega) > 0:
                    RSI = 0
                else:
                    RSI = np.nan
                osc = np.append(osc, RSI)
            # From the day n later, the value of the RSI oscillator is calculated normally.
            for i in range(n - 1, m):
                # Take the price differences on consecutive days over the past `n` days
                stock_price_diff_period = stock_price_diff[i - n + 1 : i + 1]
                # Separate the positive differences and the negative differences
                sto_price_diff_peri_posi = stock_price_diff_period[stock_price_diff_period > 0]
                sto_price_diff_peri_nega = stock_price_diff_period[stock_price_diff_period < 0]
                # Calculate the relative strength (RS) and the RSI
                if len(sto_price_diff_peri_posi) > 0 and len(sto_price_diff_peri_nega) > 0:
                    RS = np.mean(sto_price_diff_peri_posi) / np.mean(abs(sto_price_diff_peri_nega))
                    RSI = RS / (1 + RS)
                # RSI should equal to 1 if the stock price is constantly increasing.
                elif len(sto_price_diff_peri_posi) > 0 and len(sto_price_diff_peri_nega) == 0:
                    RSI = 1
                # RSI should equal to 0 if the stock price is constantly decreasing.
                elif len(sto_price_diff_peri_posi) == 0 and len(sto_price_diff_peri_nega) > 0:
                    RSI = 0
                # If the stock price keeps constant over the period, RSI should be NaN.
                else:
                    RSI = np.nan
                osc = np.append(osc, RSI)
            return osc
        else:
            # When the number of stock prices data `m` is less than `n`, the length of the period `n` is
            # automatically adjusted to `m` day(s). The calculation process in this case is similar.
            for i in range(m):
                stock_price_diff_period = stock_price_diff[ : i + 1]
                sto_price_diff_peri_posi = stock_price_diff_period[stock_price_diff_period > 0]
                sto_price_diff_peri_nega = stock_price_diff_period[stock_price_diff_period < 0]
                if len(sto_price_diff_peri_posi) > 0 and len(sto_price_diff_peri_nega) > 0:
                    RS = np.mean(sto_price_diff_peri_posi) / np.mean(abs(sto_price_diff_peri_nega))
                    RSI = RS / (1 + RS)
                elif len(sto_price_diff_peri_posi) > 0 and len(sto_price_diff_peri_nega) == 0:
                    RSI = 1
                elif len(sto_price_diff_peri_posi) == 0 and len(sto_price_diff_peri_nega) > 0:
                    RSI = 0
                else:
                    RSI = np.nan
                osc = np.append(osc, RSI)
            return osc
