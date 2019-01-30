# -*- coding: utf-8 -*-


import http.cookiejar
import urllib.error
import urllib.request
import urllib.response
import urllib.parse
import ftplib
import os
import zipfile

print("\n.........")

# cookie
cookieJar = http.cookiejar.CookieJar()
handler = urllib.request.HTTPCookieProcessor(cookieJar)
opener = urllib.request.build_opener(handler)

# 登录
usrName = "majunliang"
usrPassword = "888888"
chanDaoDomain = "http://192.168.6.180"
loginURL = "http://192.168.6.180/www/index.php?m=user&f=login"
loginparams = {'domain': "http://192.168.6.180", 'account': usrName, 'password': usrPassword}
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.57 Safari/537.36'}
request = urllib.request.Request(loginURL, urllib.parse.urlencode(loginparams).encode("'utf-8"), headers=headers)
response = opener.open(request)
resStr = response.read()
if b"/www/index.php" in resStr:
    print("1. 登录成功")
else:
    print("登录失败")

# 获取bugid
# http://192.168.6.180/www/index.php?m=bug&f=view&bugID=110953
bugID = "110953"
bugIDURL = "http://192.168.6.180/www/index.php?m=bug&f=view&bugID=" + bugID
request = urllib.request.Request(bugIDURL)
response = opener.open(request)

# 获取页面日志下载地址
import re

html = response.read().decode()

ipsDownloadURL = ""
reg = r'href=.*?.ips'
obj = re.search(reg, html);
if obj.group():
    ipsDownloadURL = obj.group(0)
    arr = ipsDownloadURL.split("'")
    ipsDownloadURL = chanDaoDomain + arr[1]

affectsVersion = ""
reg = r'<th>影响版本</th>\s+<td>\s?(.*?)<'
obj = re.search(reg, html);
if obj.group():
    affectsVersion = obj.group(0)
    arr = affectsVersion.split("\n")
    affectsVersion = arr[-1]
    affectsVersion = affectsVersion.replace(" ", "").strip()
    affectsVersion = affectsVersion.replace("<", "")

if len(ipsDownloadURL) & len(affectsVersion):
    print("2.1 ips日志下载地址成功: %s \n2.2 影响版本: %s " % (ipsDownloadURL, affectsVersion))

ipaDownloadPath = os.path.join(os.path.expanduser('~'), 'Desktop/CrashLog/', bugID)
if not os.path.exists(ipaDownloadPath):
    os.makedirs(ipaDownloadPath)
    print("2.3 创建文件夹 %s" % ipaDownloadPath)
os.chdir(ipaDownloadPath)
# urllib.request.urlretrieve(ipsDownloadURL, "crash.log")

ftp = ftplib.FTP(host="192.168.6.250")
ftp.login("yf_ftp", "lPaYInVgduKrguvS")
ftp.cwd("software/iOS/iOS/")
ipaName = affectsVersion + ".ipa"
dsYMName = affectsVersion + "-dSYM.zip"
# ftp.retrbinary("RETR " + ipaName, open(ipaName, 'wb').write)
# ftp.retrbinary("RETR " + dsYMName, open(dsYMName, 'wb').write)
ftp.close()


# zip_file = zipfile.ZipFile(dsYMName)
# zip_file.extractall()


def symbolicatecrashPath():
    for root, dirs, files in os.walk("/Applications/Xcode.app"):
        for name in [os.path.join(root, file) for file in files]:
            if os.path.basename(name) == "symbolicatecrash" and "SharedFrameworks" in name:
                return name


os.environ["DEVELOPER_DIR"] = "/Applications/XCode.app/Contents/Developer"
os.system(symbolicatecrashPath() + " crash.log iReader.app.dSYM > readable.log")
print(open(readable.log))
print("\n.........")
