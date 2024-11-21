import sqlite3

conn = sqlite3.connect("bankDb.db")

cursor = conn.cursor()

cursor.execute("""
        CREATE TABLE IF NOT EXISTS Bank(
             accountNo TEXT PRIMARY KEY,
             name TEXT NOT NULL,
             balance REAL NOT NULL)
""")

# Function to create a new account
def create_account(accountNo, name, deposit):
    try:
        cursor.execute("INSERT INTO Bank (accountNo, name, balance) VALUES (?, ?, ?)", (accountNo, name, deposit))
        conn.commit()
        print("Account created successfully.")
    except sqlite3.IntegrityError as e:
        print(f"Error: Account number must be unique. Error: {e}")
    except ValueError:
        print("Error: Invalid deposit amount.")
        
def deposit_money(account_no,amount):
    try:
        if amount is not None and amount>0:
            cursor.execute("SELECT balance FROM Bank WHERE accountNo=?", (account_no,))
            account = cursor.fetchone()
            if account:
                cursor.execute("UPDATE Bank SET balance = balance + ? WHERE accountNo=?", (amount,account_no))
                conn.commit()
                print("Deposit successfully")
            else:
                print("Error: Account not found.")
        else:
            print("Error: Invalid deposit amount.")
    except sqlite3.IntegrityError as e:
        print(f"Error: {e}")

def withdraw_money(account_no, amount):
    try:
        if amount is not None and amount>0:
            cursor.execute("SELECT balance FROM Bank WHERE accountNo=?", (account_no,))
            account = cursor.fetchone()
            if account:
                current_balance = account[0]
                if current_balance >= amount:
                    cursor.execute("UPDATE Bank SET balance = balance -? WHERE accountNo=?", (amount, account_no))
                    conn.commit()
                    print("Withdrawal successful")
                else:
                    print("Error: Insufficient balance.")
            else:
                print("Error: Account not found.")
        else:
            print("Error: Invalid withdrawal amount.")
    except sqlite3.IntegrityError as e:
        print(f"Error: {e}")

def check_balance(account_no):
    try:
        cursor.execute("SELECT balance FROM Bank WHERE accountNo =?", (account_no,))
        balance = cursor.fetchone()
        if balance is None:
            return 0
        else:
            return balance[0]
    except sqlite3.IntegrityError as e:
        print(f"Error: {e}")

# Function to delete an account
def delete_account(account_no):
    try:
        cursor.execute("SELECT * FROM Bank WHERE accountNo=?", (account_no,))
        account = cursor.fetchone()
        if account:
            cursor.execute("DELETE FROM Bank WHERE accountNo=?", (account_no,))
            conn.commit()
            print(f"Account with account number {account_no} has been deleted successfully.")
        else:
            print("Error: Account not found.")
    except sqlite3.IntegrityError as e:
        print(f"Error: {e}")

print("Welcome to our Bank System...")
print("Choose the options accordingly")

while True:
    print("\n1. Create Account")
    print("2. Deposit Money")
    print("3. Withdraw Money")
    print("4. Check Balance")
    print("5. Change name")
    print("6. Delete Account")
    print("7. Display all available accounts")
    print("8. Exit")

    try:
        choice = int(input("Enter your choice: "))

        if choice == 1:
            accountNo = input("Enter your account number (it should be unique): ")
            name = input("Enter your name: ")
            deposit_input = input("Enter initial deposit (optional): ")
            deposit = float(deposit_input) if deposit_input.strip() else 0  # Handle optional deposit
            create_account(accountNo, name, deposit)

        elif choice == 2:
            account_no = input("Enter your account number: ")
            amount_input = input("Enter the amount to deposit: ")
            try:
                amount = float(amount_input)
                deposit_money(account_no, amount)
            except ValueError:
                print("Error: Please enter a valid number for deposit.")

        elif choice == 3:
            account_no = input("Enter your account number: ")
            amount_input = input("Enter the amount to withdraw: ")
            try:
                amount = float(amount_input)
                withdraw_money(account_no, amount)
            except ValueError:
                print("Error: Please enter a valid number for withdrawal.")

        elif choice == 4:
            account_no = input("Enter your account number: ")
            balance = check_balance(account_no)
            if balance:
                print(f"Your current balance is: {balance}")

        elif choice == 5:
            account_no = input("Enter your account number: ")
            new_name = input("Enter your new name: ")
            cursor.execute("UPDATE Bank SET name = ? WHERE accountNo = ?", (new_name, account_no))
            conn.commit()
            print("Name updated successfully.")

        elif choice == 6:
            account_no = input("Enter your account number: ")
            delete_account(account_no)

        elif choice == 7:
            try:
                cursor.execute("SELECT * FROM Bank")
                accounts = cursor.fetchall()
                if accounts:
                    print("\nAccNo\t\tName\t\tBalance")
                    for account in accounts:
                        print(f"{account[0]}\t\t{account[1]}\t\t{account[2]}")
                else:
                    print("No accounts found.")
            except sqlite3.IntegrityError as e:
                print(f"Error: {e}")

        elif choice == 8:
            print("Thank you for using our banking system. Goodbye!")
            break

        else:
            print("Invalid choice. Please try again.")

    except ValueError:
        print("Error: Please enter a valid integer for your choice.")
        continue