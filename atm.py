import datetime

class User:
    def __init__(self, user_id, pin, balance=0):
        self.user_id = user_id
        self.pin = pin
        self.balance = balance
        self.transaction_history = []

    def verify_pin(self, pin):
        return self.pin == pin

    def add_transaction(self, transaction_type, amount):
        self.transaction_history.append({
            'type': transaction_type,
            'amount': amount,
            'date': datetime.datetime.now()
        })

    def get_transaction_history(self):
        return self.transaction_history

    def withdraw(self, amount):
        if amount > self.balance:
            print("Insufficient balance!")
        else:
            self.balance -= amount
            self.add_transaction('Withdraw', amount)
            print(f"Withdrawn: ${amount}")

    def deposit(self, amount):
        self.balance += amount
        self.add_transaction('Deposit', amount)
        print(f"Deposited: ${amount}")

    def transfer(self, amount, receiver):
        if amount > self.balance:
            print("Insufficient balance!")
        else:
            self.balance -= amount
            receiver.balance += amount
            self.add_transaction('Transfer', amount)
            receiver.add_transaction('Received', amount)
            print(f"Transferred: ${amount} to User {receiver.user_id}")


class ATM:
    def __init__(self):
        self.users = {}
        self.current_user = None

    def add_user(self, user):
        self.users[user.user_id] = user

    def authenticate_user(self, user_id, pin):
        user = self.users.get(user_id)
        if user and user.verify_pin(pin):
            self.current_user = user
            return True
        return False

    def show_menu(self):
        print("\nATM Menu:")
        print("1. Transaction History")
        print("2. Withdraw")
        print("3. Deposit")
        print("4. Transfer")
        print("5. Quit")

    def perform_operation(self, choice):
        if choice == 1:
            self.show_transaction_history()
        elif choice == 2:
            self.withdraw()
        elif choice == 3:
            self.deposit()
        elif choice == 4:
            self.transfer()
        elif choice == 5:
            self.quit()

    def show_transaction_history(self):
        history = self.current_user.get_transaction_history()
        if not history:
            print("No transactions yet.")
        else:
            for transaction in history:
                print(f"{transaction['date']} - {transaction['type']}: ${transaction['amount']}")

    def withdraw(self):
        amount = float(input("Enter amount to withdraw: "))
        self.current_user.withdraw(amount)

    def deposit(self):
        amount = float(input("Enter amount to deposit: "))
        self.current_user.deposit(amount)

    def transfer(self):
        receiver_id = input("Enter receiver user ID: ")
        receiver = self.users.get(receiver_id)
        if not receiver:
            print("Receiver not found.")
        else:
            amount = float(input("Enter amount to transfer: "))
            self.current_user.transfer(amount, receiver)

    def quit(self):
        print("Thank you for using the ATM!")
        self.current_user = None


def main():
    atm = ATM()

    # Adding some dummy users
    atm.add_user(User('user1', '1234', 1000))
    atm.add_user(User('user2', '5678', 500))

    print("Welcome to the ATM!")
    user_id = input("Enter user ID: ")
    pin = input("Enter PIN: ")

    if atm.authenticate_user(user_id, pin):
        print("Authentication successful!")
        while atm.current_user:
            atm.show_menu()
            choice = int(input("Enter your choice: "))
            atm.perform_operation(choice)
    else:
        print("Authentication failed! Please check your user ID and PIN.")


if __name__ == "__main__":
    main()
