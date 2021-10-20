# FileProcessor

This python project contains a class `FileProcessor` which allows one to grab a file and get some meta data and header information from it.
In the current state, it outputs a PrettyTable to txt file as well as the raw data from that table into a csv.

### Class: FileProcessor
```py
class FileProcessor:

    def __init__(self):
        self.filePath = ''
        self.fileSize = ''
        self.mode = ''
        self.modifiedTime = ''
        self.createTime = ''
        self.header = ''
        self.lastErr = ''

    def SetFilePath(self, filePath):
        ''' Set the file path if valid 
            Obtain file size and timestamps
            return True if valid and set the self.filePath object variable
        '''
        if os.path.isfile(filePath):
            if os.access(filePath, os.R_OK):
                self.filePath = filePath
                stats = os.stat(self.filePath)
                self.fileSize = stats.st_size
                self.mode = stats.st_mode
                self.modifiedTime = time.ctime(stats.st_mtime)
                self.createTime = time.ctime(stats.st_atime)
                self.lastErr = ''
                return True
            else:
                self.filePath = ''
                self.lastErr = 'Invalid File Path'

    def GetFileHeader(self):
        with open(self.filePath, 'rb') as binFile:
            firstTwenty = binFile.read(20)
            hexStr = hexlify(firstTwenty)
            self.header = hexStr

    def PrintFileDetails(self):
        print("Path:               ", self.filePath)
        print("File Size:          ", '{:,}'.format(self.fileSize), "Bytes")
        print("File Mode:          ", self.mode)
        print("File Modified Time: ", self.modifiedTime)
        print("File Created Time:  ", self.createTime)
        print("File Header:        ", self.header)
```

### Additional Nice-ities:
Function added that allows a PrettyTable to be converted to csv (I could not get the built-in method to work):
```py
def ptable_to_csv(table, filename, headers=True):
    """Save PrettyTable results to a CSV file.

    :param PrettyTable table: Table object to get data from.
    :param str filename: Filepath for the output CSV.
    :param bool headers: Whether to include the header row in the CSV.
    :return: None
    """
    raw = table.get_string()
    data = [tuple(filter(None, map(str.strip, splitline)))
            for line in raw.splitlines()
            for splitline in [line.split('|')] if len(splitline) > 1]
    if table.title is not None:
        data = data[1:]
    if not headers:
        data = data[1:]
    with open(filename, 'w+') as f:
        for d in data:
            f.write('{}\n'.format(','.join(d)))
```

Function added to check or convert a filepath to a unique filepath:
```py
def uniquify(path):
    """If the given file already exists, creates file with appended number (incrementing while).

    :param str path: Filepath for checking or converting to unique filepath.
    """
    filename, extension = os.path.splitext(path)
    counter = 1

    while os.path.exists(path):
        path = filename + " (" + str(counter) + ")" + extension
        counter += 1

    return path
```

## Screenshots of process

