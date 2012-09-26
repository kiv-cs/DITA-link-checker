# -*- coding: utf-8 -*-
#This script analyses xrefs in dita files and generates html with marked non-valid xrefs
from os import walk,chdir,access,F_OK,getcwdu,environ
from xml.dom.minidom import *
import os.path
from sys import exit

#do no forget last slash after path!
rootPath = u'D:\SVN REPOS\dita-ets24\DITA\\'
#environ 'PATH TO SCRIPT' is from start.cmd. Thish should be path to directory with this file (dita-xrefs.py) 
outputPath = environ['PATH_TO_SCRIPT']+'\\xrefs.html'

#if filter svn catalogs
svnFilter = True

def getFileContent(path):
	ditaFile = open(path,'r',0777)
	content = ditaFile.read()
	ditaFile.close()
	return content

def getDitaFiles(path):
	'''
	recursively gets all .xml and .dita* files from directory 'path' (excluding .svn dirs if svn_filter=True)
	return list of lists [path to file, filename]
	'''
	ditaFiles=[]
	#tree contains a set of tuples like (catalog_path, [inner catalog names], [inner file names])
	tree=walk(rootPath)
	for entity in iter(tree):
		fileNames=entity[2]
		for fileName in fileNames:
			if (('.dita' in fileName) or ('.xml' in fileName)) and not ('.svn' in entity[0])*svnFilter:
				ditaFiles.append([entity[0]+'\\', fileName])
	return ditaFiles

def getAttributes(string,element,attribute):
	parsedContent = parseString(content)
	elements = parsedContent.getElementsByTagName(element)
	attributes = []
	for node in elements:
		attributes.append(node.getAttribute(attribute))
	return attributes

def renderNodeHtml(nodePath, nodeName,refs,existList):
	output=''
	output+='<b>'+nodePath.replace('\\','/')+nodeName + '</b>\n'
	output+='<ul>\n'
	for ref in refs:
		okPic = existList[refs.index(ref)]
		output+='<li><img src="'+'true'*okPic+'false'*(1-okPic)+'.png">'+getRealPath(nodePath,ref).replace('\\','/')+'</li>\n'
	output+='</ul>\n'
	return output

def writeHtml(html):
	out = open(outputPath,'w')
	out.write(html)
	out.close()

def getRealPath(whereAmIPath,relativeFilePath):
	currentDir=getcwdu()
	chdir(whereAmIPath)
	realPath = os.path.realpath(relativeFilePath)
	chdir(currentDir)
	return realPath

ditaFiles = getDitaFiles(rootPath)
html=''
errorCount=0
for ditaFile in ditaFiles:
	ditaFilePath=ditaFile[0]
	ditaFileName=ditaFile[1]
	content = getFileContent(ditaFilePath+ditaFileName)
	attributes=getAttributes(content, 'link', 'href')
	if attributes:
		existList=[]
		for attribute in attributes:
			refPath=getRealPath(ditaFilePath,attribute)
			existList.append(access(refPath,F_OK))
			#just for console uotput
			if not access(refPath,F_OK):
				errorCount+=1
		html+=renderNodeHtml(ditaFilePath,ditaFileName,attributes,existList)
writeHtml(html)
print 'Done. Error count: %d' % errorCount
print 'Output here: %s' % outputPath
if errorCount:
	exit(1)