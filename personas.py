from bs4 import BeautifulSoup
import requests
import csv
import os

personas_loc = {"venturer": [],
				"pioneer": [],
				"voyager": [],
				"traditional":[]
				}

def get_personality_raw_data(the_url):
	"Get raw data for each personality from bs4"

	result = requests.get(the_url, auth=('user', 'pass'))
	content = result.content
	soup = BeautifulSoup(content, "html.parser")
	soup.prettify()

	return soup

def add_location(persona, soup):
	"""Creates location list: [0/1(domestic, intl), location, total_score]"""

	locations = soup.find_all("td", {"class":"location"})
	stars = soup.find_all("td", {"class": "starsTotal"})
	
	#adding location
	count = 0 
	for entry in locations:
		for loc in entry.find_all(text = True):
			if loc == " ":
				continue
			count += 1
			if count <= 15:
				personas_loc[persona].append([0, loc.encode('utf-8')])
			else:
				personas_loc[persona].append([1, loc.encode('utf-8')])

	count1 = 0
	count2 = 15 
	for entry in stars:
		for star in entry.find_all(text = True):
			score = star.encode('utf-8')
			if count1 <= 14:
				personas_loc[persona][count1].append(float(score))
				count1 += 1
			else:
				personas_loc[persona][count2].append(float(score))
				count2 += 1


venturer = "http://besttripchoices.com/travel-personalities/venturer/destinations/?phpMyAdmin=3c28893ed0f04e142dff5f914479abd7#intl"
pioneer = "http://besttripchoices.com/travel-personalities/mid-venturer/destinations/?phpMyAdmin=3c28893ed0f04e142dff5f914479abd7#us"
voyager = "http://besttripchoices.com/travel-personalities/centric-venturer/destinations/?phpMyAdmin=3c28893ed0f04e142dff5f914479abd7#us"
traditional = "http://besttripchoices.com/travel-personalities/authentic/destinations/?phpMyAdmin=3c28893ed0f04e142dff5f914479abd7#us"

venturer_soup = get_personality_raw_data(venturer)
pioneer_soup = get_personality_raw_data(pioneer)
voyager_soup = get_personality_raw_data(voyager)
traditional_soup = get_personality_raw_data(traditional)

add_location("venturer", venturer_soup)
add_location("pioneer", pioneer_soup)
add_location("traditional", traditional_soup)
add_location("voyager", voyager_soup)

print personas_loc


# currentPath = os.getcwd()
# csv_columns = ['Category','Location','Score']

# def WriteListToCSV(csv_file,csv_columns,persona):

#     with open(currentPath + csv_file, 'w') as csvfile:
#         writer = csv.writer(csvfile)
#         writer.writerow(csv_columns)
#         for data in personas_loc[persona]:
#             writer.writerow(data)

# WriteListToCSV("/voyager.csv",csv_columns,"voyager")
# WriteListToCSV("/traditional.csv",csv_columns,"traditional")
# WriteListToCSV("/venturer",csv_columns,"venturer")
# WriteListToCSV("/pioneer.csv",csv_columns,"pioneer")



# def get_description_raw_data(the_url):
# 	"""Get raw data for the description for each personality type"""

# 	result = requests.get(the_url, auth=('user', 'pass'))
# 	content = result.content
# 	soup = BeautifulSoup(content, "html.parser")
# 	soup.prettify()

# 	return soup

# def add_description(persona, soup):
# 	"""Add description as a string to the persona_loc dictionary"""

# 	descriptions = []
# 	matches = soup.find_all("p")
# 	for m in matches[9:15]:
# 		for n in m.find_all(text = True):
# 			descriptions.append(n.split("/n/n/n")[0].encode('utf-8'))
# 			break

# 	return descriptions

# description_soup = get_description_raw_data("http://besttripchoices.com/travel-personalities/")
# print add_description("test", description_soup)


