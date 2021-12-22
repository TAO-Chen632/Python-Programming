# Evaluate performance.
import numpy as np
import matplotlib.pyplot as plt

def read_ledger(ledger_file, days = 1825, show = 'report'):
    '''
    Reads and reports useful information from `ledger_file`.

    Input:
        ledger_file (str): path to the ledger file
        days (int, default 1825 (5 years)): the total period of the transaction history
        show (str, default 'report'): either 'report' or 'return' to choose a way to
            display the result

    Output:
        result (tuple): a tuple of length 3 consisted of the total expenditure, the
            total income and the final net profit

    Remark:
        1. Firstly, I add the argument `days` whose default value is 1825 (five years) to this function.
        This argument represents the total period of the simulation which is of great importance in
        analyzing the ledger file, so I take it as an argument of the function.
        2. Furthermore, For the convenience of testing the strategies, I also add the argument `show` which
        controls the way to display the information of the simulation. If `show` equals to 'report', the
        overall information of the simulation will be displayed on the screen and the plot of the amount of
        money that we had over time will be produced. On the other hand, If `show` equals to 'return', the
        tuple `result` is returned in the end which carries the overall information of the ledger file.
    '''
    # Extract all the information from `ledger_file`
    ledger_content = []
    f = open(ledger_file, 'r')
    for line in f:
        ledger_content.append(line.strip('\n').split(','))
    f.close()
    # The total number of transactions performed
    total_number = len(ledger_content)
    # Initialize some variables
    amount_spent = 0
    amount_earned = 0
    amount_transaction = [0] * days
    type_transaction = [0, 0]
    stock = []
    # Loop over all the records in `ledger_file`
    for record in ledger_content:
        # Calculate the total amount spent and the total number of purchase
        if 'buy' in record:
            amount_spent += abs(eval(record[-1]))
            type_transaction[0] += 1
        # Calculate the total amount earned and the total number of sale
        if 'sell' in record:
            amount_earned += eval(record[-1])
            type_transaction[1] += 1
        # Keep a track of the net profit on each day
        amount_transaction[eval(record[1])] += eval(record[-1])
        # Keep a track of all the types of stocks that appear
        stock.append(eval(record[2]))
    # Calculate the overall profit or loss
    difference = amount_earned - amount_spent
    # Initialize the portfolio variable
    portfolio = [0] * (np.max(stock) + 1)
    # Calculate the state of the portfolio just before the last day
    for record in ledger_content:
        if eval(record[1]) == (days - 1):
            portfolio[eval(record[2])] = eval(record[3])
    # Calculate the amount of money that we had on each day
    for i in range(1, days):
        amount_transaction[i] += amount_transaction[i - 1]
    # If the way of showing the result is 'report', the overall information of the simulation will be displayed
    # on the screen and the plot of the amount of money that we had over time will be produced.
    if show == 'report':
        # Display the overall information of the simulation
        print('The summary of {} is shown as follows'.format(ledger_file))
        print('The total number of transactions performed is {}.'.format(total_number))
        print('The total numbers of purchase and sale are {} and {} respectively'.format(type_transaction[0], type_transaction[1]))
        print('The total amount spent and earned are {:.2f} and {:.2f} respectively.'.format(amount_spent, amount_earned))
        if difference >= 0:
            print('The overall profit is {:.2f}.'.format(difference))
        else:
            print('The overall loss is {:.2f}.'.format(abs(difference)))
        print('The state of the portfolio just before the last day is {}.'.format(portfolio))
        # Produce the plot of the amount of money that we had over time
        X = [i for i in range(days)]
        plt.figure()
        plt.plot(X, amount_transaction, 'r-')
        plt.show()
    # If the way of showing the result is 'return', the overall information about the simulation will be returned.
    if show == 'return':
        result = (amount_spent, amount_earned, difference)
        return result
