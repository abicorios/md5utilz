print("md5scannerz v1.01 19.03.2017\nАвторы: omonim2007 и abicorios\nhttp://pscd.ru/forum/index.php?/topic/321-omonims-sety-dlia-retro-konsolei-8-64-bit")
print("https://github.com/abicorios")
print("Чтобы выйти нажмите Ctrl+C\nЧтобы скопировать выделенное, нажмите правую кнопку мыши.")
print("Чтобы вставить из буфера обмена, тоже нажмите правую кнопку мыши. Программа по ситуации понимает, копирование или вставку нужно делать.")
# coding: utf-8

# In[1]:


import os
import pandas as pd
from shutil import copyfile, rmtree
import hashlib
from sys import exit
import subprocess, shlex
import re
def myrmtree(imypath):
    for r, d, f in os.walk(imypath):
        for i in f:
            os.chmod(r+'\\'+i, 0o777)
    rmtree(imypath)
def myosremove(imypath):
    os.chmod(imypath, 0o777)
    os.remove(imypath)
def wrap(mystr):
    return re.sub(r'([^\\]|^)\\\?\\([^\\])',r'\1\\\\?\\\2',mystr)
def wraper(ar):
    return list(map(wrap,ar))
def myexit():
    f.close()
    exit()
def U(s):
    return r'\\?\{}'.format(s[0].upper()+s[1:])
def fend(s):
    if s[-1]=='\\':
        return s[:-1]
    else:
        return s
def norm(s):
    return fend(U(s))



def p(a):
    print(a.replace(myfrom,'').replace(myto,'').replace(exe,'').replace(mybuffer,''))
    f.write(str(a)+'\n')


def md5(myfile):
    hash_md5 = hashlib.md5()
    with open(myfile, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest().upper()
def drop(x,sep):
    return sep.join(x.split(sep)[:-1])
def mytype(ipath):
    if os.path.isfile(ipath):
        if re.search(r'\.(7z|zip|rar)$',ipath):
            return 'archive'
        else:
            return 'file'
    if os.path.isdir(ipath):
        return 'dir'
def inbuffer(ipath,ibuffer):
    if ibuffer in ipath:
        return True
    else:
        return False
def isempty(folder):
    if len(os.listdir(folder))>0: return False
    else: return True
def readz(ipath,ito,ibuffer,tinfo):
    for i in os.listdir(ipath):
        thisthing=r'{}\{}'.format(ipath,i)
        if mytype(thisthing)=='file':
            m=md5(thisthing)
            p(i)
            tinfo+=[{'path':ipath,'name':i,'md5':m}]
            # print('tinfo ',tinfo)
            if inbuffer(ipath,ibuffer):
                myosremove(thisthing)
        if mytype(thisthing)=='archive':
            if inbuffer(ipath,ibuffer):
                mycmd='"{}\\7z" x "{}" -o"{}\\{}" -aou'.format(exe,thisthing,ipath,drop(i,'.'))
                p(mycmd)
                subprocess.run(wraper(shlex.split(mycmd)))
                readz(ibuffer,ito,ibuffer,tinfo)
                myosremove(thisthing)
            if not inbuffer(ipath,ibuffer):
                mycmd='"{}\\7z" x "{}" -o"{}{}\\{}" -aou'.format(exe,thisthing,ibuffer,ipath.replace(myfrom,''),drop(i,'.'))
                p(mycmd)
                subprocess.run(wraper(shlex.split(mycmd)))
                readz(ibuffer,ito,ibuffer,tinfo)
        if mytype(thisthing)=='dir':
            if isempty(thisthing):
                if inbuffer(ipath,ibuffer):
                    os.rmdir(thisthing)
            else:
                readz(thisthing,ito,ibuffer,tinfo=tinfo)
                if isempty(thisthing):
                    if inbuffer(ipath,ibuffer):
                        os.rmdir(thisthing)

info=[]
p7zx86=r'C:\Program Files (x86)\7-Zip'
p7zx64=r'C:\Program Files\7-Zip'
while (not os.path.isdir(p7zx86)) and (not os.path.isdir(p7zx64)):
    print('Установите 7-Zip из http://www.7-zip.org/ используя умолчательный путь C:\\Program Files\\7-Zip или C:\\Program Files (x86)\\7-Zip')
    inp=str(input('Введите q чтобы выйти, или установите 7-Zip сейчас и введите здесь что угодно кроме q\n'))
    if inp=='q':
        exit()
if os.path.isdir(p7zx64):
    exe=p7zx64
elif os.path.isdir(p7zx86):
    exe=p7zx86
else:
    exit()

myto=r'{}'.format(input('Введите путь к пустой папке, в которую нужно поместить результат, например D:\\result\n'))
#myto='D:\\test\\0'
#if os.path.isdir(myto): myrmtree(myto)
myto=norm(myto)
if not os.path.isdir(myto): os.mkdir(myto)
while len(os.listdir(myto))>0:
    print('Ошибка! Папка {} не пуста! \n'.format(myto[4:]))
    myto=r'{}'.format(input('Введите путь к пустой папке для размещения результата. Или введите q чтобы выйти.\n'))
    if myto=='q':
        exit()
    myto=norm(myto)
myfrom=r'{}'.format(input('Введите путь к папке, которую нужно сканировать, например D:\\roms by genre\n'))
#myfrom='D:\\test\\long'
myfrom=norm(myfrom)
while not os.path.isdir(myfrom):
    p('Ошибка! Папка {} не существует!\n'.format(myfrom[4:]))
    myfrom=r'{}'.format(input('Введите путь к актуальной папке. Или введите q чтобы выйти.\n'))
    if myfrom=='q':
        exit()
    myfrom=norm(myfrom)
mybuffer=r'\\?\C:\Windows\Temp\md5utils'




if not os.path.isdir(myto): os.mkdir(myto)
if os.path.isdir(mybuffer): myrmtree(mybuffer)
os.mkdir(mybuffer)


f = open(r'{}\mylog.txt'.format(myto), 'a')

# In[4]:


readz(myfrom,myto,mybuffer,info)
myrmtree(mybuffer)

t=pd.DataFrame(info,columns=['path','name','md5'])
t
t['path']=t['path'].map(lambda x: x.replace(mybuffer+'\\',''))
t
t['path']=t['path'].map(lambda x: x.replace(myfrom+'\\',''))
t
t.to_csv(r'{}\{} ({}).csv'.format(myto,myfrom.split('\\')[-1],pd.Timestamp.now().strftime('%d.%m.%Y')),index=False)


# In[5]:


f.close()
input('\nВведите Enter чтобы выйти.\n')
