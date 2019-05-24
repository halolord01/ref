'''This is my custom modual for python'''
from time import strftime, localtime
from io import TextIOWrapper

def debug(*arg):
    base = 'Debug '
    print ('-----------------------------------------------------')
    for i,a in enumerate(arg):
        print(base + str(i) + ': ' + str(a) + '\n')
    print ('-----------------------------------------------------')
    pass

def print_block(text, pre = 0, post = 0):
    if pre > 0: pre -=1
    if post > 0: post -=1
    print('\n'* pre)
    print('{:=^80}'.format(''))
    print('{:=^80}'.format(' ' + str(text) + ' '))
    print('{:=^80}'.format(''))
    print('\n'* post)

def printl(text, pre = 0, post = 0, crr = '='):
    if pre > 0: pre -=1
    if post > 0: post -=1
    print('\n'* pre)
    print('{:{cr}^80}'.format(' ' + str(text).upper() + ' ',  cr = crr))
    print('\n'* post)

def returnTime():
    return strftime('%Y-%m-%d %H:%M:%S', time.localtime())
    # return time.asctime(time.localtime(time.time()))

def end_check(f):
    f.buffer.seek(-1,2)
    resp = f.read(1)
    f.buffer.seek(0,2)
    return (TextIOWrapper(
            f.buffer, encoding = f.encoding, errors=f.errors,
            newline=f.newlines), resp)