"""
This programm is an implementation of bank account management based on json files.
To generate HTML documentation for this module issue the command:

    pydoc -w bank_management

"""

import requests
import json
from decimal import Decimal
import time
import datetime
from pathlib import Path

class BankAccount:
    """
        The Class Bank Account will create an Bank Account from a JSON file or generate a new one.
    """
    def __init__(self, name, balance=0.00):
        file = Path("./account_of_"+ name +".json")
        if file.is_file():
            with open('account_of_'+ name +'.json') as json_file:  
                data = json.load(json_file)
            self.name = data['name']
            self._balance = data['balance']
            self.history = data['history']
            
        else:
            self.name = name
            self._balance = balance
            self.history = []
        self.save()

    def deposit(self, amount, description):
        """
            The function deposit will deposit an amount to an account and update its json data file.
            :amount: the amount of cash
            :description: The description of the action
        """
        if isinstance(amount, (int, float)) == False:
            raise TypeError("The inserted amount is not numeric")
        self._balance += amount
        self.history.append('Income of an amount of {}$ at date {} : {}'.format(amount, datetime.datetime.now().date(), description))
        self.save()

    def withdraw(self, amount, description):
        """
            The function withdraw will withdraw an amount fram an account and update its json data file.
            :amount: the amount of cash
            :description: The description of the action
        """
        if isinstance(amount, (int, float)) == False:
            raise TypeError("The inserted amount is not numeric")
        if amount > self._balance:
            raise ValueError("Insufficient funds")
        self._balance -= amount
        self.history.append('Withdraw of an amount of {}$ at date {} : {}'.format(amount, datetime.datetime.now().date(), description))
        self.save()
        
    def convert_then_withdraw(self, amount, currency, description):
        """
            The function convert_then_withdraw will convert an amount to a specific currency and withdraw from an account and update its json data file.
            :amount: the amount of cash
            :currency: the currency in which the amount should be converted
            :description: The description of the action
        """
        if isinstance(amount, (int, float)) == False:
            raise TypeError("The inserted amount is not numeric")
        
        exchange = currency + '_USD'
        api = 'https://free.currencyconverterapi.com/api/v5/convert'
        query = '?q=' + exchange + '&compact=ultra'

        response = requests.get(api + query)
        
        while not response:
            time.sleep(0.1)
    
        rate = response.json()[exchange]
        amount_after_conversion = round(amount * rate, 2)
        
        if amount_after_conversion > self._balance:
            raise ValueError("Insufficient funds")
            
        self._balance -= amount_after_conversion
        self.history.append('Withdraw after conversion of an amount of {} '.format(amount) 
                      + currency 
                      + ' to {} $ at date {} : {}'.format(amount_after_conversion, datetime.datetime.now().date(), description))
        self.save()
        
    def transfert(self, beneficiairy, amount, description):
        """
            The function transfer will transfert an amount from an account to another and update its json data file.
            :beneficiairy: The beneciciairy of the transfert
            :amount: the amount of cash
            :description: The description of the action
        """
        if isinstance(amount, (int, float)) == False:
            raise TypeError("The inserted amount is not numeric")
        if amount > self._balance:
            raise ValueError("Insufficient funds")
        self.withdraw(amount, 'Transfert to {} : {}'.format(beneficiairy.name, description))
        beneficiairy.deposit(amount, 'Transfert from {} : {}'.format(self.name, description))
        self.save()
        beneficiairy.save()
        
    def save(self):
        data = {}
        data['name'] = self.name
        data['balance'] = round(self.balance, 2)
        data['history'] = self.history
        with open('account_of_'+ self.name +'.json', 'w') as json_file:
            json.dump(data, json_file)

    @property
    def balance(self):
        return self._balance

    def __repr__(self):
        return '{0.__class__.__name__}(name={0.name}, balance={0.balance})'.format(self)

    def __str__(self):
        history_list = '\n'
        for transaction in self.history:
            history_list += ('\t- ' + transaction + '\n')
        return '\n\tBank account of {} : \n\tCurrent balance : {} \n\tHistory : {} \n'.format(self.name, self.balance, history_list)

# start of the program

ch = ''
name = ''
currencies = [
    "EUR - Euro",
    "GBP - Great Britain pound (Sterling) (nicknamed Cable)",
    "JPY - Japanese yen",
    "CHF - Swiss Franc (nicknamed Swissie)",
    "AUD - Australian dollar (nicknamed Aussie)",
    "CAD - Canadian dollar (nicknamed Loonie)",
    "CNY - China Yuan Renminbi",
    "NZD - New Zealand dollar (nicknamed Kiwi)",
    "INR - Indian rupee",
    "BZR - Brazilian Real",
    "SEK - Swedish Krona",
    "ZAR - South African Rand",
    "HKD - Hong Kong Dollar"
]

while ch != 7:
    if ch == '1':
        name = str(input("\tEnter your name : "))
        file = Path("./account_of_"+ name +".json")
        if file.is_file():
            print('This account already exists.')
        else:
            account = BankAccount(name)
            print('\n\tAccount {} created successfully.'.format(name))
    elif ch == '2': # Deposit
        name = str(input("\tEnter your name : "))
        file = Path("./account_of_"+ name +".json")
        if file.is_file():
            account = BankAccount(name)
            amount = float(input("\tEnter the amount to deposit : "))
            description = str(input("\tEnter a description for your deposit : "))
            account.deposit(amount, description)
        else:
            print('This account doesn\'t exist')
    elif ch == '3': # Withdraw
        name = str(input("\tEnter your name : "))
        file = Path("./account_of_"+ name +".json")
        if file.is_file():
            account = BankAccount(name)
            amount = float(input("\tEnter the amount to withdraw : "))
            description = str(input("\tEnter a description for your withdraw : "))
            account.withdraw(amount, description)
        else:
            print('This account doesn\'t exist')
    elif ch == '4': # Convert and Withdraw
        name = str(input("\tEnter your name : "))
        file = Path("./account_of_"+ name +".json")
        if file.is_file():
            account = BankAccount(name)
            currency_choice = 0
            while currency_choice < 1 or currency_choice > 13:
                print("\tPlease choose one of the following currencies :")
                for index, cur in enumerate(currencies):
                    print("\t{} - {}".format(index + 1, cur))
                currency_choice = int(input("\tEnter the currency in which you want to do the withdraw : "))
            
            currency = currencies[currency_choice - 1][:3]
            amount = float(input("\tEnter the amount to withdraw : "))
            description = str(input("\tEnter a description for your withdraw : "))
            account.convert_then_withdraw(amount, currency, description)
        else:
            print('This account doesn\'t exist')
    elif ch == '5': # Transfert amount
        name = str(input("\tEnter your name : "))
        file = Path("./account_of_"+ name +".json")
        if file.is_file():
            account = BankAccount(name)
            beneciciary_name = str(input("\tEnter beneciciary's name : "))
            file = Path("./account_of_"+ beneciciary_name +".json")
            if file.is_file():
                beneciciary_account = BankAccount(beneciciary_name)
                amount = float(input("\tEnter the amount to transfert : "))
                description = str(input("\tEnter a description for your transfert : "))
                account.transfert(beneciciary_account, amount, description)
            else:
                print('The account of beneficiary doesn\'t exist')
        else:
            print('This account doesn\'t exist')
    elif ch == '6':
        name = str(input("\tEnter your name : "))
        file = Path("./account_of_"+ name +".json")
        if file.is_file():
            account = BankAccount(name)
            print(account)
        else:
            print('This account doesn\'t exist')
    elif ch == '7':
        print("\tThanks for using Bank Account Managemnt System")
        break
    else :
        if ch is not '':
            print("Invalid choice")
    
    #system("cls");
    print("\tMAIN MENU")
    print("\t1. NEW ACCOUNT")
    print("\t2. DEPOSIT AMOUNT")
    print("\t3. WITHDRAW AMOUNT")
    print("\t4. WITHDRAW AMOUNT IN A SPECIFIC CURRENCY")
    print("\t5. TRANSFERT AMOUNT TO ACCOUNT")
    print("\t6. BALANCE ENQUIRY")
    print("\t7. EXIT")
    print("\tPlease Select Your Option (1-7)")
    #system("cls");

    ch = input("\n\tEnter your choice : ")