
a_dictionary = {"name" : "John", "age" : 35, "height" : 65}

dict_items = a_dictionary.items()
print(dict_items)


first_two = list(dict_items)[:2]
print(first_two)

##########################################

import os, sys
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)

from helper.translateToUrlPath import translateToUrlPath

#########################################

someURL = 'http:\u002F\u002Fsomewebsite.com\u002Fsomefile.jpg'
import codecs
print(codecs.decode(someURL, 'unicode-escape'))
# prints 'http://somewebsite.com/somefile.jpg'

#########################################

import re
string = 'happy t00 go _--129.129'

print(re.sub(r'[^a-zA-Z ]+', '', string))
print(re.sub(r'[^a-zA-Z-0-9- ]+', '', string))

#########################################

offset_value = 5000

print(offset_value % 5000 == 0 and offset_value > 0)
print(offset_value > 0)

if (offset_value % 5000 == 0) & offset_value > 0:
    print(offset_value)


from datetime import date
today = date.today()
print("Today's date:", today)
