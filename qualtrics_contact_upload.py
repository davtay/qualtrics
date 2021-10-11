import requests, json, os
from dotenv import load_dotenv

load_dotenv()

def log_to_chat(status):
    webhook_url = os.getenv("WEBHOOK_URL")
    message_headers = {'Content-Type' : 'application/json; charset=UTF-8'}
    
    message_success = {'text' : 'Staff creation - Success'}
    message_errh = {'text' : 'Staff creation - Failure: Http error'}
    message_errc = {'text' : 'Staff creation - Failure: Connection error'}
    message_errt = {'text' : 'Staff creation - Failure: Timeout'}
    message_err = {'text' : 'Staff creation - Failure: Something went wrong'}
    
    if status == 'success':
        chat_message = requests.post(webhook_url,data=json.dumps(message_success),headers=message_headers)
    elif status == 'errh':
        chat_message = requests.post(webhook_url,data=json.dumps(message_errh),headers=message_headers)
    elif status == 'errc':
        chat_message = requests.post(webhook_url,data=json.dumps(message_errc),headers=message_headers)
    elif status == 'errt':
        chat_message = requests.post(webhook_url,data=json.dumps(message_errt),headers=message_headers)
    else:
        chat_message = requests.post(webhook_url,data=json.dumps(message_err),headers=message_headers)

def qualtrics_upload():
    qualtrics_url = os.getenv("QUALTRICS_URL")
    qualtrics_token = os.getenv("QUALTRICS_TOKEN")
    qualtrics_file_name = os.getenv("QUALTRICS_FILE_NAME")
    qualtrics_file_loc = os.getenv("QUALTRICS_FILE_LOC")
    qualtrics_file = {'file':(qualtrics_file_name,open(qualtrics_file_loc,'rb'),'text/csv')}
    auth_header = {'x-api-token' : qualtrics_token}

    try:
        upload_contacts = requests.post(qualtrics_url,headers=auth_header,files=qualtrics_file)
        upload_contacts.raise_for_status()
        log_to_chat('success')
    except requests.exceptions.HTTPError as errh:
        log_to_chat('errh')
    except requests.exceptions.ConnectionError as errc:
        log_to_chat('errc')
    except requests.exceptions.Timeout as errt:
        log_to_chat('errt')
    except requests.exceptions.RequestException as err:
        log_to_chat()
        
if __name__ == '__main__':
    qualtrics_upload()