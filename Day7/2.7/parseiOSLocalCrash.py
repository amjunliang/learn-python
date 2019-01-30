#!/usr/bin/env python
#coding:utf-8

import os
import sys
import re
import urllib2
import urllib
import cookielib
import ftplib
import zipfile
import shutil

'''
使用方法 python parseiOSCrashLog.py 74173
或者先执行chmod +x parseiOSCrashLog.py再执行 ./parseiOSCrashLog.py 74173
74173为禅道bug id

参考文献:
1.http://www.jianshu.com/p/e428501ff278
2.https://stackoverflow.com/questions/1506010/how-to-use-export-with-python-on-linux
3.http://blog.csdn.net/figo829/article/details/18728381
4.https://stackoverflow.com/questions/34275782/how-to-get-desktop-location-using-python

注意：
loginurl 和 bugidurl可能发生改变(直接修改url路径即可)
登录禅道的账户和密码可能发生改变(之间替换账户和密码)
禅道网页中的附件和对应的版本号的结构可能发生改变(这个需要更改getLogInfos函数中的正则匹配了)
made by zgy 2017/07/31
'''

loginurl = 'http://192.168.6.180/www/index.php?m=user&f=login'
bugidurl = 'http://192.168.6.180/www/index.php?m=bug&f=view&t=html&id='
loginDomain = 'http://192.168.6.180'
downloadsDir = 'crashLog'
username = 'zhaoguangyu'
password = '999999'

## 这段代码是用于解决中文报错的问题  
reload(sys)  
sys.setdefaultencoding("utf8")  
#####################################################

class ParseCrshLog(object):
	
	def __init__(self):
		self.dsymName = ''
		self.crashFilePath = ''

	def downloadDSYMAndIPAFile(self, fileName):
		'''下载dSYM文件和ipa文件'''
		path = 'software/iOS/iOS/'
		#filename = 'iOS_V6.8.0_Test_build1398_Debug_20170721_0958.ipa'

		#ftp = ftplib.FTP("ftp://192.168.6.250") 
		ftp = ftplib.FTP("192.168.6.250") 
		ftp.login("yf_ftp", "lPaYInVgduKrguvS") 
		ftp.cwd(path)
		fileIpaName = fileName + ".ipa"
		fileDsymName = fileName + "-dSYM.zip"
		try:
			ftp.retrbinary("RETR " + fileIpaName, open(fileIpaName, 'wb').write)
			ftp.retrbinary("RETR " + fileDsymName, open(fileDsymName, 'wb').write)
		except:
			print"❌ 错误--------打开ipa文件或dSYM文件失败，ipa路径为：%s, 请检查该bug对应的禅道页面中\"影响版本\"的内容填写是否正确" %(fileIpaName)
			exit(1)
		ftp.quit()

	def report(count, blockSize, totalSize):
		percent = int(count*blockSize*100/totalSize)
		sys.stdout.write("\r%d%%" % percent + ' complete')
		sys.stdout.flush()


	def un_zip(self, file_name):
		"""unzip zip file"""
		zip_file = zipfile.ZipFile(file_name)
		#if os.path.isdir(file_name + "_files"):
		#	pass
		#else:
		#	os.mkdir(file_name + "_files")
		for names in zip_file.namelist():
			#zip_file.extract(names,file_name + "_files/")
			zip_file.extract(names)
		zip_file.close()

	def getSymbolicatieCrashpath(self):
		'''获取symbolicatecrash的文件路径'''
		from os.path import basename
		for dpath, dnames, fnames in os.walk("/Applications/Xcode.app"):
			for i, fname in enumerate([os.path.join(dpath, fname) for fname in fnames]):
				if basename(fname) == "symbolicatecrash" and "iPhoneSimulator" in fname:
					return fname

	def symbolicatiecrashlog(self):
		'''通过symbolicatecrash解析日志'''
		''' 已改为每次获取路径, 每次慢几秒，可以忽略，为了以后的扩展。如果觉得慢，再改为写死的。 
		#此方法查找symbolicatecrash的文件路径，每次查找时间比较慢外加此路径变化几率很小，如果因为xcode版本升级而导致这个路径改变，需要手动运行下面命令，并将最新路径填入到cp 行中
		#find /Applications/Xcode.app -name symbolicatecrash -type f
		#os.system("cp /Applications/Xcode.app/Contents/Developer/Platforms/iPhoneSimulator.platform/Developer/Library/PrivateFrameworks/DVTFoundation.framework/symbolicatecrash .")
		'''
		from shutil import copy
		copy(self.getSymbolicatieCrashpath(), "./")
		os.environ["DEVELOPER_DIR"] = "/Applications/XCode.app/Contents/Developer"
#os.putenv("DEVELOPER_DIR", "/Applications/XCode.app/Contents/Developer")
		os.system("./symbolicatecrash crash.log iReader.app.dSYM > readable.log")
		os.system("open readable.log")

	def copyCrashLog(self, crashLogFile):
		from shutil import copy
		copy(crashLogFile, "./crash.log")
	
	def removeFileInFirstDir(self, targetDir):
		'''删除一级目录中的所有文件'''
		for file in os.listdir(targetDir): 
			targetFile = os.path.join(targetDir,  file)
			if os.path.isfile(targetFile):
				os.remove(targetFile)
	
	def mkDownloadDirectory(self):
		'''在桌面上创建下载的目录，目录结构为 ~/Desktop/downloadsDir/74173(dsymName)'''
		desktop = os.path.join(os.path.join(os.path.expanduser('~')), 'Desktop')
		downloadPath = os.path.join(os.path.join(desktop, downloadsDir), dsymName)
		if not os.path.exists(downloadPath):
			os.makedirs(downloadPath)
		return downloadPath

	def changeWorkDirectory(self, downloadPath):
		'''修改程序的运行目录'''
		os.chdir(downloadPath)
		
		#hutil.copy(downloadsDir, os.path.join(os.environ["HOMEPATH"], "Desktop"))
		#downloadPath = os.path.dirname(os.path.realpath(__file__)
		#os.mkdirs("Downloads")

if __name__ == '__main__':
	if len(sys.argv) < 3:
		crashFilePath = raw_input('请拖入crash文件: ')
		dsymName = raw_input('请输入dSYM文件名称,即发包邮件中的文件名称,去掉后缀名，会自动从ftp服务器下载该文件，例如iOS_V7.5.0_Test_build1654__Debug_20180319_1414 : ')
	else:
		crashFilePath = sys.argv[1]		
		dsymName = sys.argv[2]

	crashFilePath = crashFilePath.strip()
	dsymName = dsymName.strip()

	parse = ParseCrshLog()
	parse.dsymName = dsymName.strip()
	parse.changeWorkDirectory(parse.mkDownloadDirectory())
	print "正在下载ipa文件和dSYM文件......"
	parse.downloadDSYMAndIPAFile(dsymName)
	print "下载ipa文件和dSYM文件成功!"
	print "解压dSYM文件......"
	parse.un_zip(dsymName + '-dSYM.zip')
	print "解析日志......"
	parse.copyCrashLog(crashFilePath)
	parse.symbolicatiecrashlog()
	print "解析日志成功，名称为 readable.log, 中间文件及结果保存在\"桌面/%s/%s\"文件夹中" %(downloadsDir, dsymName)
