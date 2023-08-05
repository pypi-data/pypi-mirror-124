from websocket import WebSocket
import json
import platform
import random
import time
from threading import Thread

APIEndpoint = 'https://discord.com/api/v9'

class WebsocketManager:
    """
        Websocket Manager for Discord's WebSocket
    """
    def __init__(self, data):
        self.token = data.token
        self.client = data
        self.data = data

    def connect(self):
        self._ws = WebSocket()
        gatewayHeaders = {}
        gatewayHeaders['Authorization'] = f'Bot {self.token}'
        gatewayHeaders['Content-Type'] = 'application/json'
        
        gatewayReq = self.data.manage.RESTGet(f'{APIEndpoint}/gateway/bot', gatewayHeaders).text

        gatewayURL = json.loads(f'{gatewayReq}')['url']

        self._ws.connect(f'{gatewayURL}/?v=9&encoding=json')
        self.connection = self._ws
        
        recv_interval = self.receiveWSMessage(self._ws)
        heartbeat_interval = recv_interval['d']['heartbeat_interval'] * random.random()

        threading = Thread(target = self.heartbeat, args = (self._ws, heartbeat_interval))
        
        threading.start()
        
        return self.connection

    def sendMessage(self, ws, message):
        ws.send(json.dumps(message))
    
    def heartbeat(self, ws, interval):
        while True:
            time.sleep(interval)
            jsonData = {
                'op': 1,
                'd': None
            }
            sendMessage(ws, jsonData)
    
    def receiveWSMessage(self, ws):
        res = ws.recv()
        if res:
            return json.loads(res)
            
    def identify(self, ws):
        self.identifyBoilerplate = {}
        self.identifyBoilerplate['d'] = {}
        self.identifyBoilerplate['d']['token'] = self.token
                    
        # Indeity Opcode 
        self.identifyBoilerplate['op'] = 2
                    
        # Properties
        self.identifyBoilerplate['d']['properties'] = {
                    '$os': str(platform.system()).lower(),
                    '$browser': 'gydo.py',
                    '$device': 'gydo.py'
                }
                    
        # Intents
        self.identifyBoilerplate['d']['intents'] = 51
        
        self.sendMessage(ws, self.identifyBoilerplate)
        
        data = ws.recv()
        self.is_ready = True
        
        return json.loads(data)