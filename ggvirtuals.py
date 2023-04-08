import os
import pathlib
import sys

import CppHeaderParser

headers: list[CppHeaderParser.CppHeader] = []

warn_noexcept = False

def absoluteFilePaths(directory: str):
    for dirpath, _, filenames in os.walk(directory):
        for f in filenames:
            yield os.path.abspath(os.path.join(dirpath, f))

def discoverParents(current: CppHeaderParser.CppClass, classes: list[CppHeaderParser.CppClass]) -> list[CppHeaderParser.CppClass]:
    parents: list[CppHeaderParser.CppClass] = []
    for cls in classes:
        for parent in current.get('inherits'):
            if cls.get('name') == parent.get('class'):
                if cls not in parents:
                    parents.append(cls)
                    parents += discoverParents(cls, classes)
    return parents


def getFullSignature(cls: CppHeaderParser.CppClass, method: CppHeaderParser.CppMethod)-> str:
    return f"{cls.get('namespace')}::{cls.get('name')}::{method.get('debug')}"

def getFullSignatureWithFileName(cls: CppHeaderParser.CppClass, method: CppHeaderParser.CppMethod)-> str:
    res = getFullSignature(cls, method)
    res += f" at line {method.get('line_number')} in file {method.get('filename')}"
    return res

def compareParams(lhs: CppHeaderParser.CppMethod, rhs: CppHeaderParser.CppMethod) -> tuple[bool, list[str]]:
    result: tuple[bool, list[str]] = (False, [])
    
    lhs_params = lhs.get('parameters')
    rhs_params = rhs.get('parameters')

    for i, l_param in enumerate(lhs_params):
        r_param = rhs_params[i]
        if(l_param.get('type') != r_param.get('type')) and (l_param.get('type').replace('const ','') != r_param.get('type').replace('const ','')):
            return (True, [])
        if(l_param.get('constant') != r_param.get('constant')):
            result[1].append(f"Potential const mismatch at parameter {i} ({r_param.get('name')})")
        #if(m lhs_params[i])    
    return result


def compareMethods(lhs: CppHeaderParser.CppMethod, rhs: CppHeaderParser.CppMethod, parent: CppHeaderParser.CppClass, other: CppHeaderParser.CppClass):
    #different return type is enough distinction
    if (lhs.get('rtnType') != rhs.get('rtnType')):
        return
    
    #so is a different number of parameters
    if len(lhs.get('parameters')) != len(rhs.get('parameters')):
        return

    problems: list[str] = []
    #so are different types of params
    res = compareParams(lhs, rhs)

    #There were different param types
    if res[0]:
        return

    problems+= res[1]
    
    if lhs.get('const') != rhs.get('const'):
        problems.append(f'Methods {getFullSignature(parent, lhs)} and {getFullSignature(other, rhs)} have different const qualifiers.')

    if not lhs.get('virtual'):
        problems.append(f'Method {getFullSignature(parent, lhs)} is not marked virtual.')

    if warn_noexcept and (lhs.get('noexcept') != rhs.get('noexcept')):
        problems.append(f'Methods {getFullSignature(parent, lhs)} and {getFullSignature(other, rhs)} have different noexcept qualifiers.')

    if(len(problems) > 0):
        print(f'Summary for {getFullSignatureWithFileName(other, rhs)}:')
    else:
        if not other.get('override'):
            print(f"Method {getFullSignatureWithFileName(other, rhs)} seems to be an override, consider using the 'override' keyword when compiling with std=c++11 or newer.")

    for problem in problems:
        print(problem)

    return


def findSimilarMethodsInClass(parent: CppHeaderParser.CppClass, other: CppHeaderParser.CppMethod, other_cls: CppHeaderParser.CppClass):
    for method in parent.get('methods').get('public'):
        if method.get('name') == other.get('name'):
            compareMethods(method, other, parent, other_cls)
    return


def findSimilarMethods(classes: list[CppHeaderParser.CppClass], current: CppHeaderParser.CppClass):
    if (len(current.get('inherits')) == 0):
        return
    print(f"\nProcessing methods of {current.get('name')}")

    # discover parent tree
    parents = discoverParents(current, classes)

    for method in current.get('methods').get('public'):
        for cls in parents:
            findSimilarMethodsInClass(cls, method, current)

    for method in current.get('methods').get('protected'):
        for cls in parents:
            findSimilarMethodsInClass(cls, method, current)


def processDir(dirPath: str):
    paths = absoluteFilePaths(dirPath)

    for entry in paths:
        if os.path.isfile(entry):
            if (pathlib.Path(entry).suffix == ".h"):
                try:
                    headers.append(CppHeaderParser.CppHeader(entry))
                except CppHeaderParser.CppHeaderParser.CppParseError:
                    print(f'Excluded classes of header {entry} due to a c++ parser error.')
                except:
                    print(f'An unknown error occured while parsing header {entry}. Some classes may not get checked.')

    classes: list[CppHeaderParser.CppClass] = []
    for header in headers:
        for cls in header.classes:
            classes.append(header.classes.get(cls))

    # process loaded classes
    for cls in classes:
        findSimilarMethods(classes, cls)


def main(argv):
    in_path: str = argv[0]
    print(f'Processing files in directory {in_path}')
    processDir(in_path)

if __name__ == "__main__":
    if (len(sys.argv) > 1):
        sys.exit(main(sys.argv[1:]))
    else:
        sys.exit(main(["./testlib"])) #received no library path
