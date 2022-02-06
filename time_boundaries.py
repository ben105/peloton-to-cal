from datetime import datetime
from pytz import timezone

CURRENT_TIME = datetime.today().astimezone(timezone('US/Pacific'))
BEGINNING_OF_DAY = datetime.combine(CURRENT_TIME, datetime.min.time())
END_OF_DAY = datetime.combine(CURRENT_TIME, datetime.max.time())
