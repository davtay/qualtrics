import requests, json, os, csv, sys
from dotenv import load_dotenv

load_dotenv()

directory = os.getenv("QUALTRICS_DIRECTORY")
qualtrics_url = os.getenv("QUALTRICS_URL")
search_url = f"{qualtrics_url}{directory}/contacts/search"
qualtrics_token = os.getenv("QUALTRICS_TOKEN")
headers = {
    "Content-Type": "application/json",
    "X-API-TOKEN": qualtrics_token
}

def qualtrics_lookup() -> list:
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
            qualtrics_users = []
            if contact['result']['elements']:
                contact_id = contact['result']['elements'][0]['id']
                qualtrics_users.append(contact_id)
    print(qualtrics_users)
    if not qualtrics_users:
        log_to_chat('empty')
        sys.exit()
                
    return qualtrics_users
              
def qualtrics_delete(user_ids) -> None:
    for user in user_ids:
        delete_contact_url = f"{qualtrics_url}{directory}/contacts/{user}"
        try:
            delete_contact = requests.request("DELETE",delete_contact_url,headers=headers)
            delete_contact.raise_for_status()
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
            log_to_chat('err')
            sys.exit()
    log_to_chat('success')
    
def log_to_chat(status) -> None:
    webhook_url = os.getenv("WEBHOOK_URL")
    message_headers = {'Content-Type' : 'application/json; charset=UTF-8'}
    message_success = {'text' : 'Staff deletion - Sucess'}
    message_errh = {'text' : 'Staff deletion - Failure: Http error'}
    message_errc = {'text' : 'Staff deletion - Failure: Connection error'}
    message_errt = {'text' : 'Staff deletion - Failure: Timeout'}
    message_err = {'text' : 'Staff deletion - Failure: Something went wrong'}
    message_empty = {'text' : 'Staff deletion - Success: No users to delete'}
    
    if status == 'success':
        chat_message = requests.post(webhook_url,data=json.dumps(message_success),headers=message_headers)
    elif status == 'errh':
        chat_message = requests.post(webhook_url,data=json.dumps(message_errh),headers=message_headers)
    elif status == 'errc':
        chat_message = requests.post(webhook_url,data=json.dumps(message_errc),headers=message_headers)
    elif status == 'errt':
        chat_message = requests.post(webhook_url,data=json.dumps(message_errt),headers=message_headers)
    elif status == 'err':
        chat_message = requests.post(webhook_url,data=json.dumps(message_err),headers=message_headers)
    elif status == 'empty':
        chat_message = requests.post(webhook_url,data=json.dumps(message_empty),headers=message_headers)

def main():
    qualtrics_delete(qualtrics_lookup())
                
if __name__ == '__main__':
    main()