#!/usr/bin/python
# -*- coding: utf-8 -*-

import urllib2
from HTMLParser import HTMLParser
from htmlentitydefs import name2codepoint
import json


class Crawler(object):
	def __init__(self):
		self.cache = []
		self.urls = []
		self.cachedUrls = self.loadCache()["urls"]
		self.html = ""
		self.files = []
		self.getHTML()

	def getHTML(self):
		print "Getting HTML from page"
		response = urllib2.urlopen('http://www.ibama.gov.br/servicos/editais-de-notificacao-2015')
		self.html = response.read()
		self.getUrls()

	def loadCache(self):
		cacheData = self.cache
		if len(cacheData) == 0:
			cache = open("cache.json","r")
			cacheData = cache.read()
			cacheData = [] if cacheData == "" else json.loads(cacheData) 
			cache.close()
		urls = []
		files = []

		for info in cacheData:
			urls.append(info["url"])
			files.append(info["file"])
		self.cache = cacheData
		return {"urls": urls, "files" : files}

	def loadFromCache(self,url):
		for cacheData in self.cache:
			if url == cacheData["url"]:
				return cacheData["file"]
			
	def saveCache(self):
		jsonFile = open("cache.json",'w')
		jsonFile.write(json.dumps(self.cache))
		jsonFile.close()

	def isCached(self,url):
		for cachedUrl in self.cachedUrls:
			if cachedUrl == url:
				return True

		return False

	def getUrls(self):
		print "Generatig the URLS"

		tmpUrls = self.urls

		class Parser(HTMLParser):
			def handle_starttag(self, tag, attrs):
				if tag == "a":
					href = attrs[0][1].split("/")
					try:
						if href[1] == "phocadownload":
							url = "http://www.ibama.gov.br" + "/".join(href)
							tmpUrls.append(url)
					except IndexError:
						pass

		parser = Parser()
		parser.feed(self.html)

	def getRedirectUrl(self,url):
		response = urllib2.urlopen(url)
		return response.geturl()

	def parseData(self,data):
		year = data[-1]
		month = data[-2]
		day = data[-3]
		return {"day": int(day), "month": int(month), "year" : int(year)}

	def extractData(self,url):
		data = url.split("-")
		try:
			day = data[-3]
		except IndexError:
			data = url.split("_")

		return self.parseData(data)

	def getFiles(self):
		for url in self.urls:
			urlData = self.extractData(url)
			if not self.isCached(url):
				print "\rGetting Real file from (" + url + ")"
				File = self.getRedirectUrl(url)
				data = {"url":url, "file":File}
				self.files.append(File)
				self.cache.append(data)
				self.saveCache()
			else:
				print "\rLoading url (" + url + ") from cache"
				self.files.append(self.loadFromCache(url))
				
		print ""

		return self.files
