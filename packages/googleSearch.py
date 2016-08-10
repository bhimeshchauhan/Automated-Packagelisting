import re
import os
import csv
import argparse
from sys import argv
import requests
from bs4 import BeautifulSoup

done = False
def main(argv):
	parser = argparse.ArgumentParser()
	parser.add_argument("path", help="Path", nargs='*')
	args = parser.parse_args()
	road = ''.join(args.path)
	os.chdir(road)
	writer = None
	header_list = ["Name"]
	writeTo = open('npm.csv', 'wb')
	writer = csv.DictWriter(writeTo, fieldnames=header_list, dialect='excel')
	writer.writeheader()
	os.system("npm ll --parseable > npm.txt")
	with open("npm.txt") as f:
		text = f.read()
		# print(text)
		p = re.compile(
			'(?P<Name>(?<=\w\:).*?(?=\:[a-zA-Z]))')
	mList = []
	for m in re.finditer(p, text):
		for value in m.groupdict():
			if m.groupdict().get(value) not in mList:
				if (m.groupdict().get(value) == 'undefined'):
					continue
				mList.append(m.groupdict().get(value))
				writer.writerow(m.groupdict())
	nameList = (list(set(mList)))
	# print nameList
	searchName = []
	for value in nameList:
		deps = value.split('@', 1)
		searchName.append("https://www.google.com/search?q="+deps[0]+" github")
		# print deps[0]
	count = 0
	listLink = []
	done = False
	for value in searchName:
		# Got the search term to github page (eg: https://www.google.com/search?q=ember-leaflet github)
		page = requests.get(value)
		soup = BeautifulSoup(page.content, "html.parser")
		links = soup.findAll("a")
		# Links found with tag <a></a>
		if links == []:
			print ("NOT GETTING ANYTHING HERE")
			continue
		urls = []
		for link in soup.find_all("a", href=re.compile("(?<=/url\?q=)(htt.*://.*)")):
			# print link["href"]
			# Got URL using link
			split = re.split(":(?=http)", link["href"].replace("/url?q=", ""))
			urls.append(split[0])
		# print (urls[0])
		extractedlink = re.findall('.*(?=&sa.*)', urls[0])
		firstlink = ''.join(extractedlink[0])
		# Got link to github Page from the Google Search
		# print(firstlink)
		#Open this link now to find the link to license page in github if this is a github link else
		# if this is a npmjs link then just get the content and look for license
		linkpage = requests.get(firstlink)
		soup = BeautifulSoup(linkpage.content, "html.parser")
		links = soup.findAll("a")
		# print(links)
		temp = []
		for link in soup.find_all("a", href=re.compile("(.*)")):
			# print (link["href"])
			temp.append(link["href"])
		# Got all the links that are in the Github Page
		# print temp
		linktoLicense = []
		for i, s in enumerate(temp):
			if "LICENSE" in s:
				# print(temp[i])
				linktoLicense.append(temp[i])
			break
		if linktoLicense == []:
			linktoLicense.append("not-a-thing")
		# print(linktoLicense)
		# Extract the License link from Github page
		# for partLink in linktoLicense:
			print(partLink)
			# licensepartlink = (partLink.encode('utf-8'))
			# if licensepartlink == "not-a-thing":
			# 	print("Didnt Find License")
			# else:
			# 	print("I got %s" % "https://github.com" +licensepartlink)
			# break
		# count += 1
		# if count == 5:
		# 	break
	# print listLink

	# for link in listLink:
	# 	linkpage = requests.get(link)
	# 	soup = BeautifulSoup(linkpage.content, "html.parser")
	# 	links = soup.findAll("a")
		# print(links)
		# temp = []
		# for link in soup.find_all("a", href=re.compile("(.*)")):
			# print (link["href"])
			# temp.append(link["href"])
		# print (temp)

	# for i, s in enumerate(temp):
	# 	if "LICENSE" in s:
	# 		# print(temp[i])
	# 		linktoLicense = temp[i]
	# 		# print(linktoLicense)
	# 		break
	#
	# for i, s in enumerate(temp):
	# 	if "github" in s:
	# 		licenseLink = ("https://github.com" + linktoLicense)
	# 		print(licenseLink)
	# 		break


if __name__ == "__main__":
	main(argv)
