import urllib.request
import urllib.parse
import random
import time
import re
import os
import traceback
def replace(x):
    #去除img标签，7位长空格
    removeImg=re.compile('<img.*?>| {7}|')
    #去除超链接标签
    removeAddr=re.compile('<a.*?>|</a>')
    #把换行的标签换为\n
    replaceLine=re.compile('<tr>|<div>|</div>|</p>')
    #将表格制表<td>替换为\t
    replaceTD=re.compile('<td>')
    #把段落开头换为\n加空两格
    replacePara=re.compile('<p.*?>')
    #将换行符或双换行符替换为\n
    replaceBR=re.compile('<br><br>|<br>')
    #将其余标签删除
    removeExtraTag=re.compile('<.*?>')
    x=re.sub(removeImg,"",x)
    x=re.sub(removeAddr,"",x)
    x=re.sub(replaceLine,"\n",x)
    x=re.sub(replaceTD,"\t",x)
    x=re.sub(replacePara,"\n  ",x)
    x=re.sub(replaceBR,"\n",x)
    x=re.sub(removeExtraTag,"",x)
    return x.strip()
def openurl(urls):
    #dailis = ["121.232.147.20:9000", "117.90.3.243:9000", "118.251.229.102:8998", "125.124.129.66:3128", "221.180.170.15:80"]
    heads= ["Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.71 Safari/537.36", "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:34.0) Gecko/20100101 Firefox/34.0", "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/534.57.2 (KHTML, like Gecko) Version/5.1.7 Safari/534.57.2", "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/30.0.1599.101 Safari/537.36", "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.84 Safari/535.11 SE 2.X MetaSr 1.0", "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Maxthon/4.4.3.4000 Chrome/30.0.1599.101 Safari/537.36"]
    #daili = urllib.request.ProxyHandler({'http': random.choice(dailis)})
    #opener = urllib.request.build_opener(daili)
    #opener.addheaders = [('User-Agent', random.choice(heads))]
    #urllib.request.install_opener(opener)
    #楼上在尝试用代理
    data={}
    head={}
    head['User-Agent']=random.choice(heads)
    #time.sleep(1)#代理ip失败害怕被锁。就每1秒换新页面。
    req = urllib.request.Request(urls,data,head)#模拟一个浏览器。只预设了5个，随机取用。
    res = urllib.request.urlopen(req)
    try:
        return res.read().decode('utf-8')
    except:
        print('出错了,这里是读入错误')
        wrong+=1
        f=open("d:/test/log.txt",'a')
        traceback.print_exc(file=f)
        f.flush()
        f.close()
def writefile(dizhi,mingzi,neirong):
    try:
        with open(dizhi+mingzi,'wb')as f:
            f.write(neirong.encode('utf-8'))
    except:
        print('出错了,这里是写入1问题')
        wrong+=1
        f=open("d:/test/log.txt",'a')
        traceback.print_exc(file=f)
        f.flush()
        f.close()
def writefile2(dizhi,mingzi,neirong):
    try:
        with open(dizhi+mingzi,'w')as f:
            f.write(neirong.encode('gbk',errors="ignore"))
    except:
        try:
            with open(dizhi+mingzi,'wb')as fb:
                fb.write(neirong.encode('utf-8'))
        except:
            print('出错了,这里是写入2问题')
            wrong+=1
            f=open("d:/test/log.txt",'a')
            traceback.print_exc(file=f)
            f.flush()
            f.close()
if not os.path.exists(r'd:/test/'):
    os.makedirs(r'd:/test/')
#tieba='%E6%88%98%E5%88%97%E8%88%B0'
targ=input('请输入你想要爬哪个贴吧（字符字符）：')
tieba=urllib.parse.quote(targ)
pageNum='aa'
while(not pageNum.isdigit()):#&pn=50
    pageNum= input('请输入你想要爬多少页（数字数字）：')
k=0
wrong=0
timestart=time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
print(timestart)#存档开始时间
print('开始预处理。。。')
htm = openurl('http://tieba.baidu.com/f?ie=utf-8&kw='+tieba)
writefile('d:/test/','test.txt',htm)
hreflist= re.findall(r'<a.*?target="_blank" class="j_th_tit ".*?</a>',htm)
print('已爬完主页面的第1页。。。')
paged=1
while(int(pageNum)>paged):
    temp2='&pn='+str(paged*50)
    htm = openurl('http://tieba.baidu.com/f?ie=utf-8&kw='+tieba+temp2)
    paged+=1
    temp3= re.findall(r'<a.*?target="_blank" class="j_th_tit ".*?</a>',htm)
    for each in temp3:
        hreflist.append(each)
    print('已爬完主页面的第'+str(paged)+'页。。。')
#for each in hreflist:
#    print(each)
print('开始对贴子进行去重工作。。。')
hreflist.sort()
newhref = []
newhref.append(hreflist[0])
lened = len(hreflist)
for i in range(1,lened):
    if(not hreflist[i]==hreflist[i-1]):
        newhref.append(hreflist[i])
print('主页面已经完全被处理好了')
f=open("d:/test/log.txt",'a')#之前存档的开始时间存进日志
f.write(timestart)
f.flush()
f.close()
for each in newhref:
    try:
        #print(each)
        urlplus = each[9:22]
        f=open("d:/test/log.txt",'a')
        k+=1
        f.write('\n'+urlplus+'\n'+'已经爬了'+str(k)+',共有'+str(wrong)+'个错\n')
        f.write(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))+'\n')
        f.flush()
        f.close()
        print('下面我们来摁下一个页面这个页面的相对地址是'+urlplus)
        #print(urlplus)
        htm = openurl('http://tieba.baidu.com'+urlplus)#进入到每个帖子里去
        pattern=re.compile(r'<h3 class="core_title_txt pull-left text-overflow .*?>(.*?)</h3>',re.S)
        print('http://tieba.baidu.com'+urlplus)
        title=re.findall(pattern,htm)#找出这个帖子的title
        #print(title[0])
        print('这个页面title叫'+title[0])
        a=k*60//lened
        print('>'*a+'-'*(60-a)+'%.2f' % (k*100/lened)+'%'+time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())))#进度条
        #writefile('d:/test/','code'+title[0]+'.txt',htm)#先把原文件写入
        pattern= re.compile(r'<li class="l_reply_num".*? style="margin-right:3px">(.*?)</span>.*?<span class="red">(.*?)</span>',re.S)
        page= re.findall(pattern,htm)#查出这个帖子有多少回复和分页
        reply= page[0][0]
        pag= page[0][1]
        tryy=1
        conts=[]
        while (int(pag)>=tryy):
            pattern=re.compile(r'<div id="post_content_.*?>(.*?)</div>',re.S)
            items=re.findall(pattern,htm)#找出每一条留言
            pattern=re.compile(r'alog-group="p_author".*?class="p_author_name.*?target="_blank">(.*?)</a>',re.S)
            authors=re.findall(pattern,htm)#对应的每一条留言的作者
            ii=0#用来同步加入每一楼作者昵称
            for item in items:
                temp=str(authors[ii])+':===='+str(replace(item))
                conts.append(temp)
                ii+=1
            #break
            if(int(pag)>tryy):
                tryy+=1
                urlplusplus='?pn='+str(tryy)#同样的方法进入下一页
                htm = openurl('http://tieba.baidu.com'+urlplus+urlplusplus)
            else:
                break
        ss=title[0]+'\n'
        for cont in conts:
            ss=ss+cont+'\r\n'
        #writefile2('d:/test/',title[0]+'.txt',ss)
        writefile2('d:/test/',urlplus[3:]+'.txt',ss)
    except:
        print('出错了,这里我也很绝望，看log.txt吧')
        wrong+=1
        f=open("d:/test/log.txt",'a')
        traceback.print_exc(file=f)
        f.flush()
        f.close()
