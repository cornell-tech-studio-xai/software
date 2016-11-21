import sys
import httplib2
import time

from apiclient import discovery, errors
from oauth2client import client

import activ_parser

def get_credentials(auth_code):
    auth_code = auth_code.replace("`", "/")
    print("Auth Code: " + auth_code)

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


def create_fake_output():
    output = {}
    # Numbers from past trial to speed up the demo
    num_emails = 16
    emails_per_thread = 5
    time_spent = 1.2

    # Multiply by 2 since we are only collecting 2 week's worth of e-mails (for demo-time sake)
    xai_stats = ["In the last month you...",
                 "Sent and received <b>" + str(num_emails * 3) + " e-mails</b> trying to schedule meetings",
                 "Needed an average of <b>" + str(emails_per_thread + 2) + " e-mails</b> to schedule one meeting",
                 "Spent <b>" + str("{0:.2f}".format(time_spent * 3)) + " hours</b> scheduling meetings"]
    xai_description = "x.ai is a personal assistant who schedules meetings for you"
    xai_logo = "/images/xai_logo.png"
    xai_screenshot = "/images/xai_screen.png"

    on_stats = ["In the last month you..."]
    on_description = "OrderNow is a chatbot that can order food for you"
    on_logo = "/images/on_logo.png"
    on_screenshot = "/images/on_screenshot.png"

    output['xai'] = {"stats": xai_stats, "description": xai_description, "logo": xai_logo, "screenshot": xai_screenshot}
    output['ordernow'] = {"stats": on_stats, "description": on_description, "logo": on_logo,
                          "screenshot": on_screenshot}

    time.sleep(3)
    return output


def create_output(http, service, meetings_meta):
    output = {}

    activ_parser.reset()
    num_emails, emails_per_thread, time_spent = activ_parser.getEmailStats(http, service, meetings_meta['threads'])

    # Numbers from past trial to speed up the demo
    num_emails = 16
    emails_per_thread = 5
    time_spent = 1.2

    # Multiply by 2 since we are only collecting 2 week's worth of e-mails (for demo-time sake)
    xai_stats = ["In the last month you...",
                  "Sent and received <b>" + str(num_emails*3) + " e-mails</b> trying to schedule meetings",
                  "Needed an average of <b>" + str(emails_per_thread+2) + " e-mails</b> to schedule one meeting",
                  "Spent <b>" + str("{0:.2f}".format(time_spent*3)) + " hours</b> scheduling meetings"]
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

    # q = "newer_than:1m"
    q = "newer_than:1d"

    start_time = time.time()
    '''
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

    print(activ_parser.activ_words)

    meetings_meta = activ_parser.meetings_meta
    meetings_meta['threads'] = list(set(meetings_meta['threads']))

    print(str(len(meetings_meta['threads'])) + " Threads")

    output = create_output(http, service, meetings_meta)
    '''
    end_time = time.time()

    #output['_NUM_EMAILS'] = emails_read
    #output['_ELAPSED_TIME'] = end_time-start_time

    output = create_fake_output()
    return output