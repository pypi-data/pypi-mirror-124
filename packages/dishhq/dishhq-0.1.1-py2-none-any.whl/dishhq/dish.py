from json.decoder import JSONDecodeError
import requests
from requests.structures import CaseInsensitiveDict
from string import Template
import json
import dotenv


class Error(Exception):
    """Base class for other exceptions"""
    pass

class DatabaseError(Error):
    """Exception raised for errors in the database."""

    def __init__(self, message="Database Error"):
        self.message = message
        super().__init__(message)



class database:
    def __init__(self, db_key: str = None):
        if db_key == None:
            try:
                db_key = dotenv.get_key('.env', 'DISH-API-KEY')
            except:
                raise DatabaseError('API Key Not Provided')
        self.url_base = "https://api.dishhq.xyz/"
        self.db_key = db_key
    
    def create(self, key: str, value: str):
        self.url = f"{self.url_base}db/create"

        self.headers = CaseInsensitiveDict()
        self.headers["X-Dish-Key"] = self.db_key
        self.headers["Content-Type"] = "application/json"
        self.data = json.dumps({"key": key, "value": value})

        self.resp = requests.post(self.url, headers=self.headers, data=self.data)
        if json.loads(self.resp.text)["error"]:
            raise DatabaseError(json.loads(self.resp.text)["message"])
        
        return {"key" : key, "value": value}

    def read(self, key: str):
        self.url = f"{self.url_base}db/read?key={key}"
        self.headers = CaseInsensitiveDict()
        self.headers["X-Dish-Key"] = self.db_key

        self.resp = requests.get(self.url, headers=self.headers)

        if json.loads(self.resp.text)["error"]:
            raise DatabaseError(json.loads(self.resp.text)["message"])


        return {"key" : key, "value": json.loads(self.resp.text)["value"]}

    def update(self, key: str, value: str):
        self.value = value
        self.url = f"{self.url_base}db/update"

        self.headers = CaseInsensitiveDict()
        self.headers["X-Dish-Key"] = self.db_key
        self.headers["Content-Type"] = "application/json"
        self.data = json.dumps({'key': key, "value": value})
        self.resp = requests.post(self.url, headers=self.headers, data=self.data)

        if json.loads(self.resp.text)["error"]:
            raise DatabaseError(json.loads(self.resp.text)["message"])

        return   {"key" : key, "value" : value}

    def delete(self, key: str):

        self.url = f"{self.url_base}db/delete?key={key}"
        self.headers = CaseInsensitiveDict()
        self.headers["X-Dish-Key"] = self.db_key
        self.resp = requests.get(self.url, headers=self.headers)

        if json.loads(self.resp.text)["error"]:
            raise DatabaseError(json.loads(self.resp.text)["message"])

        return key

        
