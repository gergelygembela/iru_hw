# Information Systems Management Homework
## Identifying similar ("nearly-compatible") methods in c++ classes

The script runs on Python 3.9 and newer Python versions. 
It depends on pip-package [`robotpy-cppheaderparser`](https://github.com/robotpy/robotpy-cppheaderparser), to install it, run:
```pip install robotpy-cppheaderparser```

With the dependency installed, the script is to be run with an argument specifying the path of a library to be analyzed (e.g. `python main.py "./testlib"`).

If no path is specified, the script attempts to run using the test library provided.

The program outputs a summary for all methods with problems. When the output consists of lines like `Processing methods of <classname>` but no errors are displayed, the program found none.

## Known issues and limitations
The program does little to no preprocessing on the headers, due to this it may not be able to parse libraries relying heavily on macros (e.g. Unreal Engine generated code/the FXB SDK, etc.). 
The parser library has its limitations, .

## Ideas for further development
The script currently only works with one "include root", due to the complexity of working out how compilers manage additional include directories/paths, it may be useful to implement 

#### My take on the need of scripts like this one
The problem this homework attempts to solve could mostly be worked around by using the `override` c++ keyword, and other compiler warnings (e.g. `-Wshadow`) that were made to eliminate the need for scripts just like mine.