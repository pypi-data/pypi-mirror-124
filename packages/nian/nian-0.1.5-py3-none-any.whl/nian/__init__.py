#初慕苏流年
#Q1274210585
#群556766602
import os
import sys
try:
    from ctypes import *;test=cdll.LoadLibrary('./test.so')
except:
    print('错误的新功能！')


def listqq(url):
    headers={
    'Host': 'i.y.qq.com',
    'user-agent': 'Mozilla/5.0 (Linux; Android 8.1.0; PBAT00 Build/OPM1.171019.026; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/93.0.4577.82 Mobile Safari/537.36',
    }
    a=requests.get(url,headers=headers).text
    list_=eval(re.findall("(?<=\"songlist\":).*?(?=},\"seoData\")",a)[0])
    l_=[]
    for i in list_:
        l_.append(i['name'])
    return l_
#测试版qq歌单获取，不全，后续更新
#返回歌名列表








def wy(music,s,t):aaaa=json.loads(requests.get("http://music.163.com/api/search/get/web?csrf_token=hlpretag=&hlposttag=&s="+music+"&type=1&offset=0&total=true&limit=20").text);aa=[aaaa["result"]["songs"][i]["id"] for i in range(6)];a=int(s);a=["http://music.163.com/song/media/outer/url?id="+str(aa[a])+".mp3",aaaa["result"]["songs"][a]["name"]+"-"+aaaa["result"]["songs"][s]["artists"][0]["name"]] if t==True else "http://music.163.com/song/media/outer/url?id="+str(aa[a])+".mp3";return a
def qq(music,s,t):aaa = requests.get("https://c.y.qq.com/soso/fcgi-bin/client_search_cp?ct=24&qqmusic_ver=1298&new_json=1&remoteplace=txt.yqq.song&searchid=61460539676714578&t=0&aggr=1&cr=1&catZhida=1&lossless=0&flag_qc=0&p=1&n=10&w={0}&g_tk_new_20200303=5381&g_tk=5381&loginUin=0&hostUin=0&format=json&inCharset=utf8&outCharset=utf-8&notice=0&platform=yqq.json&needNewCode=0".format(music));aaaa=json.loads(aaa.text);nian=aaaa["data"]["song"]["list"];bb=[];bb=[music["title"]+"-"+music["singer"][0]["title"] for music in nian];aaa=json.loads(requests.get("https://u.y.qq.com/cgi-bin/musicu.fcg?format=json&data=%7B%22req_0%22%3A%7B%22module%22%3A%22vkey.GetVkeyServer%22%2C%22method%22%3A%22CgiGetVkey%22%2C%22param%22%3A%7B%22guid%22%3A%22358840384%22%2C%22songmid%22%3A%5B%22{}%22%5D%2C%22songtype%22%3A%5B0%5D%2C%22uin%22%3A%221443481947%22%2C%22loginflag%22%3A1%2C%22platform%22%3A%2220%22%7D%7D%2C%22comm%22%3A%7B%22uin%22%3A%2218585073516%22%2C%22format%22%3A%22json%22%2C%22ct%22%3A24%2C%22cv%22%3A0%7D%7D".format(aaaa["data"]["song"]["list"][int(s)]['mid'])).text);aa=aaa['req_0']['data']['midurlinfo'][0]['purl'];a=["https://isure.stream.qqmusic.qq.com/"+aa,bb[s]] if t==True else "https://isure.stream.qqmusic.qq.com/"+aa;return a
def kg(music,s,t):b=music;a=json.loads(requests.get("http://msearchcdn.kugou.com/api/v3/search/song?showtype=14&highlight=em&pagesize=30&tag_aggr=1&tagtype=%E5%85%A8%E9%83%A8&plat=0&sver=5&keyword={}&correct=1&api_ver=1&version=9108&page=1&area_code=1&tag=1&with_res_tag=1".format(b)).text[23:-21]);aa=[a["data"]["info"][i]["hash"] for i in range(6)];bb=[a["data"]["info"][i]["album_id"] for i in range(6)];c,s=int(s),requests.Session();headers={"Host": "www.kugou.com","Connection": "keep-alive","Cache-Control": "max-age=0","Upgrade-Insecure-Requests": "1","User-Agent": "Mozilla/5.0 (Linux; Android 8.1.0; PBAT00 Build/OPM1.171019.026; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/62.0.3202.84 Mobile Safari/537.36","dnt": "1","Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8","Referer": "http://www.kugou.com/yy/index.php?r=play/getdata&hash=f8784ebfbae36b324ec1e3441b6156b4&album_id=1645030&_=","Accept-Encoding": "gzip, deflate","Accept-Language": "zh-CN,en-US;q=0.9","Cookie": "kg_mid=99d022a988b55c42e89a27dfa084fdac; kg_dfid=0Qi8qz2gH29M3dfNNl2aQ6cD; kg_dfid_collect=d41d8cd98f00b204e9800998ecf8427e; KuGooRandom=66531611627702529; Hm_lvt_aedee6983d4cfc62f509129360d6bb3d=1611627606; Hm_lpvt_aedee6983d4cfc62f509129360d6bb3d=1611636395","X-Requested-With": "mark.via","If-Modified-Since": "","If-None-Natch": ""};a=[json.loads(s.get("http://www.kugou.com/yy/index.php?r=play/getdata&hash="+aa[c]+"&album_id="+bb[c]+"&_",headers=headers,allow_redirects=False).text)["data"]["play_url"],a["data"]["info"][c]["filename"]] if t==True else json.loads(s.get("http://www.kugou.com/yy/index.php?r=play/getdata&hash="+aa[c]+"&album_id="+bb[c]+"&_",headers=headers,allow_redirects=False).text)["data"]["play_url"];return a
def dy(url):print("测试功能,随时删除");url_string=url;print("解析302地址中......");r = requests.head(url_string, stream=True);print("获取视频ID中......");a="https://www.iesdouyin.com/web/api/v2/aweme/iteminfo/?item_ids="+r.headers['Location'][38:57];print("获取链接ID中......");b="https://aweme.snssdk.com/aweme/v1/play/?video_id="+json.loads(requests.get(a).text)["item_list"][0]["video"]["vid"]+"&ratio=720p&line=0";return b
def kw(song):keyword = requests.utils.quote(song);s = requests.session();url = 'https://kuwo.cn/';headers = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9','Accept-Encoding': 'gzip, deflate, br','Accept-Language': 'zh-CN,zh;q=0.9','Cache-Control': 'no-cache','Connection': 'keep-alive','Host': 'kuwo.cn','Pragma': 'no-cache','Sec-Fetch-Dest': 'document','Sec-Fetch-Mode': 'navigate','Sec-Fetch-Site': 'none','Sec-Fetch-User': '?1','Upgrade-Insecure-Requests': '1','User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36',};s.get(url, headers=headers);csrf = s.cookies.get_dict()['kw_token'];url = f'https://kuwo.cn/api/www/search/searchMusicBykeyWord?key={keyword}&pn=1&rn=30&httpsStatus=1';headers = {'csrf': csrf,'Referer': f'https://kuwo.cn/search/list?key={keyword}','User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36',};r = s.get(url, headers=headers).json();rid = jsonpath.jsonpath(r, '$..rid')[0];url = f'https://kuwo.cn/url?format=mp3&rid={rid}&response=url&type=convert_url3&br=128kmp3&from=web&t=1614342354424&httpsStatus=1';headers = {'Accept': 'application/json, text/plain, */*','Accept-Encoding': 'gzip, deflate, br','Accept-Language': 'zh-CN,zh;q=0.9','Cache-Control': 'no-cache','Connection': 'keep-alive','Host': 'kuwo.cn','Pragma': 'no-cache','Referer': f'https://kuwo.cn/search/list?key={keyword}','Sec-Fetch-Dest': 'empty','Sec-Fetch-Mode': 'cors','Sec-Fetch-Site': 'same-origin','User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36',};r = s.get(url, headers=headers).json();music_url = r.get("url");return music_url
#抖音主页 dyzy 新功能！！！
def nianui():
    print('请确定你的系统为 Ubuntu 并安装wget mpg123等')
    from nian import nianuitest
    nianuitest()
def dyzy(url):
    a=requests.head(url,stream=True)
    b=re.findall('&sec_uid=(.*?)&did',a.headers['location'])
    #https://www.iesdouyin.com/share/user/65619434591?with_sec_did=1&u_code=2b2ajceda7hb&sec_uid=MS4wLjABAAAAkNW8tWhCYYzv2e8G43uI46mnSQH2NKXBGHfnJcpINAg&did=MS4wLjABAAAAGaiKVkT8beqe-wGq4l7N3c1-8t-3vGTHUwJbCetQjng&iid=MS4wLjABAAAAAFFb9CzHLceZZDHZyTlw3uVT2eZi2xz6q-XuGU7QJlqcUF3V0PH9SHWltw0NTrQ6&timestamp=1621932323&utm_source=copy&utm_campaign=client_share&utm_medium=android&share_app_name=douyin
    #主页
    #https://www.iesdouyin.com/web/api/v2/aweme/post/?sec_uid=MS4wLjABAAAAkNW8tWhCYYzv2e8G43uI46mnSQH2NKXBGHfnJcpINAg&count=21&max_cursor=0&aid=1128&_signature=BfCy5AAAZWEyk7w6JGwabQXwsv&dytk=
    #json
    #CJeumwAAaEE.9KBFoVN2NwiXro这个sigh？
    print("测试功能,随时失效  [Debug mode]")
    #print(b)
    url="https://www.iesdouyin.com/web/api/v2/aweme/post/?sec_uid="+b[0]+"&count=100&max_cursor=0&aid=1128&_signature=BfCy5AAAZWEyk7w6JGwabQXwsv&dytk="
    headers={"Host": "www.iesdouyin.com","cache-control": "max-age=0","upgrade-insecure-requests": "1","user-agent": "Mozilla/5.0 (Linux; Android 8.1.0; PBAT00 Build/OPM1.171019.026; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/88.0.4324.181 Mobile Safari/537.36","accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9","dnt": "1","x-requested-with": "mark.via","sec-fetch-site": "none","sec-fetch-mode": "navigate","sec-fetch-user": "?1","sec-fetch-dest": "document","accept-encoding": "gzip, deflate","accept-language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7"}
    a=requests.get(url,headers=headers).text
    b=re.findall('"vid":"(.*?)"',a)
    c=["https://aweme.snssdk.com/aweme/v1/play/?video_id="+i+"&ratio=720p&line=0" for i in b]
    return c
def nianuitest():
    global sou
    try:
        import urwid,os,nian,time
    except:
        print('尝试安装缺失(基于Ubuntu)')
        os.system('pip3 install urwid;su;apt install mpg123 -y')
        print('请重新尝试，或反馈')
        #print('如无法使用请查看系统，或反馈')
    def menu_button(caption, callback):
        button = urwid.Button(caption)
        urwid.connect_signal(button, 'click', callback)
        return urwid.AttrMap(button, None, focus_map='reversed')
    
    def sub_menu(caption, choices):
        contents = menu(caption, choices)
        def open_menu(button):
            return top.open_box(contents)
        return menu_button([caption, u'...'], open_menu)
    
    def menu(title, choices):
        body = [urwid.Text(title), urwid.Divider()]
        body.extend(choices)
        return urwid.ListBox(urwid.SimpleFocusListWalker(body))
    
    def item_chosen(button):
        response = urwid.Text([u'You chose ', button.label, u'\n'])
        done = menu_button(u'Ok', exit_program)
        top.open_box(urwid.Filler(urwid.Pile([response, done])))
    
    def exit_program(button):
        raise urwid.ExitMainLoop()
    def sta(name):
        global i
        print('\n\n\n')
        os.system(f'wget -q "{kg(name,0,True)[0]}" -O ".nian.mp3"')
        sh=f'nohup mpg123 .nian.mp3 &'
        os.system(sh)
        #print(sh)
        #print(sh.read(),'\n')
        print('执行播放\r')
        sh=os.popen('ps -aux|grep "mpg123 .n"')
        a=0
        for i in sh.read().split(' '):
            if len(i)>1:
                a+=1
            if a==2:
                break
        sh.close()
        print('删除日志缓存\n此输出仅用于观看，可忽略不影响使用')
        os.system('rm nohup.out')
    
    def sto(buttion):
        try:
            a=os.system(f'kill {i}')
        except:
            a=1
        if a==0:
            print('\n\n\n停止播放！')
            rm('')
        else:
            print('\n\n\n失败？请反馈？')
            rm('')
    def rm(buttion):
        os.system('rm .nian.mp3')
        print('\n\n\n删除缓存完成！')
    sou=urwid.Edit(u"音乐名称: \n")
    echo=menu_top = menu(u'初慕苏流年 v-0.0.1', [
        sub_menu(u'音乐🎶聚合', [
            sub_menu(u'音乐搜索',[
            sou
            ]),
            
            sub_menu(u'排行榜', [
                menu_button(u'Text Editor', item_chosen),
                menu_button(u'Terminal', item_chosen),
            ]),
            menu_button(u'停止播放并删除缓存(1-5MB)',sto),
        ]),
        
        
    ])
    class CascadingBoxes(urwid.WidgetPlaceholder):
        max_box_levels = 4
        def __init__(self, box):
            super(CascadingBoxes, self).__init__(urwid.SolidFill(u'/'))
            self.box_level = 0
            self.open_box(box)
    
        def open_box(self, box):
            self.original_widget = urwid.Overlay(urwid.LineBox(box),
                self.original_widget,
                align='center', width=('relative', 80),
                valign='middle', height=('relative', 80),
                min_width=24, min_height=8,
                left=self.box_level * 3,
                right=(self.max_box_levels - self.box_level - 1) * 3,
                top=self.box_level * 2,
                bottom=(self.max_box_levels - self.box_level - 1) * 2)
            self.box_level += 1
    
        def keypress(self, size, key):
            global sou
            if key == 'esc' and self.box_level > 1:
                self.original_widget = self.original_widget[0]
                self.box_level -= 1
            elif key=='q':
                raise urwid.ExitMainLoop()
            elif key=='p':
                print(echo)
                
            elif key=='enter' and len(sou.edit_text)>0:
                sta(sou.edit_text)
                self.original_widget = self.original_widget[0]
                self.box_level -= 1
                sou.edit_text=''
            else:
                return super(CascadingBoxes, self).keypress(size, key)
    top = CascadingBoxes(menu_top)
    urwid.MainLoop(top, palette=[('reversed', 'standout', '')]).run()
def import_(path):
    dirs = os.listdir(path)
    o=''
    with open('_init_.py','w+') as w:
        for i in dirs:
            o+=f"from {path.replace('/','.')}.{i.split('.')[0]} import *\n"
        w.write(o)
    import _init_
def c():
    return test