
import os
import sys
import CppHeaderParser

import pathlib


class ResultItem:
    name = 'a'
    

headers: list[CppHeaderParser.CppHeader] = []

runResult: list[ResultItem] = []

def absoluteFilePaths(directory: str):
    for dirpath,_,filenames in os.walk(directory):
        for f in filenames:
            yield os.path.abspath(os.path.join(dirpath, f))


def findMethodsWithName(cls: CppHeaderParser.CppClass, name: str)-> list[CppHeaderParser.CppMethod]:
    for method in cls.get('methods'):
        print(method.get())


def discoverParents(current: CppHeaderParser.CppClass, classes: list[CppHeaderParser.CppClass]) -> list[CppHeaderParser.CppClass]:
    parents: list[CppHeaderParser.CppClass] = []
    for cls in classes:
        for parent in current.get('inherits'):
            if cls.get('name') == parent.get('class'):
                if cls not in parents: 
                    parents.append(cls)
                    parents += discoverParents(cls, classes)
    return parents


def compareMethods(lhs: CppHeaderParser.CppMethod, rhs: CppHeaderParser.CppMethod):

    
    return


def findSimilarMethodsInClass(cls: CppHeaderParser.CppClass, other: CppHeaderParser.CppMethod):
    for method in cls.get('methods').get('public'):
        if(method.get('name') == other.get('name')):
            compareMethods(method, other)
    return


def findSimilarMethods(classes: list[CppHeaderParser.CppClass], current: CppHeaderParser.CppClass):
    if(len(current.get('inherits')) == 0):
        return
    print("Processing methods of "+current.get('name'))
    
    #discover parent tree
    parents = discoverParents(current, classes)
 
    for method in current.get('methods').get('public'):
        for cls in parents:
            findSimilarMethodsInClass(cls, method)

    for method in current.get('methods').get('protected'):
        for cls in parents:
            findSimilarMethodsInClass(cls, method)



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
