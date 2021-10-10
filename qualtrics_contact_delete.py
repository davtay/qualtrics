import requests, json, os, csv, sys
from dotenv import load_dotenv

def qualtrics_lookup_delete():
    directory = os.getenv("QUALTRICS_DIRECTORY")
    qualtrics_url = os.getenv("QUALTRICS_URL")
    search_url = f"{qualtrics_url}{directory}/contacts/search"

    qualtrics_token = os.getenv("QUALTRICS_TOKEN")
    headers = {
        "Content-Type": "application/json",
        "X-API-TOKEN": qualtrics_token
    }

    qualtrics_file_loc = os.getenv("QUALTRICS_FILE_LOC")
    with open(qualtrics_file_loc, 'r') as csv_file:
        field = next(csv_file)
        while True:
            email = csv_file.readline()
            if not email:
                break
            payload = {"filter": {
                "comparison": "eq",
                "filterType": "email",
                "value": email.strip()
                }
            }
            response = requests.request("POST", search_url, json=payload, headers=headers)
            contact = response.json()

            if contact['result']['elements']:
                contact_id = contact['result']['elements'][0]['id']
                delete_contact_url = f"{qualtrics_url}{directory}/contacts/{contact_id}"
                try:
                    delete_contact = requests.request("DELETE",delete_contact_url,headers=headers)
                    delete_contact.raise_for_status()
                    log_to_chat('success')
                except requests.exceptions.HTTPError as errh:
                    log_to_chat('errh')
                    sys.exit()
                except requests.exceptions.ConnectionError as errc:
                    log_to_chat('errc')
                    sys.exit()
                except requests.exceptions.Timeout as errt:
                    log_to_chat('errt')
                    sys.exit()
                except requests.exceptions.RequestException as err:
                    log_to_chat()
                    sys.exit()

def log_to_chat(status):
    
    webhook_url = os.getenv("WEBHOOK_URL")
    message_headers = {'Content-Type' : 'application/json; charset=UTF-8'}
    message_success = {'text' : 'Disabled staff deletion completed'}
    message_errh = {'text' : 'Staff deletion - Failure: Http error'}
    message_errc = {'text' : 'Staff deletion - Failure: Connection error'}
    message_errt = {'text' : 'Staff deletion - Failure: Timeout'}
    message_err = {'text' : 'Staff deletion - Failure: Something went wrong'}
    
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
                
if __name__ == '__main__':
    qualtrics_lookup_delete()