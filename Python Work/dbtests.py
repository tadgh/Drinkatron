import dbinterface
import datetime
import time
db = dbinterface.DB()
endDate = datetime.datetime.now()
#endDate = endDate.strftime('%Y-%m-%d')
startDate = '2013-01-01'
print(startDate)
print(endDate)
res1 = db.getOverallDrinkDataBetweenDates('2013-01-01', '2013-05-01')

for item in res1:
	print(item)