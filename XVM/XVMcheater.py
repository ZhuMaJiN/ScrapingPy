import urllib.request
import urllib.parse
yn=input(r'是否想要批量查询(Y/N):')
if ((yn[0]=='Y')or(yn[0]=='y')):
    pass
else:
    name=input(r'请输入想要查询的id:')
    serv=input(r'请输入想要查询的id所在区服(南/北):')
    if(serv[0]=='南'):
        ice='south'
    if(serv[0]=='北'):
        ice='north'
    name=urllib.parse.quote(name)
    req=urllib.request.Request("http://rank.kongzhong.com/Data/action/WowsAction/getLogin?name="+name+"&zone="+ice)
    res=urllib.request.urlopen(req)
    string=res.read().decode('utf-8')
    temp=string.split(',')
    i=temp[0]
    i=i[8:]
    a=int(i)
    if(a==0):
        print('就不是正常玩家')
    if(a==-1):
        print('怕是狗头人')
    if(a==-2):
        print('现役狗头人')
    if(a==-3):
        print('资深狗头人')
    if(a==-4):
        print('这。。强无敌狗头人酋长')
    if(a==-5):
        print('还有负五？。。。天')
    i=temp[1]
    i=i[8:-1]
    print('这里是你的id：'+i)
