from google.auth.transport.requests import Request
from googleapiclient.discovery import build
import os
import pickle
import logging

logger = logging.getLogger(__name__)

class GmailService:
    def __init__(self, credentials_path, token_path, scopes):
        self.credentials_path = credentials_path
        self.token_path = token_path
        self.scopes = scopes
        self.service = self.authenticate_gmail()

    def authenticate_gmail(self):
        creds = None
        if os.path.exists(self.token_path):
            with open(self.token_path, 'rb') as token:
                creds = pickle.load(token)

        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                try:
                    creds.refresh(Request())
                except Exception as e:
                    logger.error(f"Error refreshing token: {e}")
                    creds = self.refresh_credentials()
            else:
                creds = self.refresh_credentials()

        with open(self.token_path, 'wb') as token:
            pickle.dump(creds, token)

        return build('gmail', 'v1', credentials=creds)

    def fetch_emails(self, max_results=100):
        results = self.service.users().messages().list(userId='me', maxResults=max_results).execute()
        messages = results.get('messages', [])
        emails = []

        for message in messages:
            msg = self.service.users().messages().get(userId='me', id=message['id']).execute()
            payload = msg['payload']
            headers = payload['headers']
            email_data = {
                'id': msg['id'],
                'sender': '',
                'subject': '',
                'body': '',
                'received_at': msg['internalDate']
            }

            for header in headers:
                if header['name'] == 'From':
                    email_data['sender'] = header['value']
                elif header['name'] == 'Subject':
                    email_data['subject'] = header['value']

            if 'parts' in payload:
                for part in payload['parts']:
                    if part['mimeType'] == 'text/plain':
                        email_data['body'] = part['body'].get('data')
                        break

            emails.append((
                email_data['id'],
                email_data['sender'],
                email_data['subject'],
                email_data['body'],
                email_data['received_at']
            ))

        return emails

    def modify_email_labels(self, email_id, add_labels, remove_labels):
        msg_labels = {'addLabelIds': add_labels, 'removeLabelIds': remove_labels}
        try:
            self.service.users().messages().modify(userId='me', id=email_id, body=msg_labels).execute()
        except Exception as error:
            logger.error(f"An error occurred while modifying email labels: {error}")

    def get_label_id(self, label_name):
        results = self.service.users().labels().list(userId='me').execute()
        labels = results.get('labels', [])
        for label in labels:
            if label['name'] == label_name:
                return label['id']
        return None
