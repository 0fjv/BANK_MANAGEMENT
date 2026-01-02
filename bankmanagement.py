# ---------- DATABASE CONNECTION ----------

def get_connection():
    con = msc.connect(
        host="localhost",
        user="root",
        password="",
        database="bank_db"
    )
    return con


# ---------- FUNCTIONS FOR BANK OPERATIONS ----------

def create_account():
    print("\n--- Create New Account ---")
    try:
name = input("Enter customer name: ")
        address = input("Enter address: ")
        phone = input("Enter phone: ")
        acc_type = input("Enter account type (Saving/Current): ")
        opening_balance = float(input("Enter opening balance: "))

        con = get_connection()
        cur = con.cursor()

        cur.execute(
            "INSERT INTO customer (name, address, phone) VALUES (%s, %s, %s)",
            (name, address, phone)
        )
        cust_id = cur.lastrowid

        cur.execute(
            "INSERT INTO account (cust_id, acc_type, balance) VALUES (%s, %s, %s)",
            (cust_id, acc_type, opening_balance)
        )
        acc_no = cur.lastrowid

        con.commit()

        print("\nAccount created successfully!")
        print("Customer ID :", cust_id) 
        print("Account No. :", acc_no)

    except Exception as e:
        print("Error while creating account:", e)
    finally:
        try:
            cur.close()
            con.close()
        except:
            pass


def deposit():
    print("\n--- Deposit Amount ---")
    try:
        acc_no = int(input("Enter account number: "))
        amount = float(input("Enter amount to deposit: "))

        con = get_connection()
        cur = con.cursor()

        cur.execute("SELECT balance FROM account WHERE acc_no = %s", (acc_no,))
        row = cur.fetchone()

        if row is None: 
            print("Account not found.")
            return

        current_balance = float(row[0])  
        new_balance = current_balance + amount

        cur.execute(
            "UPDATE account SET balance = %s WHERE acc_no = %s",
            (new_balance, acc_no)
        )
        con.commit()

        print("\nDeposit successful.")
        print("Previous balance:", current_balance)
        print("Deposited       :", amount)
        print("New balance     :", new_balance)

    except Exception as e:
        print("Error while depositing:", e)
    finally:
        try:
            cur.close()
            con.close()
        except:
            pass


def withdraw():
    print("\n--- Withdraw Amount ---")
    try:
        acc_no = int(input("Enter account number: "))
        amount = float(input("Enter amount to withdraw: "))

        con = get_connection()
        cur = con.cursor()

        cur.execute("SELECT balance FROM account WHERE acc_no = %s", (acc_no,))
        row = cur.fetchone()

        if row is None:
            print("Account not found.")
            return

        current_balance = float(row[0])   

        if amount > current_balance:
            print("Insufficient balance.")
            return

        new_balance = current_balance - amount

        cur.execute(
            "UPDATE account SET balance = %s WHERE acc_no = %s",
            (new_balance, acc_no)
        )
        con.commit()

        print("\nWithdrawal successful.")
        print("Previous balance:", current_balance)
        print("Withdrawn       :", amount)
        print("New balance     :", new_balance)

    except Exception as e: 
        print("Error while withdrawing:", e)
    finally:
        try:
            cur.close()
            con.close()
        except:
            pass


def check_balance():
    print("\n--- Check Balance ---")
    try:
        acc_no = int(input("Enter account number: "))

        con = get_connection()
        cur = con.cursor()

        cur.execute("""
            SELECT account.acc_no, customer.name, account.acc_type, account.balance
            FROM account
            JOIN customer ON account.cust_id = customer.cust_id
            WHERE account.acc_no = %s
        """, (acc_no,))

        row = cur.fetchone()

        if row is None:
            print("Account not found.")
        else:
            print("\nAccount Details:")
            print("Account No.   :", row[0])
            print("Customer Name:", row[1])
            print("Account Type :", row[2])
            print("Balance       :", row[3])

    except Exception as e:
        print("Error while checking balance:", e)
    finally:
        try:
            cur.close()
            con.close()
        except:
            pass


def view_all_accounts():
    print("\n--- View All Accounts ---")
    try:
        con = get_connection()
        cur = con.cursor()

        cur.execute("""
            SELECT account.acc_no, customer.name, account.acc_type, account.balance
            FROM account
            JOIN customer ON account.cust_id = customer.cust_id
            ORDER BY account.acc_no
        """)
        rows = cur.fetchall()

        if not rows:
            print("No accounts found.")
            return

        print("\nAcc_No | Customer Name            | Type      | Balance")
        print("---------------------------------------------------------")
        for r in rows:
            print(f"{r[0]:<6} | {r[1]:<24} | {r[2]:<9} | {r[3]:>8}")

    except Exception as e:
        print("Error while viewing accounts:", e)
    finally:
        try:
            cur.close()
            con.close()
        except:
            pass


def delete_account():
    print("\n--- Delete Account ---")
    try:
        acc_no = int(input("Enter account number to delete: "))

        con = get_connection()
        cur = con.cursor()

        cur.execute("SELECT cust_id FROM account WHERE acc_no = %s", (acc_no,))
        row = cur.fetchone()

        if row is None:
            print("Account not found.")
            return

        cust_id = row[0]

        confirm = input("Are you sure you want to delete this account? (y/n): ")
        if confirm.lower() != 'y':
            print("Deletion cancelled.")
            return

        cur.execute("DELETE FROM account WHERE acc_no = %s", (acc_no,))
        cur.execute("DELETE FROM customer WHERE cust_id = %s", (cust_id,))
        con.commit()

        print("\nAccount deleted successfully.")

    except Exception as e:
        print("Error while deleting account:", e)
    finally: 
        try:
            cur.close()
            con.close()
        except:
            pass


# ---------- MAIN MENU ----------

def menu():
    while True:
        print("=====================================")
        print("        BANK MANAGEMENT SYSTEM       ")
        print("=====================================")
        print("1. Create new account")
        print("2. Deposit")
        print("3. Withdraw")
        print("4. Check balance")
        print("5. View all accounts")
        print("6. Delete account")
        print("7. Exit")
        print("=====================================")

        choice = int(input("Enter your choice (1-7): "))

        if choice == 1:
            create_account()
        elif choice == 2:
            deposit()
        elif choice == 3:
            withdraw()
        elif choice == 4:
            check_balance()
        elif choice == 5:
            view_all_accounts()
        elif choice == 6:
            delete_account()
        elif choice == 7:
            print("\nThank you for using Bank Management System.")
            break
        else:
            print("Invalid choice. Please try again.") 


if __name__ == "__main__":
    menu()
