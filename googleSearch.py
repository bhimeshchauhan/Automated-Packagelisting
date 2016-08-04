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
	count = 0
	listLink = []
	done = False
	for value in searchName:
		# print (value)
		page = requests.get(value)
		# print (value)
		soup = BeautifulSoup(page.content, "html.parser")
		links = soup.findAll("a")
		# print(links)
		if links == []:
			print ("NOT GETTING ANYTHING HERE")
			continue
		urls = []
		for link in soup.find_all("a", href=re.compile("(?<=/url\?q=)(htt.*://.*)")):
			# print link["href"]
			split = re.split(":(?=http)", link["href"].replace("/url?q=", ""))
			# print split
			urls.append(split[0])
		# print (urls[0])
		extractedlink = re.findall('.*(?=&sa.*)', urls[0])
		firstlink = ''.join(extractedlink[0])
		print((firstlink))
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
		for i, s in enumerate(temp):
			if "LICENSE" in s:
				# print(temp[i])
				linktoLicense = temp[i]
				print(linktoLicense)
				break


		listLink.append(firstlink)
		count += 1
		if count == 3:
			break
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
