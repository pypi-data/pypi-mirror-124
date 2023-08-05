from .restapi import RESTManager
from .WebsocketManager import WebsocketManager
import json
from ClientUser import ClientUser

APIEndpoint = 'https://discord.com/api/v9'


class Client:
    """
        Main Client for Discord Bots
    """
    def __init__(self, token):
        self.endpoint = APIEndpoint
        self.token = token
        self.manage = RESTManager(self.token, APIEndpoint)
        self.ws = WebsocketManager(self)
        connection = self.ws.connect()
        self.user = ClientUser(self, connection)
    
    """
        Send a message through Discord's REST API
    """
    def sendMessage(
        self, 
        message, 
        channelId, 
        *embed
    ):
        self.messageJSON = {
            'content': f'{message}',
            'embeds': []
        }

        r = self.manage.RESTPostMessage(self.token, APIEndpoint, channelId, self.messageJSON)
        
        return r

    def MessageEmbed(self, title, description):
        self.MessageEmbedJSON = {
            'title': title,
            'description': description
        }

        return self.MessageEmbedJSON