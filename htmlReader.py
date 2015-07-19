from HTMLParser import HTMLParser
from htmlentitydefs import name2codepoint
import re
import subprocess
class HTMLConverter(object):

	def read(self,fileName):
		xFile = open(fileName,"r")
		code = xFile.read()
		xFile.close()


		pdfData = []

		class Parser(HTMLParser):
			def handle_data(self, data):
				data = data.replace("\n","")
				if not data == "" and not data == " ":
					pdfData.append(data)

		parser = Parser()
		parser.feed(code)

		pdfData = " ".join(pdfData)

		words = re.split(" +", pdfData)

		return " ".join(words)
	
	def convert(self,xFile):
		htmlFile = xFile.replace("files/","error/").replace("pdf","html")
		command = subprocess.Popen(["pdf2txt.py","-o",htmlFile,xFile], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
		command.communicate()

		return htmlFile