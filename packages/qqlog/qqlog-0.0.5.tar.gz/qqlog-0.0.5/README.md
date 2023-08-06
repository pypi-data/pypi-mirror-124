
# qqlog install
```python
pip install qqlog
```

# qqlog example 1

```python
from qqlog import ex,init,enterleave,trace
init()
#init(path='./log/qqlog.log',level=logging.DEBUG)

@ex()
def test1(a,b):
    return a/b

@enterleave()
def test2(a,b):
    return a/b    

@trace()
def test3(a,b):
    return a/b

@enterleave()
def test4(a,b,prefix='answer is'):
    val = a/b
    print('%s %s'%(prefix,str(val)))
    return val

class testclass(object):
    @enterleave()
    def __init__(self):
        print('init')
    @enterleave()
    def sum(self,a,b):
        return a+b

import pandas as pd
df = pd.DataFrame(data={'1':[1,2,3],'b':['test1','test2','test3']},index=range(3))

@enterleave()
def df_test(a,b,df):
    val = a+b+df['1'].sum()    
    return val

import numpy as np
d = np.array([[1,2,3],[4,5,6]])

@enterleave()
def np_test(a,b,d):
    val = a+b+d.sum()    
    return val

import logging
logging.getLogger('newlogger')

@enterleave(loggername='newlogger',level=logging.ERROR)
def new_logger_test(a,b):
    return a+b

try:
    test1(1,0)
    test2(1,1)
    test3(1,0)
    test4(1,2,prefix='result:')
    df_test(1,2,df)
    np_test(1,2,d)
    testclass().sum(10,20)
    new_logger_test(5,15)
    
    
except Exception as ex:
    print(ex)

```
# Console/qqlog.log
2021-09-29 21:47:47 [ERROR] [MainThread] [RAISE]test1: division by zero                                                           
2021-09-29 21:47:47 [DEBUG] [MainThread] [ENTER]test2(0:int=1, 1:int=1)                                                           
2021-09-29 21:47:47 [DEBUG] [MainThread] [RETURN]test2(1.0)                                                                       
2021-09-29 21:47:47 [ERROR] [MainThread] [RAISE]test3                                                                             
****************************************TRACE START****************************************                                       
Traceback (most recent call last):                                                                                                
  File "E:\jupyter\projects\whl\qqlog\qqlog\__init__.py", line 174, in func_warp                                                  
    return_val = func(*args, **kwargs)                                                                                            
  File "E:\jupyter\projects\whl\qqlog\example.py", line 15, in test3                                                              
    return a/b                                                                                                                    
ZeroDivisionError: division by zero                                                                                               
                                                                                                                                  
****************************************TRACE END****************************************                                         
                                                                                                                                  
2021-09-29 21:47:47 [DEBUG] [MainThread] [ENTER]test4(0:int=1, 1:int=2, prefix:str='result:')                                     
result: 0.5                                                                                                                       
2021-09-29 21:47:47 [DEBUG] [MainThread] [RETURN]test4(0.5)                                                                       
2021-09-29 21:47:47 [DEBUG] [MainThread] [ENTER]df_test(0:int=1, 1:int=2, 2:DataFrame=[3bb56549-ebe7-4a85-900f-50d8788d29d3.csv]) 
2021-09-29 21:47:47 [DEBUG] [MainThread] [RETURN]df_test(9)                                                                       
2021-09-29 21:47:47 [DEBUG] [MainThread] [ENTER]np_test(0:int=1, 1:int=2, 2:ndarray=[367eb5ed-73f8-45e8-8fcb-4d8781afc46a.ary])   
2021-09-29 21:47:47 [DEBUG] [MainThread] [RETURN]np_test(24)                                                                      
2021-09-29 21:47:47 [DEBUG] [MainThread] [ENTER]__init__()                                                                        
init                                                                                                                              
2021-09-29 21:47:47 [DEBUG] [MainThread] [RETURN]__init__(None)                                                                   
2021-09-29 21:47:47 [DEBUG] [MainThread] [ENTER]sum(0:int=10, 1:int=20)                                                           
2021-09-29 21:47:47 [DEBUG] [MainThread] [RETURN]sum(30)                                                                          
[ENTER]new_logger_test(0:int=5, 1:int=15)                                                                                         
[RETURN]new_logger_test(20)                                                                                                       
```

# qqlog example 2
```python
from qqlog import ex,init,createCsvFileLogger,createConsoleFileLogger
import logging
init()

createCsvFileLogger('csv',level=logging.DEBUG,headers=['asctime','funcName','levelname','msg'],formatters=['asctime','funcName','levelname','msg'],path='debug.csv')
createConsoleFileLogger('consolefile',level=logging.DEBUG,path='./consolefile.log')

@ex(loggername='csv',rethrow=False)
def test_csv(a,b):
    return a/b

@ex(loggername='consolefile',rethrow=False)
def test_consolefile(a,b):
    return a/b

try:
    test_csv(1,0)
    test_consolefile(1,0)
except Exception as ex:
    print(ex)
```
``` debug.csv
asctime,funcName,levelname,msg
"2021-10-23 21:32:26","func_warp","ERROR","[RAISE]test_csv: division by zero"
```
``` cnsolefile.log
2021-10-23 21:32:26,407 [RAISE]test_consolefile: division by zero
```