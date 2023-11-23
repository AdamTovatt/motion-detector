class NetworkCredentials:
    def __init__(self, ssid, password):
        self._ssid = ssid
        self._password = password

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