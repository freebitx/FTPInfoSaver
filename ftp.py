import content

import ftplib
import logging
import os

class FTPViewer:
    COUNT_FILE_INFO = 9 # count of words in content info string
    def __init__(self, host, login = '', password = ''):
        self.host = host
        self.login = login
        self.password = password

    def __del__(self):
        self.ftp.close()
        self.ftp.quit()

    def Connect(self):
        self.ftp = ftplib.FTP(self.host)
        self.ftp.login(self.login, self.password)
        logging.debug('host: ' + self.host)
    
    def ReadInfo(self):
        dirs = self._processDirectory()
        return dirs

    def _retrieveInfo(self, name):
        result = content.BaseInfo(name)
        
        result.size = self.ftp.size(name)
        return result

    def _retrieveFileInfo(self, parent_dir, str):
        infos = str.split(';')
        if len(infos) < self.COUNT_FILE_INFO:
            logging.error('unknown info format')
            return None
        file_info = content.FileInfo(parent_dir, infos[8])
        file_info.link = 'ftp://' + self.login + ':' + self.password + '@' + self.host + '/' + file_info.GetAbsPath()
        file_info.timestamp.month = infos[5]
        file_info.timestamp.day = int(infos[6])
        file_info.timestamp.year = int(infos[7])
        name_parts = file_info.name.split('.')
        parts_count = len(name_parts)
        if (parts_count > 1) or (file_info.name[0] == '.' and parts_count > 2):
            file_info.format = name_parts[len(name_parts) - 1]
        try:
            file_info.size = self.ftp.size(file_info.GetAbsPath())
        except ftplib.all_errors as e:
            logging.error('error while getting file size: ' + repr(e))
        return file_info

    def _retrieveDirInfo(self, parent_dir, str):
        if str == '':
            return content.DirectoryInfo('', '')
        infos = str.split(';')
        if len(infos) < self.COUNT_FILE_INFO:
            logging.error('unknown info format')
            return None
        if infos[8] == '.' or infos[8] == '..':
            return None
        dir_info = content.DirectoryInfo(parent_dir, infos[8])

        return dir_info

    def _isDirEmpty(self, l):
        str = ''.join(l)
        return str.find('No such file or directory') != -1

    def _processDirectory(self, parent_dir = '', str_dir_info = ''):
        data = []
        contents = []
        cur_dir = self._retrieveDirInfo(parent_dir, str_dir_info)
        if cur_dir == None:
            return None
        try:
            if cur_dir.GetAbsPath() == '':
                data = self.ftp.retrlines('LIST', callback = contents.append)
            else:
                data = self.ftp.retrlines('LIST ' + cur_dir.GetAbsPath(), callback = contents.append)
        except ftplib.all_errors as e:
            logging.error('error while getting directory content: ' + repr(e))
            return cur_dir
        if self._isDirEmpty(contents):
            return cur_dir
        logging.debug('current directory: ' + cur_dir.GetAbsPath())
        
        files = (';'.join(line.split()) for line in contents)
        directory_list = list(files)
        for str in directory_list:
            infos = str.split(';')
            firstChar = str[0][0] # by the first character we define a folder or file
            if firstChar == 'd': # if folder
                d = self._processDirectory(cur_dir.GetAbsPath(), str)
                if d != None:
                    cur_dir.AddDir(d)
                    logging.debug(d.name + ' is directory')
            elif firstChar == '-': # if file
                fileInfo = self._retrieveFileInfo(cur_dir.GetAbsPath(), str)
                logging.debug(fileInfo.name + ' is file')
                cur_dir.AddFile(fileInfo)
        return cur_dir
