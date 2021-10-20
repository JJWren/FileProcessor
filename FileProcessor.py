'''
Joshua Wren
2021-10-12
File Processor
'''
from __future__ import print_function
from genericpath import exists
import os
import pathlib
import sys
import time
from binascii import hexlify
from prettytable import PrettyTable
from pathlib import Path

''' Determine which version of Python '''
if sys.version_info[0] < 3:
    PYTHON_2 = True
else:
    PYTHON_2 = False


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


# region [Convert PrettyTable to CSV - Function]
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
# endregion


# region [While File Exists, Add Number - Function]
def uniquify(path):
    filename, extension = os.path.splitext(path)
    counter = 1

    while os.path.exists(path):
        path = filename + " (" + str(counter) + ")" + extension
        counter += 1

    return path
# endregion


if __name__ == "__main__":
    print("Start of File Processor...")

    if PYTHON_2:
        directory = raw_input("Enter directory to process files from: ")
    else:
        directory = input("Enter directory to process files from: ")

    """Instantiate a PrettyTable"""
    ptable = PrettyTable()
    ptable.field_names = ["File Path", "File Size", "File Mode",
                          "File Modified", "File Created", "File Header"]

    if os.path.isdir(directory):
        dirs = os.listdir(directory)

        for eachFile in dirs:
            ''' Set file path '''
            file = os.path.join(directory, eachFile)
            ''' Instantiate instance of the class: FileProcessor '''
            obj = FileProcessor()

            print(f"\nProcessing File {file}...\n")

            if obj.SetFilePath(file):
                if obj.SetFilePath(file):
                    obj.GetFileHeader()
                    # obj.PrintFileDetails()
                    ptable.add_row([obj.filePath, obj.fileSize, obj.mode,
                                    obj.modifiedTime, obj.createTime, obj.header])
                else:
                    print("Processing Failed: ", obj.lastErr)
            else:
                print("File Name Err: ", obj.lastErr)
    else:
        print(f"'{directory}' is an invalid directory")

    """Sort/Align the PT"""
    ptable.sortby = "File Path"
    ptable.align["File Path"] = "l"
    ptable.align["File Size"] = "l"

    """PT output to txt"""
    path_to_output_to = os.path.curdir
    parent_dir = os.path.basename(directory)
    filename_txt = f"{path_to_output_to}_{parent_dir}_FilesProcessedPT.txt"
    # appends number to file name if it already exists
    unique_file = uniquify(filename_txt)
    try:
        f = open(unique_file, "w+")
        ptable_txt = ptable.get_string()
        f.write(ptable_txt)

        print(f'{unique_file} was generated in local script folder')
        f.close()
    except:
        print("An error occurred while trying to write PrettyTable contents to txt file")

    """PT output to csv"""
    filename_csv = f"{path_to_output_to}_{parent_dir}_FilesProcessedPT.csv"
    # appends number to file name if it already exists
    unique_file = uniquify(filename_csv)
    fullpath = f'{os.curdir}\\{unique_file}'
    try:
        ptable_to_csv(ptable, fullpath, True)
        print(f'{unique_file} was generated in local script folder')
    except Exception as error:
        print(
            f'\nThe following exception occurred while trying to create csv file:\n\t{error}\n')

    print("\n** File Processing End **")
