import requests

CHATBOT_ENDPOINT = "https://parami.ai"

def get_chatbot_token(id):
    r = requests.get(CHATBOT_ENDPOINT+"/api/v1/chatbot/"+id+"?return_token=1")

    assert r.status_code == 200, "Something went wrong"

    # Keep this for future use, will not change over time
    chatbot_token = r.text

    return chatbot_token

def get_chatbot_session(chatbot_token):
    r = requests.get(CHATBOT_ENDPOINT+"/api/v1/request_chatbot?chatbot_token="+chatbot_token)

    # Keep this throughout a single chat, will be invalidated after expiration
    chatbot_session, my_id = r.text.split("|")

    return chatbot_session, my_id

def send_message_to_chatbot(chatbot_session, message):
    r = requests.post(
        CHATBOT_ENDPOINT+"/api/v1/embedded_chatbot",
        json={
            'chatbot_session': chatbot_session,
            'message': message,
            'action': "message",
        }
    )

    assert r.status_code == 200, "Something went wrong"

def send_get_started_to_chatbot(chatbot_session):
    r = requests.post(
        CHATBOT_ENDPOINT+"/api/v1/embedded_chatbot",
        json={
            'chatbot_session': chatbot_session,
            'message': "Get Started",
            'action': "kick_start",
        }
    )

    assert r.status_code == 200, "Something went wrong"
    
def get_message_from_chatbot(chatbot_session, last_ts=0):
    r = requests.get(CHATBOT_ENDPOINT+"/api/v1/embedded_chatbot?chatbot_session="+chatbot_session+'&after_ts='+str(last_ts))

    chat_history = r.json()

    return chat_history


###########################################
####                                   ####
####    Usage for web chatbot below    ####
####                                   ####
###########################################

#######
## 1 ##
#############################################################
##  Create a Web Chatbot in Asanga and get its chatbot id  ##
#############################################################

CHATBOT_ID = "infopa/ParamiCan"

#######
## 2 ##
###########################################
##  Get the chatbot token from the name  ##
###########################################
chatbot_token = get_chatbot_token(CHATBOT_ID) 

# chatbot_token
# >> 'gNNyl7DvnZefW03gg3jU00xBei23loksBhIvHokWfW0LZvLyE-uMUMlw2d'


#######
## 3 ##
###############################################
##  Request a chatbot session for each user  ##
###############################################
chatbot_session, my_id = get_chatbot_session(chatbot_token)

# chatbot_session
# >> 'gRzd0iV7-tqEOGPmSsoNHky1sdUn6NVPz453oj6gswlYKV0br5meP_hx-ImAJhSatIiYwtVMfu4XBqqrPq3OEaUfnpdBd5'
# my_id
# >> 'asangaweb test2 a0Wqccfxz5xF'

#######
## 4 ##
#####################################
##  Send a message to the chatbot  ##
#####################################
send_message_to_chatbot(chatbot_session, "hi")


#######
## 5 ##
####################################################
##  Retrieve the messages from this conversation  ##
####################################################
messages = get_message_from_chatbot(chatbot_session)
last_ts = messages[0]['datetime']  # datetime from the latest message
'''
messages
>>
[{'msg_id': 'asangaweb test2 vwC8DeJw9n5V',
  'attachments': [],
  'datetime': 1607072686641,
  'body': 'hi',
  'sender': 'asangaweb test2 a0Wqccfxz5xF',   ## This is equal to `my_id` from the above
  'buttons': None,
  'next_input_is_mask': False,
  'terminate': '',
  'is_masked': None}]
'''

import time
time.sleep(3)

messages = get_message_from_chatbot(chatbot_session)
'''
messages
>>
[{'msg_id': 'asangaweb test2 owlKLLu9QH6W',
  'attachments': [],
  'datetime': 1607072687155,
  'body': "Hello!",
  'sender': 'asangaweb test2 test2',
  'buttons': None,
  'next_input_is_mask': False,
  'terminate': '',
  'is_masked': False},
 {'msg_id': 'asangaweb test2 vwC8DeJw9n5V',
  'attachments': [],
  'datetime': 1607072686641,
  'body': 'hi',
  'sender': 'asangaweb test2 a0Wqccfxz5xF',
  'buttons': None,
  'next_input_is_mask': False,
  'terminate': '',
  'is_masked': None}]
'''

messages = get_message_from_chatbot(chatbot_session, last_ts=last_ts)
'''
messages
>>
[{'msg_id': 'asangaweb test2 owlKLLu9QH6W',
  'attachments': [],
  'datetime': 1607072687155,
  'body': "Hello!",
  'sender': 'asangaweb test2 test2',
  'buttons': None,
  'next_input_is_mask': False,
  'terminate': '',
  'is_masked': False}]
'''
