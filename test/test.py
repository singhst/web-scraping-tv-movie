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
