import os
import json

FILE_NAME = "DATA_STORE_1"
FILE_EXTENSION = ".json"

FILE_MAX_SIZE = 125 # MegaBytes (MB)

FILE_FULLNAME = FILE_NAME + FILE_EXTENSION

startStats = {
    "clicks": 0,
    "stars": 100,
    "test": True,
}

current_file_path = os.path.abspath(__file__)
current_dir = os.path.dirname(current_file_path)
target_folder_path = os.path.join(current_dir, "resources/")
dir = target_folder_path + FILE_FULLNAME

File = None

class Data_Manager:
    def __init__(self):
        self.file_path = dir
        self.dataStore = {}
        try:
            with open(dir, 'r', encoding='utf-8') as f:
                cont = f.read().strip()
                self.dataStore = cont
            d = self.dataStore
            self.dataStore = json.loads(d)
            file_size = os.path.getsize(dir)
            file_size_mb = file_size / (1024 * 1024)
            if file_size_mb > FILE_MAX_SIZE:
                self.dataStore = {}
                print(f"File size more than {FILE_MAX_SIZE}mb. We'll clear file.")
            print("File is found! Data loaded!")
        except FileNotFoundError:
            with open(dir, 'w') as f:
                json.dump(self.dataStore, f)
            print("File is not found! But created!")
        except json.JSONDecodeError:
            print("File contains invalid JSON. Initializing empty datastore.")
            self.dataStore = {}
        
    def Save(self):
        with open(dir, 'w') as f:
            json.dump(self.dataStore, f, indent=4)
        # print("Data saved to file!")

    def Load(self):
        try:
            with open(dir, 'r', encoding='utf-8') as f:
                content = f.read().strip()
                if not content:
                    print("File content is empty!")
                    return {}
                self.dataStore = content
            d = self.dataStore
            self.dataStore = json.loads(d)
            # print("Data loaded from file!")
            return True
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"Error loading data: {str(e)}")
            return False
    def SetData(self, userId=None, name=None, value=None):
        if userId is None:
            # print("Data couldn't be saved! Invalid UserId")
            return None
        if str(userId) not in self.dataStore:
            self.dataStore[str(userId)] = startStats
            print("Stats is not found. But created!")
            return None
        if name is None:
            # print("Invalid name of data to save!")
            return None
        if value is None:
            print("Invalid value of data to save!")
            return None
        self.dataStore[str(userId)][name] = value
        self.Save()
        # print("Successful saved data to dataStore!")
        return True
    def GetData(self, userId=None, name=None):
        if userId is None:
            return None
        if name is None:
            return None
        try:
            value = self.dataStore[str(userId)][name]
            return value
        except:
            return None