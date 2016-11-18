from __future__ import print_function
import httplib2
import os, time

from apiclient import discovery, errors
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

from activ_parser import parseMsg, getMessageBody, activ_words

try:
    import argparse

    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/gmail-python-quickstart.json
SCOPES = 'https://www.googleapis.com/auth/gmail.readonly'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Gmail API Python Quickstart'


def get_credentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'gmail-python-quickstart.json')

    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else:  # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials


def batchGet(http, service, userId, messageIds):
    batch = service.new_batch_http_request()
    for messageId in messageIds:
        batch.add(service.users().messages().get(userId=userId,
            id=messageId, format='raw'), callback=parseMsg)
    batch.execute(http=http)
    # print(activ_words)


def createOutputFile(results):
    for word, struct in results.iteritems():
        sequence = word
        for next in struct['sequence']:
            sequence += " " + next
        print(sequence + " : " + str(struct['count']))


def main():
    """Shows basic usage of the Gmail API.

    Creates a Gmail API service object and outputs a list of label names
    of the user's Gmail account.
    """
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('gmail', 'v1', http=http)

    # results = service.users().labels().list(userId='me').execute()
    # labels = results.get('labels', [])

    emails_read = 0
    max_emails = 400

    next_page_token = ""
    more_pages = True

    start_time = time.time()

    meta = service.users().messages().list(userId='me').execute()

    while (emails_read < max_emails and more_pages):
        # This only executes after the first time (for future pages)
        if next_page_token:
            meta = service.users().messages().list( \
                userId='me', pageToken=next_page_token).execute()

        if 'messages' not in meta:
            print("No Messages Found")
            break;
        messages_meta = meta['messages']

        if 'nextPageToken' in meta:
            next_page_token = meta['nextPageToken']
        else:
            more_pages = False

        message_ids = [msg['id'] for msg in messages_meta]
        batchGet(http, service, 'me', message_ids)
        emails_read += len(message_ids)

    end_time = time.time()
    print("Parsing " + str(emails_read) + " emails took " + \
          str(end_time - start_time) + " seconds")
    print("Final word-counts:")
    # print(activ_words)
    createOutputFile(activ_words)
    return


if __name__ == '__main__':
    main()
