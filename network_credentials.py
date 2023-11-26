import ujson
import os

class NetworkCredentials:
    def __init__(self, ssid, password, username):
        self._ssid = ssid
        self._password = password
        self._username = username

    @property
    def ssid(self):
        return self._ssid

    @ssid.setter
    def ssid(self, value):
        self._ssid = value

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, value):
        self._password = value

    @property
    def username(self):
        return self._username

    @username.setter
    def username(self, value):
        self._username = value
        
    @staticmethod
    def fromQueryParameters(query_string):
        params = {}
        if query_string:
            pairs = query_string[2:].split("&")  # Remove leading "/?" and split by "&"
            for pair in pairs:
                key, value = pair.split("=")
                params[key] = value

        return NetworkCredentials(
            ssid=params.get("ssid", ""),
            password=params.get("password", ""),
            username=params.get("username", ""),
        )
    
    @staticmethod
    def load():
        try:
            with open("network_credentials.txt", "r") as file:
                data = ujson.load(file)
                return NetworkCredentials(
                    ssid=data["ssid"],
                    password=data["password"],
                    username=data["username"]
                )
        except (OSError, ValueError):
            return None

    def save(self):
        data = {
            "ssid": self._ssid,
            "password": self._password,
            "username": self._username
        }
        with open("network_credentials.txt", "w") as file:
            ujson.dump(data, file)
    
    @staticmethod
    def remove():
        try:
            os.remove("network_credentials.txt")
        except OSError:
            pass
    
    def __str__(self):
        return f"NetworkCredentials(ssid={self.ssid}, password={self.password}, username={self.username})"