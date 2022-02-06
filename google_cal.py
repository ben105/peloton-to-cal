import requests

from google.auth.transport import requests as auth_requests
from google.oauth2 import service_account
from time_boundaries import BEGINNING_OF_DAY, END_OF_DAY


SERVICE_ACCOUNT = ''

CREDENTIAL_SCOPES = ["https://www.googleapis.com/auth/calendar"] 
CREDENTIALS_KEY_PATH = 'service_account_key.json'


def get_default_token():
  credentials = service_account.Credentials.from_service_account_file(
      CREDENTIALS_KEY_PATH, scopes=CREDENTIAL_SCOPES)
  credentials.refresh(auth_requests.Request())
  return credentials.token


HEADERS = {
  'Authorization': 'Bearer {}'.format(get_default_token()),
  'content-type': 'application/json'
}


def get_events(calendar_id):
  resp = requests.get(
    f'https://www.googleapis.com/calendar/v3/calendars/{calendar_id}/events?timeMin={BEGINNING_OF_DAY.strftime("%Y-%m-%dT%X-0800")}&timeMax={END_OF_DAY.strftime("%Y-%m-%dT%X-0800")}&showDeleted=false',
    headers=HEADERS
  )
  resp.raise_for_status()
  return [item for item in resp.json()['items'] if item['creator']['email'] == SERVICE_ACCOUNT]


def add_event(calendar_id, peloton_class):
  payload = {
    "end": {
      "dateTime": peloton_class['endTime'],
    },
    "start": {
      "dateTime": peloton_class['startTime'],
    },
    "summary": peloton_class['title'],
    "description": peloton_class['description']
  }
  resp = requests.post(f'https://www.googleapis.com/calendar/v3/calendars/{calendar_id}/events', json=payload, headers=HEADERS)
  resp.raise_for_status()


def delete_event(calendar_id, event):
  resp = requests.delete(f'https://www.googleapis.com/calendar/v3/calendars/{calendar_id}/events/{event["id"]}', headers=HEADERS)
  resp.raise_for_status()