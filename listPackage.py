import os
import json
import argparse
import pandas as pd
from sys import argv
from termcolor import colored, cprint

class packageList():

	def __init__(self, pathtofile = None, pathtofolder = None, npmcontentSplit = None, npmnamelist = None, npmpathList = None,
	    npmlicense = None, npmlinklist = None, finalnpmlink = None, appendednpmlink = None):
		self.pathtofolder = pathtofolder
		self.pathtofile = pathtofile
		self.npmcontentSplit = []
		self.npmnamelist = [] # List of npm package names
		self.npmpathList = [] # List of npm path list
		self.npmlicense = []
		self.npmlinklist = []
		self.finalnpmlink = []
		self.appendednpmlink = []


	def main(self, argv):
		parser = argparse.ArgumentParser(description='Get the npm, bower, pip, homebrew packages and information (Name, License and Home Page Link) installed on your system/project')
		parser.add_argument("--p", nargs= 1,
	                    help='add path to the directory where your project bower.json and package.json is. Use it if you are extracting packages first time')
		parser.add_argument("--f", nargs= 1, help='add path to file to add package info to existing file and get stdout of newly added packages')
		args = parser.parse_args()
		self.pathtofolder = ''.join(args.p)
		self.pathtofile = ''.join(args.f)
		cprint(self.pathtofolder, "yellow")
		cprint(self.pathtofile, "red")
		os.chdir(self.pathtofolder)
	# 	# bowerPath = []
	# 	# bowerPath.append(os.listdir(road+"bower_components"))
	# 	# numbowerFiles = len(os.listdir(road+"bower_components"))


	##### NPM Packages #####
		os.system("npm ll --parseable > npm.txt") # Execute a command to get all the npm packages
		with open("npm.txt") as f:
			npmcontent = f.readlines()
		# cprint(npmcontent, "red")


		for line in npmcontent:
			# print(line)
			self.npmcontentSplit.append(line.split(':'))
		# cprint (npmcontentSplit, "blue")
		for items in self.npmcontentSplit:
			# cprint (items, "green")
			# Check if npm package is already present to remove duplicates and if the path is valid
			if (items[1] not in self.npmnamelist and items[2] != "INVALID"):
				self.npmnamelist.append(items[1])
				self.npmpathList.append(items[0])
		# cprint(npmnamelist, "red") # NPM package names
		# cprint((npmpathList), "blue")
		# Get the list of all the licenses and the links to home page of the packages
		for path in self.npmpathList:
			os.chdir(path)
			with open('package.json') as f:
				data = json.load(f)
				if 'license' in data:
					if 'type' not in data["license"]:
						gotLicense = (data["license"])
						self.npmlicense.append(gotLicense)
						# print(gotLicense)
					else:
						gotLicense = (data["license"]["type"])
						self.npmlicense.append(gotLicense)
						# print(gotLicense)
				elif 'licenses' in data:
					gotLicense = (data["licenses"][0]["type"])
					self.npmlicense.append(gotLicense)
					# print(gotLicense)
				else:
					gotLicense = ("License Not Found")
					self.npmlicense.append(gotLicense)
					# print(gotLicense)
				if 'repository' in data:
					gotnpmLink = (data["repository"])
					# cprint(gotnpmLink, "red")
					if 'url' in gotnpmLink:
						npmLink = (gotnpmLink["url"])
						# cprint(npmLink, "green")
						self.npmlinklist.append(npmLink)
					else:
						nourl = "git+No URL in repository Hash"
						# cprint(nourl, "yellow")
						self.npmlinklist.append(nourl)
				elif 'repository' not in data:
					nohomepage = "git+No Repository in Data Hash"
					# cprint(nohomepage, "yellow")
					self.npmlinklist.append(nohomepage)
		# cprint(npmLicense, "red")
		# cprint(npmlinklist, "green")
		# Get the final package link
		for link in self.npmlinklist:
			# cprint (link, 'red')
			if ('git:' in link.encode('UTF8') and nohomepage not in link.encode('UTF-8')):
				templinkone = (str.replace(link.encode('UTF8'),'git:', 'git+https:'))
				# cprint(templinkone, 'green')
				self.appendednpmlink.append(templinkone)
			elif ('https:' in link.encode('UTF8') and 'git+' not in link.encode('UTF8') and nohomepage not in link.encode(
					'UTF-8') and nourl not in link.encode('UTF-8')):
				templinktwo = (str.replace(link.encode('UTF8'),'https:', 'git+https:'))
				# cprint(templinktwo, 'blue')
				self.appendednpmlink.append(templinktwo)
			elif ('git+ssh:' in link.encode('UTF8')):
				# cprint(link.encode('UTF8'), "red")
				templinkthree = (str.replace(link.encode('UTF8'), 'ssh://git@', 'https://'))
				# cprint(templinkthree, "blue")
				self.appendednpmlink.append(templinkthree)
			else:
				self.appendednpmlink.append(link)
		# cprint (appendednpmlink, 'green')
		for link in self.appendednpmlink:
			splitlink = link.split('+')
			# cprint(splitlink[0], "green")
			if splitlink[1] != None:
				self.finalnpmlink.append(splitlink[1])
			else:
				self.finalnpmlink.append("No HomePage Found")
			# cprint(link, "yellow")
	# cprint(finalnpmlink, "yellow") # List of all npm homepage links

	##### Bower Packages #####
	# 	bowerModule = []
	# 	bowerComponent = []
	# 	licensebower = []
	# 	for i in range(1,numbowerFiles):
	# 		bowerModule.append(bowerPath[0][i])
	# 	# print(bowerModule) #Bower package Names
	#
	# 	for module in bowerModule:
	# 		bowerComponent.append(road+"bower_components/"+module)
	# 	# print(bowerComponent)
	#
	# 	for path in bowerComponent:
	# 		os.chdir(path)
	# 		with open('bower.json') as bf:
	# 			data = json.load(bf)
	# 			# print(path)
	# 			# print data
	# 			if 'license' in data:
	# 				bowerLicense = data["license"]
	# 				licensebower.append(bowerLicense)
	# 				# print(bowerLicense)
	# 			else:
	# 				bowerLicense = ("license not found")
	# 				licensebower.append(bowerLicense)
	# 				# print(bowerLicense)
	#
	#
	# ##### HomeBrew #####
	# 	homebrewname = []
	# 	homebrewlicense = []
	# 	os.chdir(road)
	# 	os.system("brew list > brew.txt")
	# 	with open ('brew.txt') as hbf:
	# 		homebrewdata = hbf.read()
	# 	# print (homebrewdata.split())
	# 	licensehomebrew = "license not found"
	# 	for name in homebrewdata.split():
	# 		homebrewname.append(name)
	# 		homebrewlicense.append(licensehomebrew)
	#
	#
	# ##### pip #####
	# 	pipname = []
	# 	piplicense = []
	# 	os.chdir(road)
	# 	os.system("pip list > pip.txt")
	# 	with open('pip.txt') as pf:
	# 		pipdata = pf.read()
	# 	# print(pipdata)
	# 	licensepip = "license not found"
	# 	for name in pipdata.split("\n"):
	# 		if name != "":
	# 			pipname.append(name)
	# 			piplicense.append(licensepip)
	# 	# print (pipname)

	##### Write Excel File #####



	#### Write Excel Sheet #####
		os.chdir(self.pathtofolder)
		df = pd.DataFrame({'Name': self.npmnamelist, 'License': self.npmlicense, 'Where will this package/library be used? (at least for the first use?)': "LIMS", 'What is the URL for the package or library?': self.finalnpmlink})
		writer = pd.ExcelWriter('SolumPackageList.xlsx', engine='xlsxwriter')
		df.to_excel(writer, sheet_name='packages')
		workbook = writer.book
		worksheet = writer.sheets['packages']
		worksheet.set_column('B:B', 28)
		worksheet.set_column('C:C', 35)
		worksheet.set_column('D:D', 55)
		worksheet.set_column('E:E', 55)
		writer.save()
		os.system("rm %s %s %s" %("npm.txt", "brew.txt", "pip.txt"))

if __name__ == "__main__":
	package = packageList()
	package.main(argv)
