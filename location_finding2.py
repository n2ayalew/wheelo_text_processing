from pprint import pprint
import requests
import re


def get_origin_dest(regex, str):
	return re.findall(regex, str, re.I)

def get_origin(locations, str):
	symbols = re.findall("-|>", str, re.I)
	origins = []

	if (symbols):

		for i in locations:

			not_origin = False

			for j in symbols:

				if (str.find(i) > str.find(j)):

					not_origin = True

			if (not_origin == False):

				origins.append(i)

		return origins

	else:

		tos_present = re.findall("\sto\s", str, re.I)

		if (len(tos_present) == 0):

			return ["Not sure what this is"]

		froms_present = re.findall("\sfrom\s", str, re.I)

		if (len(froms_present) == 0):

			if (len(tos_present) > 1):

				return ["May be round trip or multiple stops"]

			else:

				for i in locations:

						if (str.find(i) < str.find(tos_present[0])):

							origins.append(i)

				return origins

		elif (len(froms_present) > 1):

			return ["May be round trip or multiple stops"]

		else:

			for i in locations:

				pos = str.find(i);
				to_pos = str.find(tos_present[0])
				from_pos = str.find(froms_present[0])

				if (pos < to_pos and pos > from_pos):

					origins.append(i)

			return origins


def get_dest(locations, str):
	symbols = re.findall("-|>", str, re.I)
	dests = []

	if (symbols):

		for i in locations:

			not_dest = False

			for j in symbols:

				if (str.find(i) < str.find(j)):

					not_dest = True

			if (not_dest == False):

				dests.append(i)

		return dests

	else:

		tos_present = re.findall("\sto\s", str, re.I)

		if (len(tos_present) == 0):

			return ["Not sure what this is"]

		froms_present = re.findall("\sfrom\s", str, re.I)

		if (len(froms_present) == 0):

			if (len(tos_present) > 1):

				return ["May be round trip or multiple stops"]

			else:

				for i in locations:

						if (str.find(i) > str.find(tos_present[0])):

							dests.append(i)

				return dests

		elif (len(froms_present) > 1):

			return ["May be round trip or multiple stops"]

		else:

			for i in locations:

				pos = str.find(i);
				to_pos = str.find(tos_present[0])
				from_pos = str.find(froms_present[0])

				if (pos > to_pos and pos > from_pos):

					dests.append(i)

			return dests



def get_other_loc(locations, str):
	return None


def main():
	import sys
	reload(sys)
	sys.setdefaultencoding('UTF-8')
	# Get FB page feed
	r = requests.get("https://graph.facebook.com/v2.8/225049564330328/feed?access_token=EAACEdEose0cBAHo4ZBAzDZCS8ZCdy0zP4Dr4oWE0ZCq67D4dRmpQZCTmu4MlW0U7dkZBNX3sf2yXN2ZCVsStNmqOugnM4fEmLNmOlEGL20gtltZBpS3AoMjVTG4LSWQMxiRZC7zbzZAyIrQ6XwjWFXnAlltFGkE3MEZALNw2OYEErwZCRAWVFm7iNsFQ")
	j = r.json()
	data = j['data']
	next = j['paging']['next']
	prev = j['paging']['previous']
	table = "toronto|markham|waterloo|\sloo|BK|mississauga|scarborough|square one|yorkdale|bk plaza|richmond hill|downtown toronto|stc|pearson|york|ottawa|montreal|london|thornhill|dt toronto|dt|vaughn|fairview mall|fairview|finch station|north york|kingston|hamilton|Laurier|Brampton"

	for i in data:

		print "<---------------------- NEXT POST ----------------------->\n"
		print i['message']
		s = ' '.join(i['message'].split('\n'))
		result = get_origin_dest(table, s)
		result = list(set(result))
		pprint(result)
		origins = get_origin(result, s)

		for origin in origins:
			try:
				result.remove(origin)
			except ValueError:
				continue

		dests = get_dest(result, s)

		for dest in dests:
			try:
				result.remove(dest)
			except ValueError:
				continue

		others = result
		print "\norigins: "
		pprint(origins)
		print "\ndestinations: "
		pprint(dests)
		print "\nothers: "
		pprint(others)
		print "<---------------------- END POST ----------------------->\n"

main()
