import datedelta
from datetime import datetime, timedelta


dt_now = datetime.now()
print(dt_now - timedelta(days = 1)) #yesterday : ayer
print(dt_now)                       #today : hoy
print(dt_now - datedelta.MONTH)     #month ago : hace mes
print(datetime.strptime('01/01/25 12:10:03.234567', '%y/%m/%d %H:%M:%S.%f')) #date from str
