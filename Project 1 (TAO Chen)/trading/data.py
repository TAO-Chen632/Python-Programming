import numpy as np

def generate_stock_price(days, initial_price, volatility):
    '''
    Generates daily closing share prices for a company, for a given number of days.

    Inputs:
        days: a positive integer, which is the total number of days that we want to simulate.
        initial_price: a non-negative value, which is the price of the stock at the first day.
        volatility: a positive value, whcih represents the volatility of the stock.

    Output:
        stock_prices: a list with length of "days". It stores the predicted prices of the stock
        everyday in the duration of "days".
    '''
    # Set `stock_prices` to be a zero array with length days
    stock_prices = np.zeros(days)
    # Set `stock_prices` in row 0 to be `initial_price`
    stock_prices[0] = initial_price
    # Set `total_drift` to be a zero array with length days
    totalDrift= np.zeros(days)
    # Set the chance of whether news happens everyday to a list with length 2
    chance = [0.99, 0.01]
    # Set up the `default_rng` from Numpy
    rng = np.random.default_rng()
    # Loop over a `range(1, days)`
    for day in range(1, days):
        # Get the random normal increment
        inc = rng.normal(scale = volatility)
        # Add `stock_prices[day-1]` to `inc` to get `NewPriceToday`
        NewPriceToday = stock_prices[day-1] + inc
        # Make a function for the news
        def news(volatility):
            '''
            Simulate the news which may happen everyday
            '''
            # Calculate `m` and `drift`
            m = rng.normal(0, 2)
            drift = m * volatility
            # Randomly choose the duration
            duration = rng.integers(3, 14, endpoint = True)
            news_impact = np.zeros(duration)
            for i in range(duration):
                news_impact[i] = drift
            return news_impact
        # Judge whether news happens today
        news_today = rng.choice([0, 1], p = chance)
        # If news happens today, perform some operations
        if news_today:
            # Get the drift from the news
            drift_today = news(volatility)
            # Get the duration
            duration = len(drift_today)
            # Add the drift to the `totalDrift` of next days
            if day + duration <= days:
                totalDrift[day: day + duration] += drift_today
            else:
                totalDrift[day: ] += drift_today[ : (days - day)]
        # Add today's drift to today's price
        NewPriceToday += totalDrift[day]
        # Set `stock_prices[day]` to `NewPriceToday` or to NaN if it is 0 or negative
        if NewPriceToday <= 0:
            stock_prices[day] = np.nan
        else:
            stock_prices[day] = NewPriceToday
    return stock_prices


def get_data(method = 'read', initial_price = None, volatility = None):
    '''
    Generates or reads simulation data for one or more stocks over 5 years,
    given their initial share price and volatility.

    Input:
        method (str): either 'generate' or 'read' (default 'read').
            If method is 'generate', use generate_stock_price() to generate
                the data from scratch.
            If method is 'read', use Numpy's loadtxt() to read the data
                from the file stock_data_5y.txt.

        initial_price (list): list of initial prices for each stock (default None)
            If method is 'generate', use these initial prices to generate the data.
            If method is 'read', choose the column in stock_data_5y.txt with the closest
                starting price to each value in the list, and display an appropriate message.

        volatility (list): list of volatilities for each stock (default None).
            If method is 'generate', use these volatilities to generate the data.
            If method is 'read', choose the column in stock_data_5y.txt with the closest
                volatility to each value in the list, and display an appropriate message.

        If no arguments are specified, read price data from the whole file.

    Output:
        sim_data (ndarray): NumPy array with N columns, containing the price data
            for the required N stocks each day over 5 years.

    Examples:
        Returns an array with 2 columns:
            >>> get_data(method='generate', initial_price=[150, 250], volatility=[1.8, 3.2])

        Displays a message and returns None:
            >>> get_data(method='generate', initial_price=[150, 200])
            Please specify the volatility for each stock.

        Displays a message and returns None:
            >>> get_data(method='generate', volatility=[3])
            Please specify the initial price for each stock.

        Returns an array with 2 columns and displays a message:
            >>> get_data(method='read', initial_price=[210, 58])
            Found data with initial prices [210, 100] and volatilities [1.2, 3.4].

        Returns an array with 1 column and displays a message:
            >>> get_data(volatility=[5.1])
            Found data with initial prices [380] and volatilities [5.2].

        If method is 'read' and both initial_price and volatility are specified,
        volatility will be ignored (a message is displayed to indicate this):
            >>> get_data(initial_price=[210, 58], volatility=[5, 7])
            Found data with initial prices [210, 100] and volatilities [1.2, 3.4].
            Input argument volatility ignored.

        No arguments specified, all default values, returns price data for all stocks in the file:
            >>> get_data()
    '''
    if method == 'read':
        # Load the data from the file 'stock_data_5y.txt' using numpy's `loadtxt()`
        sim_data = np.loadtxt('stock_data_5y.txt', dtype = float, delimiter = ' ')
        # Read the initial prices and volatilities of stocks from the data
        sim_data_initial_price = sim_data[1, : ]
        sim_data_volatility = sim_data[0, : ]
        # Initialize the lists that will store the target initial prices and volatilities
        sim_initial_price = []
        sim_volatility = []
        index = []
        # Dividing the task into several situations, find the suitable initial prices or volatilities of the stocks
        # from the file and return the stock prices data corresponding to these initial prices and volatilities.
        if initial_price == None and volatility == None:
            sim_data = sim_data[1: , : ]
            return sim_data
        elif initial_price == None:
            for i in range(len(volatility)):
                k = np.argmin(abs(sim_data_volatility - volatility[i]))
                index.append(k)
                sim_initial_price.append(sim_data_initial_price[k])
                sim_volatility.append(sim_data_volatility[k])
            print("Found data with initial prices {} and volatilities {}."\
            .format(sim_initial_price, sim_volatility))
            sim_data = sim_data[1: , index]
            return sim_data
        else:
            for i in range(len(initial_price)):
                k = np.argmin(abs(sim_data_initial_price - initial_price[i]))
                index.append(k)
                sim_initial_price.append(sim_data_initial_price[k])
                sim_volatility.append(sim_data_volatility[k])
            if volatility == None:
                print("Found data with initial prices {} and volatilities {}."\
                .format(sim_initial_price, sim_volatility))
            else:
                print("Found data with initial prices {} and volatilities {}."\
                .format(sim_initial_price, sim_volatility) + "\n" + \
                "Input argument volatility ignored.")
            sim_data = sim_data[1: , index]
            return sim_data

    if method == "generate":
        # Firstly, exclude the situations that the initial prices and volatilities are not
        # input correctly and throw an appropriate message for each illegal input.
        if initial_price == None and volatility == None:
            print('Please specify the initial price and the volatility for each stock.')
        elif initial_price == None:
            print('Please specify the initial price for each stock.')
        elif volatility == None:
            print('Please specify the volatility for each stock.')
        else:
            # generate the simulation data for five years
            days = 1825
            # Initialize the variable of simulation data
            sim_data = np.zeros((days, 1))
            # Transfer the appropriate data to the ndarray `sim_data` and
            # finally return the data after some necessary adjustments
            for i in range(len(initial_price)):
                sim_data_column = generate_stock_price(days, initial_price[i], volatility[i])
                sim_data = np.hstack([sim_data, sim_data_column[ :, np.newaxis]])
            sim_data = sim_data[ : , 1: ]
            return sim_data