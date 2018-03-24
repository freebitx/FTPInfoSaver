__metaclass__ = type

class Timestamp:
    def __init__(self):
        self.year = 0
        self.month = ''
        self.day = 0

class BaseInfo:
    def __init__(self, path, name):
        self.name = name
        self.path = path
    def GetAbsPath(self):
        if self.path == '':
            return self.name
        return self.path + '/' + self.name

class DirectoryInfo(BaseInfo):
    def __init__(self, path, name):
        super(DirectoryInfo, self).__init__(path, name)
        self.files = []
        self.directories = []

    def AddDir(self, directory):
        self.directories.append(directory)

    def AddFile(self, file):
        self.files.append(file)

class FileInfo(BaseInfo):
    def __init__(self, path, name):
        super(FileInfo, self).__init__(path, name)
        self.link = ''
        self.timestamp = Timestamp()
        self.size = 0
        self.format = ''
