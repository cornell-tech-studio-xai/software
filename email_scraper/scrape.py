import base64
import email
from apiclient import errors

class Scraper:
    def __init__:
        service

    def GetMessages(self, service, user_id):
        try:
            message_list = service.users().messages().get(userId=user_id)
            print(message_list)
        except errors.HttpError, error:
            print('An error occurred: %s' % error)

s = Scraper()
