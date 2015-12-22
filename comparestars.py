# Yelp Python App
# takes in a .csv of roadfood restaurants
# compares their rating on yelp

### extras for next time (add in comments): ###
	# ks test
	# scatter plot box-and-whiskers plot
	# actually plot restaurants

### not needed, maybe ###
	# ? vertically align submit buttons
	# ? squares fix vertical alignment

### to add: ###
	# label national bar chart
		# also label other graphs
	# proper quotes

	# scatter plot number ???

import sample
import re
import csv
import requests_cache
import requests
import json

restaurants_array = []

with open('roadhouse.csv', 'rb') as roadhouse:
	rest = csv.reader(roadhouse)
	for row in rest:
		restaurants_array.append(row)

restaurants_dict = []
restaurants_array = restaurants_array[1:]
bad_restaurants = []
# print restaurants_array[0]

# problematic: [1, 3, 8, 19, 20, 24, 45, 45, 59, 60, 67, 74]
# after barbeque: [8, 19, 20, 24, 45, 45, 59, 60, 74]
# after space: [8, 19, 20, 24, 45, 45, 60, 67, 74]


fout = open('restaurants.json','a')
# fout.write("[")

print restaurants_array[299]
print restaurants_array[598]
print restaurants_array[898]
print restaurants_array[1098]
print restaurants_array[1298]
print restaurants_array[1498]
print restaurants_array[1698]
print restaurants_array[len(restaurants_array)-1]
restaurants_array = restaurants_array[1698:]
# print restaurants_array[299]

for i in range(0, len(restaurants_array)):
#bad restaurants: [19, 60, 67, 124, 131, 147, 225, 242, 251, 269, 295]
# 299 + [42, 43, 46, 54, 59, 75, 76, 104, 199, 216, 254, 259, 274, 281, 282, 285]
# 598 + [17, 28, 42, 48, 50, 59, 60, 74, 118, 143, 182, 196, 224, 240, 254, 269]
# 898 + [59, 62, 97, 101, 139, 164, 188]
# 1098 + [2, 9, 20, 34, 136, 186]
# 1298 + [26, 102, 132]
# 1498 + [22, 33, 36, 39, 55, 57, 83, 144, 148, 155]
# 1698 + [48, 91, 131, 132]
# for i in (21, 25):
	#print restaurants_array[i]
	restaurants_dict.append({"name": restaurants_array[i][2].split(" - ")[0][1:], "longitude": restaurants_array[i][0], 
							 "latitude": restaurants_array[i][1]
							 })
	try:
		restaurants_dict[i]["phone"] = re.sub(r"\D", "", restaurants_array[i][2].split("{")[1])
	except IndexError:
		restaurants_dict[i]["phone"] = "0000000000"
	restaurants_dict[i]["address"] = restaurants_array[i][2].split(" - ")[1].split(" {")[0].replace(":", ",")
	try:
		temps = sample.search(restaurants_dict[i]['name'], restaurants_dict[i]['address'])
		print "for restaurant " + str(i+1) + ":"
		# print temps
		# print restaurants_dict[i]
		if temps[u'businesses'] == []:
			# bad_restaurants.append(i+1)
			pass
		else:
			try:
				temps[u'businesses'] = temps[u'businesses'][0]
			except IndexError:
				# bad_restaurants.append(i+1)
				pass
			try:
				c = temps[u'businesses'][u'phone']
			except KeyError:
				# bad_restaurants.append(i+1)
				temps[u'businesses'][u'phone'] = "0000000001"
			if temps[u'businesses'][u'phone'] == restaurants_dict[i]['phone'] or temps[u'businesses'][u'name'].replace(" ", "") == restaurants_dict[i]['name'].replace(" ", ""):
				restaurants_dict[i]["rating"] = temps[u'businesses'][u'rating']
				restaurants_dict[i]["review_count"] = temps[u'businesses'][u'review_count']
			else:
				print restaurants_dict[i]
				print temps[u'businesses']
				manual_confirmation = raw_input("I'm going to ask you to confirm if the first choice is in fact actually correct. \n")
				if manual_confirmation == 'yes' or manual_confirmation == 'y':
					restaurants_dict[i]["rating"] = temps[u'businesses'][u'rating']
					restaurants_dict[i]["review_count"] = temps[u'businesses'][u'review_count']
				else:
					print "Possible conflict at restaurant %s" % str(i+1)
					bad_restaurants.append(i+1)
	except:
		print restaurants_array[i]
		pass
	# fout.write(str(restaurants_dict[i]))
	# fout.write(",")

# fout.write("]")
# fout.flush()

fout.write(json.dumps(restaurants_dict))
fout.close()

print json.dumps(restaurants_dict)
print bad_restaurants


