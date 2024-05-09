import json

class FileManager:
    def load_data(self, filename):
        try:
            with open(filename, "r") as file:
             return file.read()
        except FileNotFoundError:
            return f"Error: {filename} not found"
        except Exception as e:
            return f"Error while reading from {filename}: {e}"

    def save_data(self, filename, data):
        try:
            with open(filename, "w") as file:
                file.write(data)
        except FileNotFoundError:
            return f"Error: {filename} not found"
        except Exception as e:
            return f"Error while writing to {filename}: {e}"

    def read_json(self, json_file_path):
        try:
            with open(json_file_path, "r") as file:
              list_of_dicts = json.load(file)
            return list_of_dicts
        except FileNotFoundError:
            return f"Error: {json_file_path} not found"
        except Exception as e:
            return f"Error while reading from {json_file_path}: {e}"
        
    def write_json(self, list_of_dicts, json_file_path):
        try:
            with open(json_file_path, "w") as file:
                json.dump(list_of_dicts, file)
        except FileNotFoundError:
            return f"Error: {json_file_path} not found"
        except Exception as e:
            return f"Error while writing to {json_file_path}: {e}"

    def add_to_json(self, data, json_file_path):
        try:
            previous_data = self.read_json(json_file_path)
            if previous_data:
                previous_data.append(data)
                self.write_json(previous_data, json_file_path)
            else:
                self.write_json([data], json_file_path)
        except Exception as e:
            return f"Error while appending to {json_file_path}: {e}"