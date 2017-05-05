from pprint import pprint
import requests
import re
import numpy as np

def get_origin_dest(regex, str):
	return re.findall(regex, str, re.I)

def get_origin(locations, preps, str):
	for i in locations:
		for j in preps:
			print "\n"


def main():
	# Get FB page feed
	r = requests.get("https://graph.facebook.com/v2.8/225049564330328/feed?access_token=EAACEdEose0cBAMut6aMZC0qHS8n29hZCZCStqEkU9z4lrevgLGRqQ1ieQvMCgZCWrLCHxZAHy1rttQEhr3QC4HwOU1ZAWAEQZBwhqWFijreP6xXQRQeM0dvbDcAS8zHcwvXrNMHYl0eBOGT2zqrfVOCxfSdS5ZBhPsyDQNsawhSpZAywbGH24E6Ol")
	j = r.json()
	data = j['data']
	next = j['paging']['next']
	prev = j['paging']['previous']
	table = "toronto|markham|waterloo|\Wloo|BK|mississauga|scarborough|square one|yorkdale|bk plaza|richmond hill|downtown toronto|stc|pearson|york|ottawa|montreal|london|thornhill|dt toronto|dt|vaughn|fairview mall|fairview|finch station|north york|kingston|hamilton|Laurier|Brampton"
	prepositions = ['from', 'to', '-->', '->', ]
	for i in data:
		print "<---------------------- NEXT POST ----------------------->\n"
		print i['message']
		s = ' '.join(i['message'].split('\n'))
		result = get_origin_dest(table, s)
		pprint(result)
		#origin = get_origin(result, s)
		#pprint(origin)
		print "<---------------------- END POST ----------------------->\n"

main()
