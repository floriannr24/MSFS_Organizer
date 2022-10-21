from pathlib import Path
import shutil
import re
import os
import argparse
import Levenshtein

# cmd line parser: option for entering multiple paths
parser = argparse.ArgumentParser()
parser.add_argument("file_path", nargs='+', type=Path)

# p = [Path('C:/Users/Florian/Downloads/test444.zip')]
p = parser.parse_args()

for files in p.file_path:
    if files.suffix == ".zip":

        scenery_Path = Path('F:/MSFS_Content/Mods/Scenery')

        result = [None]
        resLev = 0
        resPath = 0
        i = 0

        # searching existing scenery-folder, comparing file names with levenhstein(ratio)
        for continents in os.listdir(scenery_Path):
            for countries in os.listdir(scenery_Path / continents):
                for airports in os.listdir(scenery_Path / continents / countries):

                    searchStrings_Path = (scenery_Path / continents / countries / airports)
                    levRatio = round(Levenshtein.ratio(str(searchStrings_Path), str(files)), 3)

                    result[resLev] = [None] * 2
                    result.append(None)

                    result[resLev][resPath] = levRatio
                    resPath = 1
                    result[resLev][resPath] = searchStrings_Path
                    resLev = resLev + 1
                    resPath = 0

        # delete latest created 'None' (not needed)
        result.pop(len(result) - 1)

        # find max levenshtein values and its indices
        result.sort()
        maxIndex = len(result)-1

        # ask for confirmation by user (max 3 times per file)
        askCounter = 0
        askReplace = input("Scenery \"" + str(result[maxIndex][1].name) + "\" found. Replace with \"" + files.name + "\" ? - Y/N")
        askCounter = askCounter+1
        maxIndex= maxIndex-1
        success = None

        while askReplace == ('n' or 'N') and askCounter <= 2:
            askReplace = input("Scenery \"" + str(result[maxIndex][1].name) + "\" found. Replace with \"" + files.name + "\" ? - Y/N")
            askCounter = askCounter + 1
            maxIndex = maxIndex-1
            success = False

        if askReplace == ('y' or 'Y'):
            success = True
            # match found and accept: copy to new location, unzip, delete unneeded files
            foundFile_Path = result[maxIndex][1]

            dest_Path = foundFile_Path.parent
            destPath_File = dest_Path / files.name

            shutil.move(files, dest_Path)
            shutil.unpack_archive(destPath_File, dest_Path)
            shutil.rmtree(foundFile_Path)
            os.remove(destPath_File)

        if success == False:
            print(files.name +" has not been inserted")
            print(" ")

        if success == True:
            print("Scenery " + str(result[maxIndex][1].name) + " replaced with: " + files.name)
            print(" ")




