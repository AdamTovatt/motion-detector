class HtmlHelper:
    @staticmethod
    def getConfigPage(file_path="wifi_configuration.html"):
        with open(file_path, "r") as file:
            return file.read()
        
    @staticmethod
    def getSubmittedPage(file_path="submitted.html"):
        with open(file_path, "r") as file:
            return file.read()