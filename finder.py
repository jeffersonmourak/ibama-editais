# -*- coding: utf-8 -*-
from parser import *
from downloader import *
from converter import *
from htmlReader import *
import shutil


class Finder(object):

	def __init__(self):
		self.downloader = Downloader()
		self.crawler = Crawler()
		self.files = self.crawler.getFiles()
		self.downloaded = self.downloader.get(self.files)
		self.htmlConverter = HTMLConverter()

	def getPages(self,xFile):
		pages = pdf_to_csv(xFile)
		print "Getting the pages"
		try:
			if pages[0]:
				return pages
			else:
				return [self.htmlConverter.read(self.htmlConverter.convert(xFile))]
		except IndexError:
			return [self.htmlConverter.read(self.htmlConverter.convert(xFile))]

	def findInFile(self,xFile, xString):
		pages = self.getPages(xFile)
		for index, page in enumerate(pages) :
			print "Finding in the page"
			if xString.upper() in page.upper():
				return index

		return -1
	def writeFile(self,name,data):
		jsonFile = open("data/"+name+".json",'w')
		jsonFile.write(json.dumps(data))
		jsonFile.close()
		return True

	def find(self,value):
		Type = type(value).__name__
		if Type == "str":
			value = [value]
		for info in value:
			data = []
			for File in self.downloaded:
				for keyword in info["keywords"]:
					page = self.findInFile(File,keyword)
					print "finding the client" + info["name"] + " in " + File
					if page > -1:
						data.append({"file" : File,"page": page})
						self.writeFile(info["name"],data)

finder = Finder()

finder.find([{"name":"ibama","keywords":["ibama","MINISTERIO DO MEIO AMBIENTE"]}])