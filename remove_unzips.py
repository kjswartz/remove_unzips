# Given a starting directory path, scan the directoy for all files
# AND remove any '.zip' suffix files if corresponding directory is found i.e. delete .zip file if unzipped
# THEN go down directory tree within parent/starting directory and continue removing .zip files if unzipped

import sys, getopt
from pathlib import Path

ALL_DELETED_FILES = []

def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hi:", ["input="])
        if len(args) != 1 or len(opts) == 0: exit_script()
    except getopt.GetoptError:
        exit_script(2)
    for opt, arg in opts:
        if opt == '-h':
            exit_script()
        elif opt in ("-i", "--input"):
            main_loop(arg)
            last_msg()
        else:
            exit_script()

def main_loop(basepath):
    dirList = []
    zipFiles = []
    matches = []
    
    # collect dir names and zip file names from directory contents
    startpath = Path(basepath)
    for item in startpath.iterdir():
        if item.is_dir(): dirList.append(item.name)
        if item.is_file() and (item.suffix in ('.zip', '.gzip')): zipFiles.append(item)

    for zip in zipFiles:
        for dir in dirList:
            if f'{dir}.zip' == zip.name or f'{dir}.gzip' == zip.name: matches.append(zip)
    
    # display to user matching files and ask if they want to delete
    if len(matches) > 0:
        print(f'Do you want to delete the following files:')
        for x in matches:
            print(x)
        
        result = input('Y/N: ')

        if result in ('Y', 'YES', 'y', 'yes'):
            for x in matches:
                ALL_DELETED_FILES.append(x)
                x.unlink() # delete the zip file

    # lets call main again to loop through any children directories
    for dir in dirList:
        childpath = f'{basepath}{dir}/'
        main_loop(childpath)

def last_msg():
    if len(ALL_DELETED_FILES) > 0: 
        print('The following files have been deleted:')
        for fileitem in ALL_DELETED_FILES:
            print(fileitem)
    else:
        print('No files have been deleted')

def exit_script(code: str = ''):
    print('remove_unzips.py -i <absolute path for starting directory>')
    sys.exit(code) if code else sys.exit()


if __name__ == "__main__":
    main()