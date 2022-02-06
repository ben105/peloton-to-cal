import datetime
import pytz
import requests

from time_boundaries import BEGINNING_OF_DAY, END_OF_DAY
from pytz import timezone


def create_session(username, password):
  session = requests.Session()
  session.post(
    'https://api.onepeloton.com/auth/login', 
    json={
      'username_or_email': username,
      'password': password,
    }
  )
  return session


def get_peloton_classes(username, password, user_id):
  session = create_session(username, password)

  ql_payload = {
    "operationName": "UserScheduledClasses",
    "variables": {
        "id": user_id,
        "startTime": f"{BEGINNING_OF_DAY.strftime('%c')} GMT-0800",
        "endTime": f"{END_OF_DAY.strftime('%c')} GMT-0800"
    },
    "query":"query UserScheduledClasses($id: ID!, $startTime: DateTime!, $endTime: DateTime!) {\n  user(id: $id) {\n    scheduledClasses(input: {startTime: $startTime, endTime: $endTime}) {\n      ...ScheduleClassList\n      __typename\n    }\n    __typename\n  }\n}\n\nfragment ScheduleClassList on ScheduledClassList {\n  scheduledClasses {\n    ...ScheduledClassDetails\n    __typename\n  }\n  __typename\n}\n\nfragment ScheduledClassDetails on ScheduledClass {\n  id\n  isScheduled\n  joinToken\n  pelotonId\n  pelotonClass {\n    classId\n    description\n    fitnessDiscipline {\n      ...FitnessDiscipline\n      __typename\n    }\n    id\n    originLocale {\n      code\n      __typename\n    }\n    title\n    ... on LiveClass {\n      airTime\n      actualStartTime\n      difficultyLevel {\n        ...DifficultyLevel\n        __typename\n      }\n      instructor {\n        ...Instructor\n        __typename\n      }\n      liveClassCategory\n      explicitRating\n      __typename\n    }\n    ... on OnDemandInstructorClass {\n      airTime\n      difficultyLevel {\n        ...DifficultyLevel\n        __typename\n      }\n      instructor {\n        ...Instructor\n        __typename\n      }\n      explicitRating\n      __typename\n    }\n    __typename\n  }\n  scheduleSource\n  scheduledStartTime\n  scheduledEndTime\n  scheduledUsers {\n    totalCount\n    edges {\n      ...ScheduledUser\n      __typename\n    }\n    __typename\n  }\n  __typename\n}\n\nfragment FitnessDiscipline on FitnessDiscipline {\n  displayName\n  slug\n  __typename\n}\n\nfragment DifficultyLevel on DifficultyLevel {\n  displayName\n  slug\n  __typename\n}\n\nfragment Instructor on Instructor {\n  assets {\n    profileImage {\n      location\n      __typename\n    }\n    __typename\n  }\n  name\n  __typename\n}\n\nfragment ScheduledUser on UserEdge {\n  node {\n    id\n    assets {\n      image {\n        location\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n  __typename\n}\n"}

  resp = session.post(
    'https://gql-graphql-gateway.prod.k8s.onepeloton.com/graphql', 
    json=ql_payload, 
    headers={
      'peloton-platform': 'web', 
      # Not sure if this will break at some point...
      'peloton-client-date': datetime.datetime.now().astimezone(pytz.utc).isoformat()
    }
  )

  peloton_classes = resp.json()['data']['user']['scheduledClasses']['scheduledClasses']

  return [{
    'description':  peloton_class['pelotonClass']['description'],
    'title': peloton_class['pelotonClass']['title'],
    'startTime': peloton_class['scheduledStartTime'],
    'endTime': peloton_class['scheduledEndTime'],
  } for peloton_class in peloton_classes]