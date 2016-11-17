import base64, email, re
activ_words =  {'MEETING': {'count':0, 'sequence':[]}, \
                'MEET': {'count':0, 'sequence':[]}, \
                'SEAMLESS': {'count':0, 'sequence':[]},
                'UBER': {'count':0, 'sequence':[]}
                }

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

def parseMsg(request_id, response, exception):
    if exception is not None:
        print("FAILED: parseMsg")
        pass
    else:
        msg_text = removeTags(getMessageBody(response))
        msg_words = msg_text.split()
        msg_words = [word.upper() for word in msg_words]
        for i, word in enumerate(msg_words):
            if word in activ_words:
                if checkSequence(msg_words, i, word):
                    activ_words[word]['count'] += 1
        pass

def checkSequence(msg_words, index, origin):
    sequence = activ_words[origin]['sequence']
    if sequence:
        i = index + 1
        for word in sequence:
            if i < len(msg_words):
                if word != msg_words[i].upper():
                    return False
            else:
                break;
            i += 1
    return True
