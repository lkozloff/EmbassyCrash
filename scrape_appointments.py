# encoding=utf8
import urllib2
from bs4 import BeautifulSoup
import cookielib
import re
import datetime
from datetime import date

MONTHS_IN_ADVANCE = 2 #max number of months to check
BASE_URL = 'https://evisaforms.state.gov/acs/default.asp'
CALENDAR_BASE_URL = 'https://evisaforms.state.gov/acs/make_calendar.asp'
APPOINTMENT_BASE_URL = 'https://evisaforms.state.gov/acs/' 

# Service Types:
# AA = Passport Services
# 02B = Birth Abroad
# 09 = Notary and other
#
# Type:
# 1 = Passport Appointment
# 2 = Birth Abroad
# 3 = Notary and other
# 4 = Add visa pages (no longer possible)
# 
# Month (as you would expect)
# Year (as you would Expect)
#
# To access system:
# Go to: https://evisaforms.state.gov/acs/default.asp?PostCode=BNK&CountryCode=THAI to grab session cookie
# Then to: https://evisaforms.state.gov/acs/make_calendar.asp?nMonth=3&nYear=2017&type=2&servicetype=02B&pc=BNK
# to grab calendars
#  
def pullAppointmentsByType(postcode='BNK',countrycode='THAI',servicetype='02B',type_=2,month=5,year=2017): 

   cookies = cookielib.LWPCookieJar()
   handlers = [
      urllib2.HTTPHandler(),
      urllib2.HTTPSHandler(),
      urllib2.HTTPCookieProcessor(cookies),
   ]
   opener = urllib2.build_opener(*handlers)
   full_url = BASE_URL+'?PostCode='+postcode+'&CountryCode='+countrycode

   #print full_url

   req = urllib2.Request(full_url)
   #don't care about these contents, actually
   page = opener.open(req)


   calendar_url = CALENDAR_BASE_URL+'?nMonth='+str(month)+'&nYear='+str(year)+'&type='+str(type_)+'&servicetype='+servicetype+'&pc='+postcode

   req = urllib2.Request(calendar_url)
   page = opener.open(req)
   soup = BeautifulSoup(page,'lxml')
   appointments = soup.find_all('td',{'bgcolor':'#ffffc0'})

   appointment_data = {}
   numbers = re.compile('\d+(?:\.\d+)?')
   for appointment in appointments:
      appt = appointment.find('a')
      try:
	   appointment_date = appt.contents[0]
	   appointment_url = appt.get('href')
	   appointment_available = numbers.findall(appointment.find('div').a.contents[0])[0]
	   appointment_data[appointment_date] = {'available':appointment_available,'url':APPOINTMENT_BASE_URL+appointment_url}
      except (TypeError, AttributeError):
          pass

   return appointment_data      


def checkAvailable(start_date='2017-02-15', end_date='2017-08-29',postcode='BNK',countrycode='THAI',servicetype='02B',type_=2):

   # get set up 
   today = date.today()
   startdate = datetime.datetime.strptime(start_date,'%Y-%m-%d')
   enddate = datetime.datetime.strptime(end_date,'%Y-%m-%d')

   # figure out which months we need to pull
   if enddate.year >= startdate.year:

      # 0 = current month only, 1 = current month and next month
      months_to_grab = enddate.month - today.month 
      if months_to_grab > MONTHS_IN_ADVANCE:
         months_to_grab = MONTHS_IN_ADVANCE

      appts = {}
      while months_to_grab >= 0:
          cur_month = today.month + months_to_grab
          #print 'pulling: ',
	  #print cur_month
  
          appts[cur_month] = pullAppointmentsByType(postcode,countrycode,servicetype,type_, cur_month,today.year)
          months_to_grab = months_to_grab - 1

      
   else:
	#shouldn't have run this in the first place!
	return None

   return appts


def main():
    appts = checkAvailable('2017-05-01','2017-07-15','BRA','BRZL','02B','2')
    print appts
    for month in sorted(appts,key=int):
       print "Days with appointments available in: "+str(month)+": " + str(len(appts[month]))
       for date in sorted(appts[month],key=int):
          print date,
          print '(Available:',appts[month][date]['available'],')'
#	  print 'URL:',month[date]['url']

if __name__ == "__main__": main()
