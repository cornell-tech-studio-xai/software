import base64, email, re, sys
activ_words = {'MEETING': {'count': 0, 'sequence': []},
                'MEET': {'count': 0, 'sequence': []},
                'SEAMLESS': {'count': 0, 'sequence': []}
                }
meetings_meta = {"threads": [], "received": 0, "sent": 0}

email_count = {"threads": 0, "emails": 0}


def reset():
    meetings_meta["threads"] = []
    meetings_meta["received"] = 0
    meetings_meta["sent"] = 0
    email_count["threads"] = 0
    email_count["emails"] = 0


def parseMsg(request_id, response, exception):
    if exception is not None:
        print("FAILED: parseMsg: " + str(sys.exc_info()))
        pass
    else:
        msg_text = removeTags(getMessageBody(response))
        msg_words = msg_text.split()
        #msg_words = [word.upper() for word in msg_words]
        for i, word in enumerate(msg_words):
            word = word.upper()
            if word in activ_words:
                if checkSequence(msg_words, i, word):
                    activ_words[word]['count'] += 1
                    if word == 'MEET' or word == 'MEETING':
                        meetings_meta['threads'].append(getThreadId(response))
                        #if isSent(response):
                        #    meetings_meta['sent'] += 1
                        #else:
                        #    meetings_meta['received'] += 1
                    break
        pass


def parseThread(request_id, response, exception):
    if exception is not None:
        print("FAILED: parseThread: " + str(sys.exc_info()))
        pass
    else:
        num_emails_this_thread = len(response['messages'])
        if num_emails_this_thread > 1:
            email_count['emails'] += num_emails_this_thread
            email_count['threads'] += 1
        pass

def getMessageBody(message):
    msg_str = base64.urlsafe_b64decode(message['raw'].encode('ASCII'))
    mime_msg = email.message_from_string(msg_str)
    messageMainType = mime_msg.get_content_maintype()
    if messageMainType == 'multipart':
        for part in mime_msg.get_payload():
            if part.get_content_maintype() == 'text':
                return part.get_payload()
        return ""
    elif messageMainType == 'text':
        return mime_msg.get_payload()
    else:
        print("FAILED: getMessageBody")
        return ""


def removeTags(msg):
    p = re.compile(r'<.*?>')
    s = re.compile(r'  ')
    no_tags = p.sub(' ', msg)
    return s.sub('', no_tags)


def checkSequence(msg_words, index, origin):
    sequence = activ_words[origin]['sequence']
    if sequence:
        i = index + 1
        for word in sequence:
            if i < len(msg_words):
                if word != msg_words[i].upper():
                    return False
            else:
                break
            i += 1
    return True


def getEmailAddress(message):
    addr = ""
    headers = message['payload']['headers']
    for header in headers:
        if header['name'] == "From":
            from_field = header['value']
            if len(from_field) > 2:
                addr =  re.search(r'<.+>', from_field).group(0)[1:-1]
                break
    return addr


def getThreadId(message):
    return message['threadId']


def isSent(message):
    return "SENT" in message['labelIds']


def getEmailStats(http, service, thread_ids):
    '''
    num_threads = 0
    num_emails = 0
    for thread_id in thread_ids:
        try:
            thread = service.users().threads().get(userId='me', id=thread_id).execute()
        except:
            print("Error getting thread!")
            continue

        num_emails_this_thread = len(thread['messages'])
        if num_emails_this_thread > 1:
            num_emails += num_emails_this_thread
            num_threads += 1
    '''

    batchGetThreads(http, service, 'me', thread_ids)

    # purposely rounding to integer value, nobody wants to see floats in a gui
    emails_per_thread = 0
    if email_count['threads'] > 0:
        emails_per_thread = email_count['emails'] / email_count['threads']

    # in hours
    #time_spent = (meetings_meta['sent'] * 3 + meetings_meta['received']) / float(60)
    time_spent = (email_count['emails']*3) / float(60)

    return email_count['emails'], emails_per_thread, time_spent

def batchGetThreads(http, service, userId, threadIds):
    batch = service.new_batch_http_request()
    for threadId in threadIds:
        batch.add(service.users().threads().get(userId=userId,
            id=threadId), callback=parseThread)
    batch.execute(http=http)