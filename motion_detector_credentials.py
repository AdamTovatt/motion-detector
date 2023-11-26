import ujson
import os

class MotionDetectorCredentials:
    def __init__(self, detector_id, secret_key):
        self._detector_id = detector_id
        self._secret_key = secret_key

    @property
    def detector_id(self):
        return self._detector_id

    @detector_id.setter
    def detector_id(self, value):
        self._detector_id = value

    @property
    def secret_key(self):
        return self._secret_key

    @secret_key.setter
    def secret_key(self, value):
        self._secret_key = value
    
    @staticmethod
    def load():
        try:
            with open("motion_detector_credentials.txt", "r") as file:
                data = ujson.load(file)
                return MotionDetectorCredentials(
                    detector_id=data["id"],
                    secret_key=data["secretKey"]
                )
        except (OSError, ValueError):
            return None

    def save(self):
        data = {
            "id": self._detector_id,
            "secretKey": self._secret_key,
        }
        with open("motion_detector_credentials.txt", "w") as file:
            ujson.dump(data, file)
    
    @staticmethod
    def remove():
        try:
            os.remove("motion_detector_credentials.txt")
        except OSError:
            pass
    
    def __str__(self):
        return f"MotionDetectorCredentials(id={self.detector_id}, secretKey={self.secret_key})"
