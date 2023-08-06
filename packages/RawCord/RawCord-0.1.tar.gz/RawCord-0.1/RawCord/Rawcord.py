from .extension import *
import asyncio

class Client:
    def __init__(self,token):
        self.token = token
        self.commands = []
        self.auth_head = {'Authorization': f"Bot {token}",'content-type': 'application/json'}

    def run(self):
        asyncio.run(GatewayStart(self.token,self.auth_head,self.commands))

    def add_command(self,name,func):
        self.commands.append({"command_name":name,"function":func})

    # Audit Log
    def get_audit_log(self,guild_id,**kwargs):
        path = BASE+f"/guilds/{guild_id}/audit-logs"
        keywords = ["user_id","action_type","before","limit"]
        r = requests.get(Functionals.process_query(path,keywords,kwargs),headers=self.auth_head)
        arguments = json.loads(r.text)

        # NOTE: To be updated in the future
        del arguments["guild_scheduled_events"]

        return Audit_Log(**arguments)

    # Shorthand of Channel.get_message()
    def get_message(self,channel_id,message_id):
        path = BASE+f"/channels/{channel_id}/messages/{message_id}"
        r = requests.get(path,headers=self.auth_head)
        debrief_request(r,self)
        arguments = r.json()
        arguments["__client__"] = self.auth_head

        return Message(**arguments)

    def get_channel(self,channel_id):
        path = BASE+f"/channels/{channel_id}"
        r = requests.get(path,headers=self.auth_head)
        arguments = json.loads(r.text)
        debrief_request(r,self)
        arguments["__client__"] = self.auth_head

        return Channel(**arguments)

    def get_guild(self, guild_id, with_counts=False):
        path = BASE + f"/guilds/{guild_id}?with_counts={with_counts}"
        r = requests.get(path,headers=self.auth_head)
        debrief_request(r,self)
        arguments = r.json()
        arguments["__client__"] = self.auth_head

        return Guild(**arguments)

    def create_guild(self, **kwargs):
        path = BASE + "/guilds"
        expected_args = ['name', 'icon', 'verification_level', 'default_message_notifications', 'explicit_content_filter', 'roles', 'channels', 'afk_channel_id', 'afk_timeout', 'system_channel_id', 'system_channel_flags']
        if not valid_kwargs(kwargs,expected_args):  return
        r = requests.post(path,headers=self.auth_head,json=kwargs)
        debrief_request(r,self,kwargs)
