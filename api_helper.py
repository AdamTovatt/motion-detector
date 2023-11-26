from motion_detector_credentials import MotionDetectorCredentials
import requests
import machine

class ApiHelper:
    BASE_URL = "https://sakurapi.se/motion-detector/"
    
    def __init__(self):
        self.apiKey = self.loadLoadApiKey()
        self.detectorCredentials = MotionDetectorCredentials.load()

    @property
    def hasCredentials(self):
        return (
            self.detectorCredentials is not None and
            bool(self.detectorCredentials.detector_id) and
            bool(self.detectorCredentials.secret_key)
        )

    def loadLoadApiKey(self):
        try:
            with open("api_key.txt", "r") as file:
                return file.read().strip()
        except FileNotFoundError:
            print("Error: api_key.txt not found.")
            return None
        
    def createDetector(self):
        if self.apiKey is None:
            print("Error: Missing API key.")
            return

        url  = self.BASE_URL + "create-new"
        headers = {"x-api-key": self.apiKey}

        try:
            response = requests.post(url, headers=headers)
            
            if  response.status_code != 200:
                raise Exception("Status code from api: " + response.status_code)

            json_data = response.json()
            self.detectorCredentials = MotionDetectorCredentials(
                detector_id=json_data["id"],
                secret_key=json_data["secretKey"]
            )

            # Save the updated credentials
            self.detectorCredentials.save()

            print("Motion detector created successfully.")
        except Exception as e:
            print(f"Error creating motion detector: {e}")
            
    def registerMotion(self):
        if not self.hasCredentials:
            print("Error: Missing motion detector credentials.")
            machine.reset()

        url = self.BASE_URL + "register-motion"
        headers = {
            "x-api-key": self.apiKey,
            "Content-Type": "application/json"
        }

        payload = {
            "id": self.detectorCredentials.detector_id,
            "secretKey": self.detectorCredentials.secret_key
        }

        try:
            response = requests.post(url, headers=headers, json=payload)
            
            if response.status_code != 200:
                if response.status_code == 403:
                    MotionDetectorCredentials.remove() # this detector doesn't exist in the database so we remove it
                    machine.reset() # reset so that we start over
                raise Exception("Status code from API: " + str(response.status_code))

            print("Motion registered successfully.")
        except Exception as e:
            print(f"Error registering motion: {e}")