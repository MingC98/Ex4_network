"""Perform credit card calculations."""
from argparse import ArgumentParser
import sys
# replace this comment with your implementation of get_min_payment(),
# interest_charged(), remaining_payments(), and main()
def get_min_payment(balance,fees):
    """
    Determine the min payment of credit card
    Args: balance (float),the total amount of balance
    fees(float): the fees associated with credit card
    Return: min_payment(float) The minimun amount of payment
    """
    percent_m = 0.02 #Default percentage of balance needs to be paid
    min_payment = balance*percent_m + fees
    if min_payment < 25:
        min_payment = 25
    return min_payment

def interest_charged(balance,apr):
    """
    Determine the amount of interest in next payment
    Args: balance (float),the total amount of balance
    apr(int (1 - 100)): the fees associated with credit card
    Return: i(float) The minimun amount of payment(float)
    """
    a=apr/100 #Apr represent by float
    d=30 #Number of days in billing cycle
    y=365 # Number of days in a year
    i = (a/y)*balance*d
    return i
    
def remaining_payments(balance,apr,targetamount,credit_line,fees):
    """
    Determine the remaining payment
    
    Args: balance (float),the total amount of balance
    apr(int (1 - 100)): the fees associated with credit card
    targetamount(int) : the amount user wants to pay
    credit_line(int): The maximun amount of balance allowed
    fees(float): the fees associated with credit card
    
    Return: r_payment(float) The amount required to be paid
    """
    # Counters for credit line and total payment time.
    t_count = 0
    f_count = 0
    s_count = 0
    p_count = 0
    #Percent of credit Line
    t_line = 0.25*credit_line
    f_line = 0.5*credit_line
    s_line = 0.75*credit_line
    while balance > 0:
        if targetamount == None:
            targetamount = get_min_payment(balance,fees)
        interest = interest_charged(balance, apr)
        r_amount = targetamount - interest # The amount goes towards balance
        if r_amount < 0:
            print("The card balance cannot be paid off")
            return
        balance = balance - r_amount
        if balance > s_line:
            s_count += 1
        if balance > f_line:
            f_count += 1
        if balance > t_line:
            t_count += 1
        p_count += 1
    return p_count,t_count,f_count,s_count
    
def main(balance,apr,targetamount,credit_line,fees):
    """
    Set up the payment plan
    Args: balance (float),the total amount of balance
    apr(int (1 - 100)): the fees associated with credit card
    targetamount(int) : the amount user wants to pay
    credit_line(int): The maximun amount of balance allowed
    fees(float): the fees associated with credit card
    """
    r_min_payment = get_min_payment(balance,fees)
    print("Recommanded minimum payment is: $" + str(r_min_payment))
    pays_minimum = False
    if targetamount == None:
        pays_minimum = True
    if(pays_minimum):
        num_payment = remaining_payments (balance,apr,r_min_payment,credit_line,fees)
        print(f"If you pay the minimum payments each month, you will pay off the credit card in {num_payment[0]} payments")
        r_string = f"You will spend a total of {num_payment[1]} months over 25% credit line\nYou will spend a total of {num_payment[2]} months over 50% credit line\nYou will spend a total of {num_payment[3]} months over 75% credit line"
    else:
        if (targetamount < r_min_payment):
            print("Your  target payment  is  less  than  the  minimum  payment  for  this  credit  card")
            return
        num_payment = remaining_payments (balance,apr,targetamount,credit_line,fees)
        print(f"if you make payments of ${targetamount}, you will pay off the credit card in {num_payment[0]} payments")
        r_string = f"You will spend a total of {num_payment[1]} months over 25% credit line\nYou will spend a total of {num_payment[2]} months over 50% credit line\nYou will spend a total of {num_payment[3]} months over 75% credit line"
    return r_string
    
    
def parse_args(args_list):
    """Takes a list of strings from the command prompt and passes them through as
    arguments
    Args:
        args_list (list) : the list of strings from the command prompt
    Returns:
        args (ArgumentParser)
    """
    parser = ArgumentParser()
    parser.add_argument('balance_amount', type = float, help = 'The total amount of balance left on the credit account')
    parser.add_argument('apr', type = int, help = 'The annual APR, should be an int between 1 and 100')
    parser.add_argument('credit_line', type = int, help = 'The maximum amount of balance allowed on the credit line.')
    parser.add_argument('--payment', type = int, default = None, help = 'The amount the user wants to pay per payment, should be a positive number')
    parser.add_argument('--fees', type = float, default = 0, help = 'The fees that are applied monthly.')
    # parse and validate arguments
    args = parser.parse_args(args_list)
    if args.balance_amount < 0:
        raise ValueError("balance amount must be positive")
    if not 0 <= args.apr <= 100:
        raise ValueError("APR must be between 0 and 100")
    if args.credit_line < 1:
        raise ValueError("credit line must be positive")
    if args.payment is not None and args.payment < 0:
        raise ValueError("number of payments per year must be positive")
    if args.fees < 0:
        raise ValueError("fees must be positive")
    return args
if __name__ == "__main__":
    try:
        arguments = parse_args(sys.argv[1:])
    except ValueError as e:
        sys.exit(str(e))
    print(main(arguments.balance_amount, arguments.apr, credit_line = arguments.credit_line, targetamount = arguments.payment, fees = arguments.fees))
