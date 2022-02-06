import dateutil.parser
import pytz

def create_id_from_peloton_class(_class):
  start = date_string_to_common(_class['startTime'])
  end = date_string_to_common(_class['endTime'])
  return f'{_class["title"]}__{start}__{end}'

def create_id_from_calendar_event(event):
  start = date_string_to_common(event['start']['dateTime'])
  end = date_string_to_common(event['end']['dateTime'])
  return f'{event["summary"]}__{start}__{end}'

def date_string_to_common(date_str):
  parsed_date = dateutil.parser.isoparse(date_str)
  parsed_date = parsed_date.astimezone(pytz.utc)
  return parsed_date.strftime('%c')
