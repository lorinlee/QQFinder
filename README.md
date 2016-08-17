# QQFinder
QQFinder, find info by qq or qq group info by qq group number

### Something is needed

because the auth is still unavailable, so it needs some extra information to make the finder work

1. qq
    
    your qq number

2. skey

    your skey, you can get it by logging in qzone, and look for it in cookie

3. ldw
    
    unknown value, but it's necessary, you can get it by logging in tencent (such as logging in qzone), then do an user finding in [find.qq.com](http://find.qq.com),
    then you can get it in the network list

4. bkn
    
    the same as ldw
    unknown value, you can do a qq group finding in [qun.qq.com](http://qun.qq.com), also get it in network list

5. keyword
    
    qq number which you want to query

6. gc
    
    qq group number which you want to query
    
### How to use

you should finish the QQFinderConfig.py at first

QQUserFinder

``` python
myUser = QQUserFinder(qq=QQFinderConfig.QQ, skey=QQFinderConfig.SKEY, ldw=QQFinderConfig.LDW)
myUser.setKeyword(QQFinderConfig.QQ)
print myUser.getUser('json')
```

QQGroupFinder

``` python
qqGroup = QQGroupFinder(qq=QQFinderConfig.QQ, skey=QQFinderConfig.SKEY, bkn=QQFinderConfig.BKN, gc=497394781)
print qqGroup.getQQGroupMember('json')
qqGroup.setGc(545142869)
print qqGroup.getQQGroupMember('json')
```

### What's more

It is an unfinished project, many problems have not been solved...
