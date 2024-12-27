#Welcome to the IIT Bank

import random
import hashlib
from datetime import datetime

# File paths
ACCOUNTS_FILE = "accounts.txt"
TRANSACTIONS_FILE = "transactions.txt"

# Utility Functions
def hash_password(password):
    """Hashes the password using SHA-256."""
    return hashlib.sha256(password.encode()).hexdigest()

def generate_account_number():
    """Generates a random 6-digit account number."""
    return str(random.randint(100000, 999999))

def load_accounts():
    """Loads accounts data from the accounts file."""
    accounts = {}
    try:
        with open(ACCOUNTS_FILE, "r") as file:
            for line in file:
                account_number, name, password, balance = line.strip().split(",")
                accounts[account_number] = {
                    "name": name,
                    "password": password,
                    "balance": float(balance)
                }
    except FileNotFoundError:
        # If the file doesn't exist, return an empty dictionary
        pass
    return accounts

def save_account(account_number, name, password, balance):
    """Saves a new account to the accounts file."""
    with open(ACCOUNTS_FILE, "a") as file:
        file.write(f"{account_number},{name},{password},{balance}\n")

def log_transaction(account_number, transaction_type, amount):
    """Logs a transaction to the transactions file."""
    with open(TRANSACTIONS_FILE, "a") as file:
        date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        file.write(f"{account_number},{transaction_type},{amount},{date}\n")

def load_transactions(account_number):
    """Loads all transactions for a specific account."""
    transactions = []
    try:
        with open(TRANSACTIONS_FILE, "r") as file:
            for line in file:
                acc_num, txn_type, amount, date = line.strip().split(",")
                if acc_num == account_number:
                    transactions.append({
                        "type": txn_type,
                        "amount": float(amount),
                        "date": date
                    })
    except FileNotFoundError:
        # If the file doesn't exist, return an empty list
        pass
    return transactions

# Banking System Functions
def create_account():
    """Handles account creation."""
    print("\n--- Create Account ---")
    name = input("Enter your name: ")
    initial_deposit = float(input("Enter your initial deposit: "))
    password = input("Enter a password: ")
    hashed_password = hash_password(password)
    account_number = generate_account_number()

    # Save account to file
    save_account(account_number, name, hashed_password, initial_deposit)
    print(f"Account created successfully! Your account number is: {account_number}")

def login():
    """Handles user login."""
    print("\n--- Login ---")
    account_number = input("Enter your account number: ")
    password = input("Enter your password: ")
    hashed_password = hash_password(password)

    accounts = load_accounts()
    if account_number in accounts and accounts[account_number]["password"] == hashed_password:
        print("Login successful!")
        account_menu(account_number, accounts[account_number])
    else:
        print("Invalid account number or password.")

def account_menu(account_number, account_data):
    """Displays the account menu after successful login."""
    while True:
        print("\n--- Account Menu ---")
        print("1. Deposit")
        print("2. Withdraw")
        print("3. View Balance")
        print("4. View Transaction History")
        print("5. Logout")
        choice = input("Enter your choice: ")

        if choice == "1":
            deposit(account_number, account_data)
        elif choice == "2":
            withdraw(account_number, account_data)
        elif choice == "3":
            print(f"Your current balance is: {account_data['balance']}")
        elif choice == "4":
            transactions = load_transactions(account_number)
            if transactions:
                print("\n--- Transaction History ---")
                for txn in transactions:
                    print(f"{txn['date']} - {txn['type']}: {txn['amount']}")
            else:
                print("No transactions found.")
        elif choice == "5":
            print("Logged out successfully!")
            break
        else:
            print("Invalid choice. Please try again.")

def deposit(account_number, account_data):
    """Handles deposit transactions."""
    amount = float(input("Enter amount to deposit: "))
    account_data["balance"] += amount
    update_account(account_number, account_data)
    log_transaction(account_number, "Deposit", amount)
    print(f"Deposit successful! Your new balance is: {account_data['balance']}")

def withdraw(account_number, account_data):
    """Handles withdrawal transactions."""
    amount = float(input("Enter amount to withdraw: "))
    if amount > account_data["balance"]:
        print("Insufficient balance!")
    else:
        account_data["balance"] -= amount
        update_account(account_number, account_data)
        log_transaction(account_number, "Withdrawal", amount)
        print(f"Withdrawal successful! Your new balance is: {account_data['balance']}")

def update_account(account_number, account_data):
    """Updates account details in the accounts file."""
    accounts = load_accounts()
    accounts[account_number] = account_data
    with open(ACCOUNTS_FILE, "w") as file:
        for acc_num, data in accounts.items():
            file.write(f"{acc_num},{data['name']},{data['password']},{data['balance']}\n")

# Main Program
def main():
    while True:
        print("\n--- IIT Bank ---")
        print("1. Create Account")
        print("2. Login")
        print("3. Exit")
        choice = input("Enter your choice: ")

        if choice == "1":
            create_account()
        elif choice == "2":
            login()
        elif choice == "3":
            print("Thank you for using the Banking System. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
