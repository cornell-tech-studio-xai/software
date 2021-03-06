import sys
import httplib2
import time

from apiclient import discovery, errors
from oauth2client import client

import activ_parser

def get_credentials(auth_code):
    auth_code = auth_code.replace("`", "/")
    flow = client.flow_from_clientsecrets(
        'client_secret.json',
        scope="https://www.googleapis.com/auth/userinfo.email https://www.googleapis.com/auth/userinfo.profile https://www.googleapis.com/auth/plus.me https://www.googleapis.com/auth/gmail.readonly openid email profile",
        redirect_uri='postmessage')
    flow.redirect_uri = "postmessage"
    #flow.params['access_type'] = 'offline'
    try:
        credentials = flow.step2_exchange(auth_code)
    except:
        raise

    return credentials

def batchGet(http, service, userId, messageIds):
    batch = service.new_batch_http_request()
    for messageId in messageIds:
        batch.add(service.users().messages().get(userId=userId,
            id=messageId, format='raw'), callback=activ_parser.parseMsg)
    batch.execute(http=http)
    # print(activ_words)


def create_output(service, meetings_meta):
    output = {}

    num_emails, emails_per_thread, time_spent = activ_parser.getEmailStats(service, meetings_meta['threads'])

    xai_stats = ["In the last month you...",
                  "Sent and received <b>" + str(num_emails) + " e-mails</b> trying to schedule meetings",
                  "Needed an average of <b>" + str(emails_per_thread) + " e-mails</b> to schedule one meeting",
                  "Spent <b>" + str("{0:.2f}".format(time_spent)) + " hours</b> scheduling meetings"]
    xai_description = "x.ai is a personal assistant who schedules meetings for you"
    xai_logo = "/images/xai_logo.png"
    xai_screenshot = "/images/xai_screen.png"

    on_stats = ["In the last month you..."]
    on_description = "OrderNow is a chatbot that can order food for you"
    on_logo = "/images/on_logo.png"
    on_screenshot = "/images/on_screenshot.png"

    output['xai'] = {"stats": xai_stats, "description": xai_description, "logo": xai_logo, "screenshot": xai_screenshot}
    output['ordernow'] = {"stats": on_stats, "description": on_description, "logo": on_logo, "screenshot": on_screenshot}

    '''
    for word, struct in results.iteritems():
        sequence = word
        for next in struct['sequence']:
            sequence += " " + next
        output[sequence] = struct['count']
    '''
    return output


def parse(auth_code):
    try:
        credentials = get_credentials(auth_code)
    except:
        return "Error getting credentials " + str(sys.exc_info())

    http = credentials.authorize(httplib2.Http())
    service = discovery.build('gmail', 'v1', http=http)

    emails_read = 0
    max_emails = 1000

    next_page_token = ""
    more_pages = True

    q = "newer_than:1m"

    start_time = time.time()

    meta = service.users().messages().list(userId='me', maxResults=100, q=q).execute()

    while emails_read < max_emails and more_pages:
        # This only executes after the first time (for future pages)
        if next_page_token:
            meta = service.users().messages().list( \
                userId='me', maxResults=100, pageToken=next_page_token, q=q).execute()

        if 'messages' not in meta:
            print("No Messages Found")
            break
        messages_meta = meta['messages']

        if 'nextPageToken' in meta:
            next_page_token = meta['nextPageToken']
        else:
            more_pages = False

        message_ids = [msg['id'] for msg in messages_meta]
        batchGet(http, service, 'me', message_ids)
        emails_read += len(message_ids)

    meetings_meta = activ_parser.meetings_meta
    meetings_meta['threads'] = list(set(meetings_meta['threads']))

    output = create_output(service, meetings_meta)

    end_time = time.time()

    output['_NUM_EMAILS'] = emails_read
    output['_ELAPSED_TIME'] = end_time-start_time
    return output