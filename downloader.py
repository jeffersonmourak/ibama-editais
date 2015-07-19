import urllib
import os.path

class Downloader(object):

	def getFile(self,url,index,length):
		fileName = "files/" + url.split("/")[-1]
		print "\rGetting File " + str(index) + " of " + str(length),
		if not os.path.exists(fileName):
			status = urllib.urlopen(url).getcode()
			if(status == 200):
				urllib.urlretrieve (url,fileName)
				return fileName
			else:
				print "\rError to download file " + str(index),
				return False
		return fileName

	def get(self,urls):
		Type = type(urls).__name__
		files = []
		if Type == "str":
			return self.getFile(urls,1,1)
		elif Type == "list":
			for i in range(len(urls)):
				url = urls[i]
				files.append(self.getFile(url,i + 1,len(urls)))
			print ""
			return files

