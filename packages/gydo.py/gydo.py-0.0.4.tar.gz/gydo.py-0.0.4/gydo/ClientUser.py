import asyncio
import pymitter
import json

class ClientUser:
    """
        Represents a Discord User
    """
    def __init__(self, data, connection):
        user = data.ws.identify(connection)['user']
        
        self.username = user['username']
        self.discriminator = user['discriminator']
        self.tag = f'{self.username}#{self.discriminator}'
        
        self.is_verified = user['verified']
        self.mfa_enabled = user['mfa_enabled']
        
        self.id = user['id']
        self.mentionSelf = f'<@{self.id}>'