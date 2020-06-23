from twitter import Twitter, OAuth


class TwitterBot:

    def __init__(self,token,token_secret,consumer_key,consumer_secret):
        self.tw = Twitter(auth=OAuth(token, token_secret, consumer_key, consumer_secret))
    

    def generate_message(self,target_username,message):
        return {
                "event": {
                    "type": "message_create",
                    "message_create": { 
                        "target": {
                            "recipient_id": self.tw.users.show(screen_name=target_username)["id"]},
                            "message_data": {"text": message}}}}

    # TODO
    def generate_message_with_attachment(self,target_username,message):
        return {
                "event": {
                    "type": "message_create",
                    "message_create": { 
                        "target": {
                            "recipient_id": self.tw.users.show(screen_name=target_username)["id"]},
                            "message_data": {"text": message}}}}


    def send_direct(self,target_username,message):
        self.tw.direct_messages.events.new(_json=self.generate_message(target_username,message))


    def check_home(self):
        print(self.tw.statuses.home_timeline())