import time
from decimal import Decimal
import mysql.connector

class PNB():
    def __init__(self):
        self.db = mysql.connector.connect(
            host="localhost",
            user="root",
            password="root",
            database="pnbbank"
        )
        self.cursor = self.db.cursor()

        print("""
        Welcome to PNB(Punjab National Bank)
        Choose Given Option: 
        1.) Create Account
        2.) Balance
        3.) Withdraw
        4.) Deposit
        5.) Change Pin
        6.) Exit
        """)

        self.user = int(input("Choose Option Number: "))
        if self.user == 1:
            self.__create_account()
        elif self.user == 2:
            self.__pnb_balance()
        elif self.user == 3:
            self.__pnb_withdraw()
        elif self.user == 4:
            self.__pnb_deposit()
        elif self.user == 5:
            self.__pnb_change_pin()
        elif self.user == 6:
            self.__pnb_exit()
        else:
            print("Choose Valid Option")

    def __create_account(self):
        name = input("Enter your name: ")
        initial_balance = float(input("Enter initial balance: "))
        pin = input("Enter your PIN: ")

        query = "INSERT INTO accounts (name, balance, pin) VALUES (%s, %s, %s)"
        self.cursor.execute(query, (name, initial_balance, pin))
        self.db.commit()

        print("Account created successfully!")

    def __pnb_balance(self):
        account_number = input("Enter your account number: ")
        query = "SELECT balance FROM accounts WHERE account_number = %s"
        self.cursor.execute(query, (account_number,))
        balance = self.cursor.fetchone()

        if balance:
            print("Welcome to your Balance Section")
            print("Current Balance:", balance[0])
        else:
            print("Account not found")

    def __pnb_withdraw(self):
        account_number = input("Enter your account number: ")
        withdraw_amount = Decimal(input("Enter withdrawal amount: "))  # Convert user input to Decimal

        query = "SELECT balance FROM accounts WHERE account_number = %s"
        self.cursor.execute(query, (account_number,))
        balance = self.cursor.fetchone()

        if balance:
            current_balance = balance[0]
            if current_balance >= withdraw_amount:
                new_balance = current_balance - withdraw_amount
                update_query = "UPDATE accounts SET balance = %s WHERE account_number = %s"
                self.cursor.execute(update_query, (new_balance, account_number))
                self.db.commit()
                print("Withdrawal successful. Updated balance:", new_balance)
            else:
                print("Insufficient balance.")
        else:
            print("Account not found")

    def __pnb_deposit(self):
        account_number = input("Enter your account number: ")
        deposit_amount = Decimal(input("Enter deposit amount: "))

        query = "SELECT balance FROM accounts WHERE account_number = %s"
        self.cursor.execute(query, (account_number,))
        balance = self.cursor.fetchone()

        if balance:
            current_balance = balance[0]
            new_balance = current_balance + deposit_amount
            update_query = "UPDATE accounts SET balance = %s WHERE account_number = %s"
            self.cursor.execute(update_query, (new_balance, account_number))
            self.db.commit()
            print("Deposit successful. Updated balance:", new_balance)
        else:
            print("Account not found")

    def __pnb_change_pin(self):
        account_number = input("Enter your account number: ")
        
        # Retrieve the current PIN from the database
        query = "SELECT pin FROM accounts WHERE account_number = %s"
        self.cursor.execute(query, (account_number,))
        current_pin = self.cursor.fetchone()

        if current_pin:
            current_pin = current_pin[0]
            entered_current_pin = input("Enter your current PIN: ")

            if entered_current_pin == current_pin:
                new_pin = input("Enter your new PIN: ")
                new_pin_confirm = input("Re-enter your new PIN: ")

                if new_pin == new_pin_confirm:
                    update_query = "UPDATE accounts SET pin = %s WHERE account_number = %s"
                    self.cursor.execute(update_query, (new_pin, account_number))
                    self.db.commit()
                    print("PIN changed successfully.")
                else:
                    print("New PINs do not match.")
            else:
                print("Incorrect current PIN.")
        else:
            print("Account not found")

    def __pnb_exit(self):
        print("Thank You for Banking With Us")

deepak = PNB()
