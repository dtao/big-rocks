"""Script to view calendar events for the past week."""

import json
import pickle
import os.path

from datetime import datetime, timedelta

from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']


def get_events(start_time, end_time):
    """Get events for the given period."""
    service = build('calendar', 'v3', credentials=get_credentials())

    result = service.events().list(
        calendarId='primary', timeMin=format_datetime(start_time),
        timeMax=format_datetime(end_time), maxResults=100, singleEvents=True,
        orderBy='startTime').execute()
    return result.get('items', [])


def get_credentials():
    """Get valid credentials for the Google API.

    On the first run, this sends the user through the OAuth flow, on which an
    access token will be cached locally. On subsequent runs the cached
    credentials will be used.
    """
    creds = None

    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)

    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    return creds


def format_datetime(datetime):
    """Format a datetime for the Google API."""
    return datetime.isoformat() + 'Z'


if __name__ == '__main__':
    now = datetime.utcnow()
    week_ago = now - timedelta(days=7)
    print(json.dumps(get_events(week_ago, now), indent=2))
