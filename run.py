import gspread
from google.oauth2.service_account import Credentials
from pprint import pprint

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file("creds.json")
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open("love_sandwiches")

# sales = SHEET.worksheet('sales')

# data = sales.get_all_values()

# print(data)

def get_sales_data():
    """
    get sales figures from the user via terminal
    
    """
    while True:
        print("Please enter sales data from your last market")
        print("Data should be six numbers separated by commas")
        print("Example: 10, 20, 30, 40, 50, 60 \n")

        data_str = input("Enter your data here:")

        sales_data = data_str.split(',')
        
        if validate_data(sales_data):
            print("Data is valid!")
            break

    return sales_data


def validate_data(values):
    """ 
    function checks that 6 numbers have been entered, each separated by a comma
    values must be able to converted to integers.  Will raise ValueError if strings can't be converted to int
    """
    try:
        [int(value) for value in values]
        if len(values) != 6:
            raise ValueError(
                f'Exactly 6 values required, you provided {len(values)}'
            )
    except ValueError as e:
        print(f'Invalid data: {e}, please try again.\n')
        return False
    return True

def update_spreadsheet(data, sheet):
    """
    update worksheet with the name 'sheet' by adding new row with the list of data provided
    """
    print(f'Updating {sheet} worksheet... \n')
    worksheet = SHEET.worksheet(sheet)
    worksheet.append_row(data)
    print(f'{sheet} worksheet updated successfully.\n')

def calculate_surplus_data(sales_row):
    """
    Compare sales with stock and calculate the surplus of each type
    The surplus is defined as the sales figure subtracted from the stock:
    + values indicate waste
    - values indicate extra sandwiches had to be made on the day
    """
    print("Calculating surplus data...\n")
    stock = SHEET.worksheet("stock").get_all_values()
    stock_row = stock[-1]

    surplus_data = []
    for stock, sales in zip(stock_row, sales_row):
        surplus = int(stock) - sales
        surplus_data.append(surplus)
    return surplus_data

def get_last_five_entries_sales():
    """
    Collects columns of data from the sales worksheet, collecting
    the last 5 entries for each sandwich and returns the sate as
    a list of lists
    """
    sales = SHEET.worksheet("sales")
    columns = []

    for ind in range(1,7):
        column = sales.col_values(ind)
        columns.append(column[-5:])
    
    return columns

def main():
    """ run all program functions"""
    data = get_sales_data()
    sales_data = [int(num) for num in data]
    update_spreadsheet(sales_data, "sales")
    new_surplus_data = calculate_surplus_data(sales_data)
    update_spreadsheet(new_surplus_data, "surplus")

print("Welcome to Love Sandwiches data automation")
#main()

sales_columns = get_last_five_entries_sales()