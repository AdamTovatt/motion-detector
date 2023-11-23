from html_helper import HtmlHelper
from network_credentials import NetworkCredentials
from url_decoder import unquote
import network
import network
import socket
import time

class HttpAccessPoint:
    def __init__(self, ssid, password):
        self.accessPoint = network.WLAN(network.AP_IF)
        self.accessPoint.config(essid=ssid, password=password)
        self.configPageHtml = HtmlHelper.getConfigPage()
        self.submittedPageHtml = HtmlHelper.getSubmittedPage()
        
    def start(self):
        print("starting")
        self.accessPoint.active(True)
        while(self.accessPoint.active() == False):
            pass

        self.httpSocket = socket.socket()
        self.httpSocket.bind((self.accessPoint.ifconfig()[0], 80))
        self.httpSocket.listen(1)
        print("listening")
        
    def stop(self):
        if hasattr(self, 'httpSocket'):
            self.httpSocket.close()
            
        self.accessPoint.active(False)

    def parseUrlInput(self, urlInput):
        if "ssid" in urlInput and "password" in urlInput:
            print("VALID INPUT")
            return NetworkCredentials.fromQueryParameters(urlInput)
        else:
            print("INVALID INPUT")
            return None

    def getNetworkCredentials(self):
        try:
            while True:
                connection, address = self.httpSocket.accept()
                print("got connection")
                request = connection.recv(1024)
                requestText = request.decode("utf-8")
                
                requestParts = requestText.split()
                httpMethod = requestParts[0]
                
                url = requestParts[1]
                
                if(len(url) > 1):
                    result = self.parseUrlInput(unquote(url))
                    if result is not None and len(result.password) > 0:
                        connection.send(self.submittedPageHtml)
                        time.sleep(1)
                        return result
                
                connection.send(self.configPageHtml)
                connection.close()
                
        except OSError as e:
            print(f" >> ERROR: {e}")
        finally:
            connection.close()