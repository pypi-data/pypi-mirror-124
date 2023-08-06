# -*- coding: utf-8 -*-
"""
Created on Fri Nov 20 20:22:44 2020

@author: yonder_sky
"""

# Python通用工具库，陈杨城，yondersky@126.com，2020-11-20
# 更新日期：2021-10-06

import collections, functools, itertools, math, numbers, time
import numpy as np
import pandas as pd
from pandas import DataFrame, Series

# 0. 全局变更

# AnsiSeriesType = type(Series(dtype=object))
ConsoleInitStamp = time.strftime('%Y%m%d%H%M%S')
# LogDir = os.getcwd()+'\\Log'
NA = np.nan

# if not os.path.exists(LogDir):
#     os.mkdir(LogDir)

# 1. 系统命令

# 1.1 控制台输出

# 2020-11-20
# def clog(*content, sep = ' ', stdOutput = None):
#     '''
#     控制台输出。
#     【示例】
#     >>> t = clog('pytool',stdOutput=False)
#     >>> leftex(t,8)
#     ' - pytool'
#     '''
#     timeStr = time.strftime('%H:%M:%S')
#     logStr = sep.join((timeStr,'-')+content)
#     if stdOutput is None:
#         stdOutput = True
#     if stdOutput:
#         print(logStr)
#     logPath = LogDir+'\\ConsoleLog_'+ConsoleInitStamp+'.txt'
#     with open(logPath,'a') as fp:
#         fp.write(logStr+'\n')
#         fp.close()
#     return logStr

# 2. 通用装饰器

# 2.1 向量化（Apply族）装饰器

'''
【注】（本节通用）
1. 此处apply（函数名为fapply）所指涵义与R语言中的apply系列函数相同，与Python中的
   apply函数（itertools包）不同。
2. 虽然str也为可迭代类型，但通用装饰器不对其展开迭代。
3. 若returnType为None，则返回类型为输入类型（但若输入类型为range，则返回类型为
   list）；否则返回类型为returnType。
'''

# 2.1.1 单参数函数

# 普通函数版本
# 2020-11-22
def emap(func):
    '''
    扩展形式的map函数，返回对应输入的迭代结果。
    【示例】
    >>> emap(abs)(-1)
    1
    >>> emap(abs)(range(5))
    [0, 1, 2, 3, 4]
    >>> emap(abs)([-1,-2,-3],tuple)
    (1, 2, 3)
    '''
    @functools.wraps(func)
    
    # 2020-11-22
    def mapped(iterables, returnType = None):
        if isinstance(iterables,str):
            return func(iterables)
        elif isinstance(iterables,collections.abc.Iterable):
            result = map(func,iterables)
            if returnType is None:
                returnType = type(iterables)
            if returnType is range or returnType is set:
                returnType = list
            if returnType is map:
                return result
            elif returnType is np.ndarray:
                return np.array(list(result))
            elif isinstance(iterables,Series) and returnType==Series:
                return Series(result,iterables.index)
            else:
                return returnType(result)
        else:
            return func(iterables)
    
    return mapped

# 类成员函数版本
# 2021-06-08
def temap(func, returnType = None):
    '''类成员函数版本的emap装饰器'''
    @functools.wraps(func)
    
    # 2021-06-08
    def mapped(self, iterables, returnType = None):
        if isinstance(iterables,str):
            return func(self,iterables)
        elif isinstance(iterables,collections.abc.Iterable):
            result = map(functools.partial(func,self),iterables)
            if returnType is None:
                returnType = type(iterables)
            if returnType is range or returnType is set:
                returnType = list
            if returnType is map:
                return result
            elif returnType is np.ndarray:
                return np.array(list(result))
            elif isinstance(iterables,Series) and returnType==Series:
                return Series(result,iterables.index)
            else:
                return returnType(result)
        else:
            return func(self,iterables)
    
    return mapped
    
# 2.1.2 多参数函数（向量化首个参数）

# 2020-11-25
def sapply(func, returnType = None):
    '''
    类R语言sapply函数，对首个输入参数向量化。
    【示例】
    >>> sapply(isinstance)('1',int)
    False
    >>> sapply(isinstance)(range(5),bool)
    [False, False, False, False, False]
    >>> sapply(isinstance,tuple)([1,2.2,'abc'],int)
    (True, False, False)
    '''
    @functools.wraps(func)
    
    # 2020-11-25
    def applied(iterables, *args, **kwargs):
        if isinstance(iterables,str):
            return func(iterables,*args,**kwargs)
        elif isinstance(iterables,collections.abc.Iterable):
            result = [func(i,*args,**kwargs) for i in iterables]
            rttype = returnType
            if rttype is None:
                rttype = type(iterables)
            if rttype is range or rttype is set:
                rttype = list
            if rttype is list:
                return result
            elif rttype is np.ndarray:
                return np.array(result)
            elif isinstance(iterables,Series) and rttype==Series:
                return Series(result,iterables.index)
            else:
                return rttype(result)
        else:
            return func(iterables,*args,**kwargs)
    
    return applied

# 3. 格式转换

# 3.1 字符串相关

# 3.1.1 子字符串

# 2020-11-20
@sapply
def left(thestr, count):
    '''
    返回thestr前count个字符。
    【示例】
    >>> left(['pytool','arraytool'],2)
    ['py', 'ar']
    '''
    return thestr[:count]

# 2020-11-20
@sapply
def leftex(thestr, count):
    '''
    返回thestr除前count个字符以外的剩余字符。
    【示例】
    >>> leftex(['pytool','arraytool'],2)
    ['tool', 'raytool']
    '''
    return thestr[count:]

# 2021-09-11
@sapply
def mid(thestr, start, count):
    '''
    返回thestr第start个位置开始的count个字符。
    【示例】
    >>> mid(['pytool','arraytool'],3,4)
    ['tool', 'rayt']
    '''
    return thestr[(start-1):(start+count-1)]

# 2021-09-11
@sapply
def right(thestr, count):
    '''
    返回thestr右侧count个字符。
    【示例】
    >>> right(['pytool', 'arraytool'], 4)
    ['tool', 'tool']
    '''
    return thestr[-count:]

# 2021-09-11
@sapply
def rightex(thestr, count):
    '''
    返回thestr除去右侧count个以外的剩余字符。
    【示例】
    >>> rightex(['pytool', 'arraytool'], 4)
    ['py', 'array']
    '''
    return thestr[:-count]


# 3.1.2 字符串转换

# 2021-09-15
@emap
def StrToFloat(numstr):
    '''
    字符串转浮点数（支持百分号）。
    【示例】
    >>> StrToFloat(['33', '33.33', '33.33%'])
    [33.0, 33.33, 0.3333]
    '''
    if numstr[len(numstr)-1]=='%':
        return float(numstr[:-1])/100
    else:
        return float(numstr)

# 3.2 数字相关

# 3.2.1 舍入

# 2021-09-14
@sapply
def ExactRound(number, ndigits = 0):
    '''
    自定义舍入函数。
    【示例】
    >>> ExactRound([0, 0.05, 0.0499], 1)
    [0.0, 0.1, 0.0]
    >>> ExactRound(12345.6789,3)
    12345.679
    >>> ExactRound(12345.6789,-3)
    12000.0
    '''
    base = 10**ndigits
    return int(number*base+0.5)/base

# 3.3 切片相关

# 格式化切片
# 2020-11-28
def FormatSlice(s, maxlen):
    '''
    根据输入的最大长度格式化切片。
    【示例】
    >>> FormatSlice(slice(None,None,None),10)
    slice(0, 10, 1)
    >>> FormatSlice(slice(None,None,-1),10)
    slice(10, 0, -1)
    >>> FormatSlice(slice(-3,None,None),10)
    slice(7, 10, 1)
    >>> FormatSlice(slice(2,-2,2),10)
    slice(2, 8, 2)
    '''
    step = 1 if s.step is None else s.step
    start = (0 if step>0 else maxlen) if s.start is None else s.start
    if start<0:
        start %= maxlen
    stop = (maxlen if step>0 else 0) if s.stop is None else s.stop
    if stop<0:
        stop %= maxlen
    return slice(start,stop,step)

# 3.4 列表相关

# 多维笛卡尔积
# 2021-06-03
def ListProduct(*iterables, order = 'C'):
    '''
    多维笛卡尔积。
    【注】
    关于order参数：
      C - 以行主序进行遍历（C风格）
      F - 以列主序进行遍历（F风格）
    【示例】
    >>> ListProduct(list('abc'),[1,0])
    [['a', 'a', 'b', 'b', 'c', 'c'], [1, 0, 1, 0, 1, 0]]
    >>> ListProduct(list('abc'),[1,0],order='F')
    [['a', 'b', 'c', 'a', 'b', 'c'], [1, 1, 1, 0, 0, 0]]
    '''
    if order=='F':
        return [list(z) for z in zip(*itertools.product(*iterables[::-1]))][::-1]
    else:
        return [list(z) for z in zip(*itertools.product(*iterables))]

# 3.5 元组相关

# 多维笛卡尔积
# 2021-06-03
def TupleProduct(*iterables, order = 'C'):
    '''
    多维笛卡尔积。
    【注】
    关于order参数：
      C - 以行主序进行遍历（C风格）
      F - 以列主序进行遍历（F风格）
    【示例】
    >>> TupleProduct(list('abc'),[1,0])
    (('a', 'a', 'b', 'b', 'c', 'c'), (1, 0, 1, 0, 1, 0))
    >>> TupleProduct(list('abc'),[1,0],order='F')
    (('a', 'b', 'c', 'a', 'b', 'c'), (1, 1, 1, 0, 0, 0))
    '''
    if order=='F':
        return tuple(tuple(z) for z in 
            zip(*itertools.product(*iterables[::-1])))[::-1]
    else:
        return tuple(tuple(z) for z in zip(*itertools.product(*iterables)))

# 4. 类型判断

# 4.1 变量类型判断

# 2021-02-16
def IsArray(var):
    '''
    判断是否为numpy.ndarray类型对象。
    【示例】
    >>> IsArray(np.ones(10))
    True
    '''
    return True if isinstance(var,np.ndarray) else False

# 2020-11-28
def IsBool(var):
    '''
    判断是否为bool类型（包括常规bool类型及numpy中的bool类型）对象。
    【示例】
    >>> IsBool(False)
    True
    >>> IsBool(np.sin(1)<0)
    True
    >>> IsBool('a')
    False
    '''
    return True if isinstance(var,np.bool_) or isinstance(var,bool) else False

# 2021-08-12
def IsDataFrame(var):
    '''
    判断是否为DataFrame。
    【示例】
    >>> IsDataFrame(DataFrame())
    True
    >>> IsDataFrame(1)
    False
    '''
    return True if isinstance(var,DataFrame) else False

# 2021-10-06
def IsIndex(var):
    '''
    判断是否为pandas索引。
    '''
    return True if isinstance(var,pd.Index) else False

# 2020-11-28
def IsInteger(var):
    '''
    判断是否为整数。
    【示例】
    >>> IsInteger(1)
    True
    >>> IsInteger([])
    False
    '''
    return True if isinstance(var,numbers.Integral) else False

# 2021-06-08
def IsIterable(var):
    '''
    判断是否为可迭代类型对象。
    【示例】
    >>> IsIterable([])
    True
    >>> IsIterable(())
    True
    >>> IsIterable(np.arange(3))
    True
    >>> IsIterable(range(3))
    True
    >>> IsIterable(slice(3))
    False
    '''
    return True if isinstance(var,collections.abc.Iterable) else False

# 2021-10-06
def IsMultiIndex(var):
    '''
    判断是否为pandas多重索引。
    【示例】
    >>> ser1 = Series(range(4))
    >>> IsMultiIndex(ser1.index)
    False
    >>> ser2 = Series(range(4),[list('abcd'),list('AAAB')])
    >>> IsMultiIndex(ser2.index)
    True
    '''
    return True if isinstance(var,pd.MultiIndex) else False

# 2021-05-13
def IsSeries(var):
    '''
    判断是否为pandas系列。
    【示例】
    >>> IsSeries(Series(range(5)))
    True
    >>> IsSeries(range(5))
    False
    '''
    return True if isinstance(var,Series) else False

# 2021-05-14
def IsSimpleIndex(var):
    '''
    判断是否为可化简的索引类型（索引为RangeIndex对象且start为0）。
    【示例】
    >>> ser1 = Series(range(4))
    >>> IsSimpleIndex(ser1.index)
    True
    >>> ser2 = Series(range(4),range(1,5))
    >>> IsSimpleIndex(ser2.index)
    False
    >>> ser3 = Series(range(4),list('abcd'))
    >>> IsSimpleIndex(ser3.index)
    False
    '''
    return var.start==0 if isinstance(var,pd.RangeIndex) else False

# 2020-11-28
def IsSingleType(var):
    '''
    判断是否为单值类型（不可迭代类型或str）。
    【示例】
    >>> IsSingleType(1)
    True
    >>> IsSingleType(NA)
    True
    >>> IsSingleType([1,4])
    False
    >>> IsSingleType(range(5))
    False
    >>> IsSingleType(slice(None,None,None))
    False
    '''
    if not isinstance(var,str) and isinstance(var,collections.abc.Iterable) \
        or isinstance(var,slice):
        return False
    else:
        return True

# 2021-07-10
def IsSingleType2(var):
    '''
    判断是否为单值类型。
    【注】IsSingleType2函数slice对象返回True，其余返回与IsSingleType函数相同。
    【示例】
    >>> IsSingleType2(1)
    True
    >>> IsSingleType2(range(5))
    False
    >>> IsSingleType2(slice(None,None,None))
    True
    '''
    if not isinstance(var,str) and isinstance(var,collections.abc.Iterable):
        return False
    else:
        return True

# 2021-02-14
def IsSlice(var):
    '''
    判断是否为切片。
    【示例】
    >>> IsSlice(slice(10))
    True
    >>> IsSlice(10)
    False
    '''
    return True if isinstance(var,slice) else False

# 5. 数据分析

# 5.1 长度自适应

# 2020-11-28
def ExpandSize(curLen, targetLen, expandCount, expandRatio):
    '''
    返回扩张后的维度大小。
    【示例】
    >>> ExpandSize(27,None,10,2)
    37
    >>> ExpandSize(27,1000,10,2)
    1007
    >>> ExpandSize(27,None,0,2)
    54
    >>> ExpandSize(27,1000,0,2)
    1728
    '''
    rtlen = curLen
    if expandCount==0:
        # 比例扩张
        rtlen = max(math.ceil(rtlen*expandRatio),rtlen+1)
        if not targetLen is None:
            while rtlen<targetLen:
                rtlen = max(math.ceil(rtlen*expandRatio),rtlen+1)
    else:
        # 数量扩张
        rtlen += expandCount
        if not targetLen is None:
            while rtlen<targetLen:
                rtlen += expandCount
    return rtlen

if __name__=='__main__':
    import doctest
    doctest.testmod()
