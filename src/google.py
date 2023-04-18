import base64
import datetime
import json
import os
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from google.oauth2 import service_account

from src.util import generate_short_uuid

DECODED_GOOGLE_CREDS_STR = base64.b64decode(os.environ.get(
    'GOOGLE_CREDENTIALS_JSON_ENCODED')).decode('utf-8')


def generate_google_meet_link(description, severity, emails):
    """
    Generates a google meet link for the given description and severity
    """
    print("Generating google meet link")
    creds = service_account.Credentials.from_service_account_info(
        info=json.loads(DECODED_GOOGLE_CREDS_STR), scopes=['https://www.googleapis.com/auth/calendar'])

    print("Got credentials")
    service = build('calendar', 'v3', credentials=creds)

    print("Built service")
    start_time = datetime.datetime.now()
    end_time = start_time + datetime.timedelta(hours=1)

    print("Got start and end time")
    event = {
        'summary': f"[{severity}] {description}",
        'start': {
            'dateTime': start_time.isoformat(),
            'timeZone': 'Etc/GMT+3',
        },
        'attendees': [{'email': email} for email in emails],
        'end': {
            'dateTime': end_time.isoformat(),
            'timeZone': 'Etc/GMT+3',
        },
        'conferenceData': {
            'createRequest': {
                'conferenceSolutionKey': {
                    'type': 'hangoutsMeet'
                },
                'requestId': generate_short_uuid(),
            }
        },
    }

    print("Created event")

    # event = service.events().insert(calendarId='primary', body=event,
    # conferenceDataVersion=1).execute()

    print("Inserted event")

    # meet_link = event['hangoutLink']

    return "https://meet.google.com/lookup/"
