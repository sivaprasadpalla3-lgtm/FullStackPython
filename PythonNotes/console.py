from abc import ABC, abstractmethod


class BankAccount(ABC):

    def __init__(self, name, number, balance):
        self._name = name
        self._number = number
        self._balance = balance

    @abstractmethod
    def get_account_type(self):
        pass

    def get_details(self):
        return (
            f"Name: {self._name}, "
            f"Account Number: {self._number}, "
            f"Balance: {self._balance}, "
            f"Account Type: {self.get_account_type()}"
        )


class SavingsAccount(BankAccount):

    def get_account_type(self):
        return "Savings Account"


class CurrentAccount(BankAccount):

    def get_account_type(self):
        return "Current Account"


class SalaryAccount(BankAccount):

    def get_account_type(self):
        return "Salary Account"


class Bank:

    bank_name = "SBI Bank"

    def __init__(self):
        self.__accounts = []

    def add_account(self, account):
        self.__accounts.append(account)

    def display_all(self):

        if not self.__accounts:
            print("No registered accounts")
        else:
            for account in self.__accounts:
                print(account.get_details())

    @classmethod
    def get_bank_name(cls):
        return cls.bank_name

    @staticmethod
    def welcome_message():
        return "Welcome to SBI Bank"


bank = Bank()

print(Bank.welcome_message())
print("Bank:", Bank.get_bank_name())


while True:

    print("\n===== BANK ACCOUNT MANAGEMENT SYSTEM =====")
    print("1. Register Savings Account")
    print("2. Register Current Account")
    print("3. Register Salary Account")
    print("4. Display All Accounts")
    print("0. Exit")

    choice = input("Enter your choice: ")

    if choice == "1":

        name = input("Enter account holder name: ")
        number = int(input("Enter account number: "))
        balance = float(input("Enter balance: "))

        account = SavingsAccount(name, number, balance)
        bank.add_account(account)

        print("Savings Account registered successfully!")


    elif choice == "2":

        name = input("Enter account holder name: ")
        number = int(input("Enter account number: "))
        balance = float(input("Enter balance: "))

        account = CurrentAccount(name, number, balance)
        bank.add_account(account)

        print("Current Account registered successfully!")


    elif choice == "3":

        name = input("Enter account holder name: ")
        number = int(input("Enter account number: "))
        balance = float(input("Enter balance: "))

        account = SalaryAccount(name, number, balance)
        bank.add_account(account)

        print("Salary Account registered successfully!")


    elif choice == "4":

        print("\n===== REGISTERED ACCOUNTS =====")
        bank.display_all()


    elif choice == "0":

        print("Thank you! Exiting the system.")
        break


    else:

        print("Invalid option. Please try again.")





