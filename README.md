# PyFix - Fault Localization & Automated Program Repair in Python

PyFix focuses on making debugging for programmers easier by localizing the bug and synthesizing program repairs. Our tool aims to predict the most suspicious statements inside a Python program, modifies them based on the cues available from the rest of the program and verifies if that fixes the program.

## Getting Started

```
python PyFix.py <arg1> <arg2> <arg3>
```
where
arg1 = Your script to find bug in and repair
arg2 = Result of test cases which will be passed to tarantula
arg3 = Unittests for testing if repaired code has its bug fixed

For example
```
python PyFix.py mid.py testCasesMid testMid
python PyFix.py is_prime.py testCasesPrime testPrime
```

### Prerequisites

You would also need to install the following libraries:
i. NumPy
ii. NLTK


```
sudo pip install numpy
sudo pip install nltk
```

## Running the tests

We have tried to keep PyFix as generic as possible however it follows a particular standard for the three input files provided.

* The first argument which is the script to be debugged must be in the form of a python function that may take a list or real numbers as input arguments.

```
def mid(x,y,z):
    m = z
    if (y<z):
        if(x<y):
            m = y
        elif (x<z):
            m = y
    else:
        if(x>y):
            m = y
        elif (x>z):
            m = x
    return m
```

* The second argument, which is the result of test cases returned by the bugged script and their input arguments, may have indefinite number of test inputs so long as every following line has the result of that test case which is whether it passed (P) or failed (F).

```
3,3,5
P
1,2,3
P
3,2,1
P
5,5,5
P
5,3,4
P
2,1,3
F
```

* The third argument is of unittests against which all of PyFix repaired scripts are tested. These have to be in the following format

```
def unittests(tempCodeString):
    try:
        exec(tempCodeString)
        assert mid(2,1,3) == 2
        assert mid(3,3,5) == 3
        assert mid(1,2,3) == 2
        assert mid(5,5,5) == 5
        assert mid(5,3,4) == 4
        assert mid(3,2,1) == 2
        # print 'Following Case Passed:'
        return True
    except:
        # print "A test case failed"
        return False
```

## Built With

* [SpiderLab](http://spideruci.org/fault-localization/) - The team behind Tarantula technique
* [Paper](http://spideruci.org/papers/jones05.pdf) - Research Paper on the Algorithm itself and Evaluations



## Authors

* [Ali Ahsan](https://github.com/aliahsan07)
* [Zain Qasmi](https://github.com/ZainQasmi)
* [Dawood Jehangir](https://github.com/dawood-jehangir)

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details


## Acknowledgments

* [Junaid Haroon Siddiqui](https://github.com/jsiddiqui) - *Project Supervisor*