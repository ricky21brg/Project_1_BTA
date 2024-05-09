from FileManager import FileManager
from HistoryMessages import HistoryMessages
import requests
import json

class CurrencyExchange:
    def __init__(self, balance = 0):
        self.file_manager = FileManager()
        self.hist_file_path = "hist.json"
        

    def write_to_history(self, hist_dict):
        try:
            previous_data = self.file_manager.read_json(self.hist_file_path)
            if previous_data is None:
                previous_data = []
            previous_data.append(hist_dict)
            self.file_manager.add_to_json(previous_data, self.hist_file_path)
        except Exception as e:
            print(f"Error while adding to {self.hist_file_path}: {e}")

    def get_exchange_rates(self):
        url = "https://fake-api.apps.berlintech.ai/api/currency_exchange"
        try:
            response = requests.get(url)
            if response.status_code == 200:
                return json.loads(response.text)
            else:
                print(f"An error has occurred: {response.status_code}")
        except Exception as e:
            print(f"An error has occurred: {e}")
    
    def exchange_currency(self, currency_from, currency_to, amount):
        try:
            exchange_rates = self.get_exchange_rates()
            if not exchange_rates:
                print("Currency exchange failed!")
                return None
            rate_from = exchange_rates.get(currency_from)
            rate_to = exchange_rates.get(currency_to)

            if rate_from is None or rate_to is None:
                print("Currency exchange failed!")
                self.file_manager.add_to_json({
                    "operation_type": "exchange",
                    "status": "failure",
                    "pre_exchange_amount": amount,
                    "exchange_amount": None,
                    "currency_from": currency_from,
                    "currency_to": currency_to
                }, self.hist_file_path)
                return None
            
            elif rate_from == 0:
                print("Currency exchange failed!")
                self.file_manager.add_to_json({
                    "operation_type": "exchange",
                    "status": "failure",
                    "pre_exchange_amount": amount,
                    "exchange_amount": None,
                    "currency_from": currency_from,
                    "currency_to": currency_to
                }, self.hist_file_path)
                return None
            
            elif type(amount) not in (int, float):
                print("Currency exchange failed!")
                self.file_manager.add_to_json({
                    "operation_type": "exchange",
                    "status": "failure",
                    "pre_exchange_amount": amount,
                    "exchange_amount": None,
                    "currency_from": currency_from,
                    "currency_to": currency_to
                }, self.hist_file_path)
                return None
            
            else:
                converted_amount = amount * (rate_to / rate_from)
                if converted_amount <= 0:
                    print("Currency exchange failed!")
                    self.file_manager.add_to_json({
                        "operation_type": "exchange",
                        "status": "failure",
                        "pre_exchange_amount": amount,
                        "exchange_amount": None,
                        "currency_from": currency_from,
                        "currency_to": currency_to
                    }, self.hist_file_path)
                    return None
                
            history_message = HistoryMessages.exchange("success", amount, converted_amount, currency_from, currency_to)
            self.write_to_history(history_message)
            self.file_manager.add_to_json({
                    "operation_type": "exchange",
                    "status": "failure",
                    "pre_exchange_amount": amount,
                    "exchange_amount": None,
                    "currency_from": currency_from,
                    "currency_to": currency_to
                }, self.hist_file_path)
            self.file_manager.add_to_json(self.hist_file_path)
            return converted_amount

        except Exception as e:
            history_message = HistoryMessages.exchange("failure", amount, None, currency_from, currency_to)
            self.write_to_history(history_message)
            print("Currency exchange failed!")
            return None