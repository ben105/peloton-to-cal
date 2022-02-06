import identifier
import datetime
import google_cal
import peloton
import requests
import time


def generate_schedule():
  user = {
      'username': '',
      'password': '',
      'user_id': '',
      'calendar_id': '',
  }
  generate_schedule_for_user(**user)


def generate_schedule_for_user(username, password, user_id, calendar_id):
  cal_events = google_cal.get_events(calendar_id)
  peloton_classes = peloton.get_peloton_classes(username, password, user_id)

  peloton_ids = [identifier.create_id_from_peloton_class(peloton_class) for peloton_class in peloton_classes]
  event_ids = [identifier.create_id_from_calendar_event(event) for event in cal_events]

  destroy_old_events(calendar_id, cal_events, peloton_ids)
  create_new_events(calendar_id, peloton_classes, event_ids)


def destroy_old_events(calendar_id, cal_events, peloton_ids):  
  for event in cal_events:
    event_id = identifier.create_id_from_calendar_event(event)
    if (event_id not in peloton_ids):
      google_cal.delete_event(calendar_id, event)


def create_new_events(calendar_id, peloton_classes, event_ids):
  for peloton_class in peloton_classes:
    peleton_id = identifier.create_id_from_peloton_class(peloton_class)
    if peleton_id not in event_ids:
      google_cal.add_event(calendar_id, peloton_class)


if __name__ == '__main__':
    generate_schedule()
