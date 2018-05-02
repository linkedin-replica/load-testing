#  Volume testing

import os
import requests
import time
import matplotlib.pyplot as plt

TimeBeforeRequest = 0
url = 'http://localhost:3000/upload'
nameNodeUrl = 'http://localhost:50070'


def getTime():
    return int(round(time.time()))


fileNames = []

MB = 1024*1024  # 1MB
sz = 1

for i in range(10):
    with open('./files/file_' + str(sz), 'wb') as file:
        file.write(os.urandom(sz * MB))
    fileNames.append('./files/file_' + str(sz))
    print('Created file with size ' + str(sz) + ' MB')
    sz <<= 1

filesUrls = []
x = []
y = []

for fileName in fileNames:
    files = {'media': open(fileName, 'rb')}
    TimeBeforeRequest = getTime()
    req = requests.post(url, files=files)
    print(fileName)
    duration = getTime() - TimeBeforeRequest
    with open('statisticsUpload.txt', 'a') as file:
        file.write('It took ' + str(duration) +
                   ' sec to upload file ' + fileName + '\n')
    x.append(int(fileName.rsplit('_')[1]))
    y.append(duration)
    filesUrls.append((fileName, req.json()['data']['url']))


plt.title('Media server volume testing (Upload)')
plt.xlabel('File size in MB')
plt.ylabel('Time in sec')
plt.plot(x, y, 'ro')
plt.savefig('upload.png')

x = []
y = []

for pair in filesUrls:
    TimeBeforeRequest = getTime()
    print(pair[0])
    req = requests.get(nameNodeUrl + pair[1])
    duration = getTime() - TimeBeforeRequest
    with open('statisticsDownload.txt', 'a') as file:
        file.write('It took ' + str(duration) +
                   ' sec to download file ' + pair[0] + '\n')
    x.append(int(pair[0].rsplit('_')[1]))
    y.append(duration)

plt.clf()
plt.title('Media server volume testing (Download)')
plt.xlabel('File size in MB')
plt.ylabel('Time in sec')
plt.plot(x, y, 'ro')
plt.savefig('download.png')
