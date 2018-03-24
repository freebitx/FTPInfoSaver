import ftp
import content

import sys
import logging

def PrintDir(dir):
    for d in dir.directories:
        print(d.GetAbsPath())
        PrintDir(d)
    for f in dir.files:
        print("file link: " + f.link)
        print("abs path: " + f.GetAbsPath())
        print("format: " + f.format)
        print("size: " + str(f.size))
        print("timestamp: " + str(f.timestamp.year) + "-" + f.timestamp.month + "-" + str(f.timestamp.day))

def ReadArgs():
    login = ""
    password = ""
    host = ""
    if len(sys.argv) > 1:
        host = sys.argv[1]
    else:
        print("host not set")
        exit()

    if len(sys.argv) > 2:
        login = sys.argv[2]

    if len(sys.argv) > 3:
        password = sys.argv[3]
    return host, login, password

logging.basicConfig(filename="ftp_saver.log", level = logging.DEBUG)

host, login, password = ReadArgs()

storage = ftp.FTPViewer(host, login, password)
storage.Connect()
d = storage.ReadInfo()
PrintDir(d)
