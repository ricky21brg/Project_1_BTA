from FileManager import FileManager
from HistoryMessages import HistoryMessages

class Account:
    def __init__(self, balance = 0):
        self.balance = balance
        self.file_manager = FileManager()
        self.hist_file_path = "hist.json"
        

    def write_to_history(self, hist_dict):
        try:
            previous_data = self.file_manager.read_json(self.hist_file_path)
            if previous_data is None:
                previous_data = []
            previous_data.append(hist_dict)
            self.file_manager.add_to_json(self.hist_file_path)
        except Exception as e:
            return f"Error while adding to {self.hist_file_path}: {e}"

    def deposit(self, amount):
        try:
            if type(amount) == int or type(amount) == float:
                if amount <= 0:
                    print("Invalid amount for deposit!")
                else:    
                    self.balance += amount
                    history_message = HistoryMessages.deposit("success", amount, self.balance)
                    self.write_to_history(history_message)
            else:
                print("Invalid amount for deposit!")
            
        except ValueError as ve:
            print("Invalid amount for deposit!")
            history_message = HistoryMessages.deposit("failure", amount, self.balance)
            self.write_to_history(history_message)
            
    def debit(self, amount):
        try:
            if type(amount) == int or type(amount) == float:
                if amount <= 0 or amount > self.balance:
                    print("Invalid amount for debit!")
                else:
                    self.balance -= amount
                    history_message = HistoryMessages.debit("success", amount, self.balance)
                    self.write_to_history(history_message)                
            else:
                print("Invalid amount for debit!")
        except ValueError as ve:
            history_message = HistoryMessages.debit("failure", amount, self.balance)
            self.write_to_history(history_message)
            return "An error {ve} has occurred. Transaction not processed"
            
    def get_balance(self):
        return self.balance

    def dict_to_string(self, dict):
        if dict["operation_type"] != "exchange":
            return f'type: {dict["operation_type"]} status: {dict["status"]} amount: {dict["amount_of_deposit"]} balance: {dict["total_balance"]}'
        else:
            return f'type: {dict["operation_type"]} status: {dict["status"]} pre exchange amount: {dict["pre_exchange_amount"]} exchange amount: {dict["exchange_amount"]} currency from: {dict["currency_from"]} currency to: {dict["currency_to"]}'
        

    def get_history(self):
        try:
            transaction_history = self.file_manager.read_json(self.hist_file_path)
            if transaction_history is None:
                return "No previous transactions available"
            transaction_str = [self.dict_to_string(dict) for dict in transaction_history]
            return "\n".join(transaction_str)
        except Exception as e:
            return f"An error {e} as occurred while retrieving transaction history"