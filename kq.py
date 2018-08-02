import csv
import time
import codecs
with open("/Users/eshgfuu/Documents/gaei_kaoqin_ictime_full.csv") as file:
    reader = csv.reader(file)
    next(reader)
    wfile = codecs.open('kq/kq.csv','w','utf-8')
    for row in reader :
        id = row[0]
        date = row[1]
        tobj = time.strptime(row[2], "%Y-%m-%d %H:%M")
        year = tobj.tm_year
        week_day = tobj.tm_wday + 1 
        month = tobj.tm_mon
        mday = tobj.tm_mday
        hour = tobj.tm_hour
        mins = tobj.tm_min
        tstr = time.strftime("%H:%M", tobj)
        qt = 'QT4'
        if month <=3 :
            qt = 'QT1'
        if month>3 and month <=6:
            qt = 'QT2'
        if month>6 and month <=9:
            qt = 'QT3'
        if month>9 and month <=12:
            qt = 'QT4'
        
        flag = 0
        if hour >= 6 and hour < 10 :
            flag = 1
        if hour >=16 and hour <= 23 :
            flag = 2
        wfile.write("%s,%s,%s,%s,%s,%s,%s,%s,%s,%s\n" % (id,date,year,month,mday,week_day,tstr,qt,row[2],flag))
    wfile.close()
