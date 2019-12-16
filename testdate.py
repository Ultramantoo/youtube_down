import  datetime
from dateutil.relativedelta import relativedelta
#以当前时间作为起始点，days=-7向前偏移7天，days=7向后偏移7天
time_now = datetime.datetime.now()
print(time_now)
time = (time_now+datetime.timedelta(hours=-13)).strftime("%Y%m%d")
print(time)
#以当前时间为起始点，偏移一个月
time_1=(time_now+relativedelta(months=-1)).strftime("%Y%m%d")
print(time_1)
