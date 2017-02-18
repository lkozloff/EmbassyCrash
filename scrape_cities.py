import urllib2
from bs4 import BeautifulSoup

BASE_URL = 'https://evisaforms.state.gov/acs/default.asp'
MAGIC_STRING = 'if (selectedvalue =='
MAGIC_CITY_STRING = 'document.PostForm.PostCodeShow.options['
page = urllib2.urlopen(BASE_URL)
soup = BeautifulSoup(page,'lxml')

#Get all the country codes
javascript = soup.prettify()
#print type(javascript)

index = 1

count = javascript.count(MAGIC_STRING,index+1)
cities_by_country = {}

while count:
   index = javascript.find(MAGIC_STRING,index+1)
   #grab the country code and all related city codes
   
   #find place to splice array until by grabbing the next }
   function_close_index = javascript.find('}',index+len(MAGIC_STRING))
   function_body = javascript[index:function_close_index]


   #grab the country code
   cc_start_index = javascript.find('"',index+len(MAGIC_STRING))
   cc_end_index = javascript.find('"',cc_start_index+1)
   cc = javascript[cc_start_index+1:cc_end_index].strip()

   cities_by_country[cc] = []

   city_count = function_body.count(MAGIC_CITY_STRING)
   city_index_start = 0;
   while city_count:
      city_index_start = function_body.find(MAGIC_CITY_STRING,city_index_start+1)
      city_index_end = function_body.find(']',city_index_start+1)
      city_index = function_body[len(MAGIC_CITY_STRING)+city_index_start:city_index_end]

      #try and convert the index into an int
      try:
	city_index_int = int(city_index)
      except ValueError:
	city_index_int = 0

      #only interested in indexes greater than 1
      if(city_index_int >=1):
	 city_name_end = function_body.find(';',city_index_start+1)
         city_name_haystack = function_body[len(MAGIC_CITY_STRING)+city_index_start:city_name_end].split("'")
	 #sorry for the magic numbers..
         city_name = city_name_haystack[1]
         city_code = city_name_haystack[3]
	 
	 #make a tuple and toss it in to our beautiful data structure
	 city_tup = (city_code,city_name)
         cities_by_country[cc].append(city_tup)
      city_count = city_count - 1




   count = count - 1

for country in cities_by_country:
   cities = cities_by_country[country]
   print '---'+country+'---'
   for city_code,city_name in cities:
      print city_code+':'+city_name
