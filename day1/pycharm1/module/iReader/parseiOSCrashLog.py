#!/usr/bin/env python
# coding:utf-8

import ftplib
import os
import re
import sys
import urllib
import zipfile

import cookielib
import urllib2

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
        self.name = ''
        self.passwprd = ''
        self.domain = ''
        self.bugId = ''

        self.cj = cookielib.LWPCookieJar()
        self.opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(self.cj))
        urllib2.install_opener(self.opener)

    def setLoginInfo(self, username, password, domain, bugId):
        '''设置用户登录信息'''
        self.name = username
        self.pwd = password
        self.domain = domain
        self.bugId = bugId

    def login(self):
        '''登录网站'''
        loginparams = {'domain': self.domain, 'account': self.name, 'password': self.pwd}
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.57 Safari/537.36'}
        req = urllib2.Request(loginurl, urllib.urlencode(loginparams), headers=headers)
        response = urllib2.urlopen(req)
        self.operate = self.opener.open(req)
        thePage = response.read()

    # todo: 有无日志判断
    def getLogInfos(self):
        '''进入禅道对应的bugid网页，并获取对应的版本号和错误日志'''
        req = urllib2.Request(bugidurl + bugId, urllib.urlencode({}), {})
        response = urllib2.urlopen(req)
        self.operate = self.opener.open(req)
        thePage = response.read()

        regex = re.compile(r'<th>影响版本</th>\s+<td>\s?(.*?)<', re.MULTILINE)
        matches = [m.groups() for m in regex.finditer(thePage)]
        version = ''
        for m in matches:
            version = m[0].strip()

        # 获取错误日志的下载地址
        regex = re.compile(r"<a href='(.*?)'.*\.ips", re.MULTILINE)
        matches = [m.groups() for m in regex.finditer(thePage)]
        logUrl = ''
        for m in matches:
            logUrl = loginDomain + m[0]
        return [version, logUrl]

    def downloadLog(self, logUrl):
        '''从禅道下载log日志'''
        req = urllib2.Request(logUrl, urllib.urlencode({}), {})
        response = urllib2.urlopen(req)
        self.operate = self.opener.open(req)
        with open("crash.log", "wb") as code:
            code.write(response.read())

    def downloadDSYMAndIPAFile(self, fileName):
        '''下载dSYM文件和ipa文件'''
        path = 'software/iOS/iOS/'
        # filename = 'iOS_V6.8.0_Test_build1398_Debug_20170721_0958.ipa'

        # ftp = ftplib.FTP("ftp://192.168.6.250")
        ftp = ftplib.FTP("192.168.6.250")
        ftp.login("yf_ftp", "lPaYInVgduKrguvS")
        ftp.cwd(path)
        fileIpaName = fileName + ".ipa"
        fileDsymName = fileName + "-dSYM.zip"
        try:
            ftp.retrbinary("RETR " + fileIpaName, open(fileIpaName, 'wb').write)
            ftp.retrbinary("RETR " + fileDsymName, open(fileDsymName, 'wb').write)
        except:
            print
            "❌ 错误--------打开ipa文件或dSYM文件失败，ipa路径为：%s, 请检查该bug对应的禅道页面中\"影响版本\"的内容填写是否正确" % (fileIpaName)
            exit(1)
        ftp.quit()

    def report(count, blockSize, totalSize):
        percent = int(count * blockSize * 100 / totalSize)
        sys.stdout.write("\r%d%%" % percent + ' complete')
        sys.stdout.flush()

    def un_zip(self, file_name):
        """unzip zip file"""
        zip_file = zipfile.ZipFile(file_name)
        # if os.path.isdir(file_name + "_files"):
        #	pass
        # else:
        #	os.mkdir(file_name + "_files")
        for names in zip_file.namelist():
            # zip_file.extract(names,file_name + "_files/")
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
        # os.putenv("DEVELOPER_DIR", "/Applications/XCode.app/Contents/Developer")
        os.system("./symbolicatecrash crash.log iReader.app.dSYM > readable.log")
        os.system("open readable.log")

    def removeFileInFirstDir(self, targetDir):
        '''删除一级目录中的所有文件'''
        for file in os.listdir(targetDir):
            targetFile = os.path.join(targetDir, file)
            if os.path.isfile(targetFile):
                os.remove(targetFile)

    def mkDownloadDirectory(self):
        '''在桌面上创建下载的目录，目录结构为 ~/Desktop/downloadsDir/74173(bugId)'''
        desktop = os.path.join(os.path.join(os.path.expanduser('~')), 'Desktop')
        downloadPath = os.path.join(os.path.join(desktop, downloadsDir), bugId)
        if not os.path.exists(downloadPath):
            os.makedirs(downloadPath)
        return downloadPath

    def changeWorkDirectory(self, downloadPath):
        '''修改程序的运行目录'''
        os.chdir(downloadPath)


# hutil.copy(downloadsDir, os.path.join(os.environ["HOMEPATH"], "Desktop"))
# downloadPath = os.path.dirname(os.path.realpath(__file__)
# os.mkdirs("Downloads")


if __name__ == '__main__':
    if len(sys.argv) < 2:
        # print "请输入bug id后重试"
        # print "参考样例： \npython parseiOSCrashLog.py 74695"
        bugId = raw_input('请输入禅道bug id: ')
    # exit(1)
    else:
        bugId = sys.argv[1]

    parse = ParseCrshLog()
    print
    "获取禅道bug id: %s的数据信息" % (bugId)
    domain = loginDomain
    parse.setLoginInfo(username, password, domain, bugId)
    parse.login()
    arr = parse.getLogInfos()
    if len(arr[0]) == 0:
        print
        "未获取到该bug id对应的影响版本的版本号"
        exit(1)
    print
    "版本号为: %s" % (arr[0])
    if len(arr[1]) == 0:
        print
        "该bug id对应的网址不包含crash日志文件"
        print
        "对应禅道地址为：%s" % (bugidurl + bugId)
        exit(1)
    print
    "crash日志文件地址为: %s" % (arr[1])
    parse.changeWorkDirectory(parse.mkDownloadDirectory())
    print
    "正在下载crash日志文件......"
    parse.downloadLog(arr[1])
    print
    "下载crash日志文件成功......"
    print
    "正在下载ipa文件和dSYM文件......"
    parse.downloadDSYMAndIPAFile(arr[0])
    print
    "下载ipa文件和dSYM文件成功!"
    print
    "解压dSYM文件......"
    parse.un_zip(arr[0] + '-dSYM.zip')
    print
    "解析日志......"
    parse.symbolicatiecrashlog()
    print
    "解析日志成功，名称为 readable.log, 中间文件及结果保存在\"桌面/%s/%s\"文件夹中" % (downloadsDir, bugId)
