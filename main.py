
import os
import sys
import CppHeaderParser

import pathlib

headers: list[CppHeaderParser.CppHeader] = []


def absoluteFilePaths(directory: str):
    for dirpath,_,filenames in os.walk(directory):
        for f in filenames:
            yield os.path.abspath(os.path.join(dirpath, f))


def findSimilarMethods(classes: list[CppHeaderParser.CppClass], current: CppHeaderParser.CppClass):
    if(len(current.get('inherits')) == 0):
        return
    print("Processing methods of "+current.get('name'))


def processDir(dirPath: str):
    paths = absoluteFilePaths(dirPath)

    for entry in paths:
        if os.path.isfile(entry):
            if(pathlib.Path(entry).suffix == ".h"):
                headers.append(CppHeaderParser.CppHeader(entry))
    
    classes: list[CppHeaderParser.CppClass] = []

    for header in headers:
        for cls in header.classes:
            classes.append(header.classes.get(cls))           
        #m_type = header.parse_method_type()
        #print(m_type)

    #process loaded classes

    for cls in classes: 
        findSimilarMethods(classes, cls)


    return

def main(argv):
    in_path: str = argv[0]
    print("Processing files in directory " + in_path)

    processDir(in_path)    

    return

if __name__ == "__main__":
    if(len(sys.argv) > 1):
        sys.exit(main(sys.argv[1:]))
    else:
        sys.exit(main(["C:\\Git\\iru_hw\\testlib"]))
