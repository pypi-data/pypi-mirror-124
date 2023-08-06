'''
写一个函数代码，返回这3个数字中最大的一个
'''
# a = 123
# b = 345
# c = 444
# def max_num(first,second,end):
#     if first>second:
#         if first>end:
#             return first
#         else:
#             return end
#     elif first<second:
#         if second>end:
#             return second
#         else:
#             return end
#
# def max_num1(first,second,end):
#     if first>second and first>end:
#         return first
#     elif second>first and second>end:
#         return second
#     elif end>first and end>second:
#         return end
# max_num=max_num1(c,b,a)
# print(max_num)
import collections

import psutil

'''
分别写2个函数，完成下面的功能：

提示一下用到函数的：**和*，猩猩是字典，星是元组

2.1 调用函数：ainfo(x=88,y=22,z=44) 你定义ainfo函数体里面的内容并且返回结果： 

[22, 44, 88]

2.2 调用函数：cinfo(x=88,y=22,z=44) 你定义cinfo函数体里面的内容并且返回结果：

('xaay','yaay','zaay')
'''

'''
要求如下：

1.该文本里，有多少个用户。（要求：输出为一个整数。）
'''

# import linecache
# import time
#
# now = time.time()
#
# # 前期准备
# data_keys = ('bid', 'uid', 'username', 'v_class', 'content', 'img', 'created_at', 'source', 'rt_num', 'cm_num', 'rt_uid', 'rt_username', 'rt_v_class', 'rt_content', 'rt_img', 'src_rt_num', 'src_cm_num', 'gender', 'rt_bid', 'location', 'rt_mid', 'mid', 'lat', 'lon', 'lbs_type', 'lbs_title', 'poiid', 'links', 'hashtags', 'ats', 'rt_links', 'rt_hashtags', 'rt_ats', 'v_url', 'rt_v_url')
#
#
# keys = {data_keys[k]:k for k in range(0,len(data_keys))}
#
# f = linecache.getlines('t.txt')
#
# lines = [x[1:-1].split('","') for x in f] #拆分
# # 1 输出用户总数
#
# users = set([line[keys['username']] for line in lines])
#
# user_total = len(set(users))
#
# assert type(user_total) == int
#
# # 2 每一个用户的名字 list
#
# users = list(users)
# assert type(users) == list
#
# # 3 有多少个2012年11月发布的tweets
#
# lines_from_2012_11 = list(filter(lambda line: line[keys['created_at']].startswith('2012-11'), lines))
#
# lines_total_from_2012_11 = len(lines_from_2012_11)
#
# assert type(lines_total_from_2012_11) == int
#
# # 4 该文本里，有哪几天的数据？
#
# users_by_date = [line[keys['created_at']].split(' ')[0] for line in lines]
#
# lines_by_created = list(set(users_by_date))
#
# lines_by_created.sort()
#
# assert type(lines_by_created) == list
#
# # 5 该文本里，在哪个小时发布的数据最多？
# # todo 这里用time模块做时间转换最好。下例只为讲解拆分方法
#
# hours = [int(line[keys['created_at']][11:13]) for line in lines]
#
# total_by_hour = [(h, hours.count(h)) for h in range(0, 24)]
#
# total_by_hour.sort(key=lambda k: k[1], reverse=True)
#
# max_hour = total_by_hour[0][0]
#
# assert type(max_hour) == int
#
# # 6 该文本里，输出在每一天发表tweets最多的用户
#
# dateline_by_user = {k: dict() for k in lines_by_created}
#
# for line in lines:
#     dateline = line[keys['created_at']].split(' ')[0]
#     username = line[keys['username']]
#     if dateline_by_user[dateline].has_key(username):
#         dateline_by_user[dateline][username] += 1
#     else:
#         dateline_by_user[dateline][username] = 1
#
# for k, v in dateline_by_user.items():
#     us = v.items()
#     us.sort(key=lambda k: k[1], reverse=True)
#     dateline_by_user[k] = {us[0][0]: us[0][1]}
#
# assert type(dateline_by_user) == dict
#
# # 7 请按照时间顺序输出 2012-11-03 每个小时的发布tweets的频率
#
# lines_from_2012_11_03 = filter(lambda line: line[keys['created_at']].startswith('2012-11-03'), lines)
#
# hourlines_from_2012_11_03 = {str(i): 0 for i in range(0, 24)}
#
# for line in lines_from_2012_11_03:
#     hour = line[keys['created_at']][11:13]
#     hourlines_from_2012_11_03[str(int(hour))] += 1
#
# hour_timeline_from_2012_11_03 = [(k, v) for k, v in hourlines_from_2012_11_03.items()]
# hour_timeline_from_2012_11_03.sort(key=lambda k: int(k[0]))
#
# assert type(hour_timeline_from_2012_11_03) == list
#
# # 8 统计该文本里，来源的相关信息和次数
#
# source = set([k[keys['source']] for k in lines])
# source_dict = {s: 0 for s in source}
# for line in lines:
#     source_name = line[keys['source']]
#     source_dict[source_name] += 1
# source_list = [(k, v) for k, v in source_dict.items()]
# source_list.sort(key=lambda k: k[1], reverse=True)
# assert type(source_list) == list
#
# # 9 计算转发URL中：以："https://twitter.com/umiushi_no_uta"开头的有几个
#
# umi_total = 0
# for line in lines:
#     if line[keys['rt_v_url']].startswith('https://twitter.com/umiushi_no_uta'):
#         umi_total += 1
# assert type(umi_total) == int
#
# # 10 UID为573638104的用户 发了多少个微博
#
# tweets_total_from_573638104 = 0
# for line in lines:
#     if line[keys['uid']] == '573638104':
#         tweets_total_from_573638104 += 1
# assert type(tweets_total_from_573638104) == int
#
#
# # 11 定义一个函数，该函数可放入任意多的用户uid参数（如果不存在则返回null），函数返回发微薄数最多的用户uid。
#
# def get_user_by_max_tweets(*uids):
#     '''
#     @deprecated:参数可为字符串或者数字
#     '''
#
#     if len(uids) > 0:
#         uids = filter(lambda u: type(u) == int or u.isdigit(), uids)
#         uids = list(map(str, uids))
#         if len(uids) > 0:
#             uids_dict = {x: 0 for x in uids}
#             for line in lines:
#                 uid = line[keys['uid']]
#                 if uid in uids:
#                     uids_dict[uid] += 1
#             uids_and_tweets_total = [(x, y) for x, y in uids_dict.items()]
#             uids_and_tweets_total.sort(key=lambda k: k[1], reverse=True)
#             return uids_and_tweets_total[0][0]
#     return "null"
#
#
# assert get_user_by_max_tweets() == 'null'
# assert get_user_by_max_tweets('ab', 'cds') == 'null'
# assert get_user_by_max_tweets('ab', 'cds', '123b') == 'null'
# assert get_user_by_max_tweets('12342', 'cd') == '12342'
# assert get_user_by_max_tweets('28803555', 28803555) == '28803555'
# assert get_user_by_max_tweets('28803555', 28803555, '96165754') == '28803555'
#
# # 12 该文本里，谁发的微博内容长度最长
#
# lines_by_content_length = [(line[keys['username']], len(line[keys['content']])) for line in lines]
# lines_by_content_length.sort(key=lambda k: k[1], reverse=True)
# user_by_max_content = lines_by_content_length[0][0]
# # todo 如果有多个最多怎么办？
# assert type(user_by_max_content) == str
#
# # 13 该文本里，谁转发的URL最多
#
# lines_by_rt = [(line[keys['uid']], int(line[keys['rt_num']])) for line in lines if line[keys['rt_num']] != '']
# lines_by_rt.sort(key=lambda k: k[1], reverse=True)
# user_by_max_rt = lines_by_rt[0][0]
# assert type(user_by_max_rt) == str
#
# # 14 该文本里，11点钟，谁发的微博次数最多。
#
# lines_on_hour11 = filter(lambda line: line[keys['created_at']].startswith('11', 11, 13), lines)
# lines_by_uid_on_hour11 = {k[keys['uid']]: 0 for k in lines_on_hour11}
# for line in lines_on_hour11:
#     uid = line[keys['uid']]
#     lines_by_uid_on_hour11[uid] += 1
# d = [(k, v) for k, v in lines_by_uid_on_hour11.items()]
# d.sort(key=lambda k: k[1], reverse=True)
# uid_by_max_tweets_on_hour11 = d[0][0]
#  todo 如果有多个最多怎么办？
# assert type(uid_by_max_tweets_on_hour11) == str
#
# # 15 该文本里，哪个用户的源微博URL次数最多。 （要求：输出用户的uid，字符串格式。）
#
# uid_by_v_url = {k[keys['uid']]: 0 for k in lines}
# for line in lines:
#     uid = line[keys['uid']]
#     if lines[keys['v_url']] != '':
#         uid_by_v_url[uid] += 1
# uid_sort_by_v_url = [(k, v) for k, v in uid_by_v_url.items()]
# uid_sort_by_v_url.sort(key=lambda k: k[1], reverse=True)
# uid_by_max_v_url = uid_sort_by_v_url[0][0]
#  todo 如果有多个最多怎么办？
# assert type(uid_by_max_v_url) == str
#
# print('运算时间：%s' % (time.time() - now))  # 整体运行时间

import time


# print(time.time()) # 获取时间戳,默认单位为秒，结果乘1000可以转换为毫秒
#
# t1=time.time()#时间戳
# print(t1)
# time.sleep(2)
# t2=time.localtime()#时间元组
# time.sleep(2)
# print(t2)
# print(time.mktime(t2))#时间元组转化成时间戳
# print(time.localtime(t1))#时间戳转化成时间元组
# time.sleep(2)
# t3 = time.asctime()#时间字符串
# print(t3)
# #时间戳转化成时间字符串
# print(time.ctime(t1))
#时间元组转化成指定格式的时间字符串
# t4="2021-10-20 11:24:00"
# print(time.strftime("%Y-%m-%d %H:%M:%S",time.localtime()))
# print(time.strftime("%H:%M:%S",time.localtime()))
# t6 = time.strftime("%H:%M:%S",time.localtime())
# print(time.strptime(t6,"%H:%M:%S"))
#将时间字符串转化成时间元组

# t5=time.strptime(t4,"%Y-%m-%d %H:%M:%S")
# print(t5)
# print(time.mktime(t5))
import os

# print(os.getcwd())
# os.chdir("..")
# print(os.getcwd())
# os.chdir("./stu")
# print(os.getcwd())
# print(os.listdir())
# os.mkdir("test")
# print(os.listdir())
# os.rmdir("test")
# print(os.listdir())
# # os.makedirs("test/test.py")
# os.chdir("./test")
# print(os.listdir())
# os.chdir("..")
# os.removedirs("test/test.py")
# print(os.listdir())
# os.makedirs("test/test.py")
# os.chdir("./test")
# os.rename("test.py",'newname.py')
# print(os.listdir())
# os.chdir("./test")
# os.remove("newname.py")
# print(os.listdir())
# print(os.path.abspath("./stu0915.py"))
# print(os.path.dirname(os.path.abspath("./stu0915.py")))
# print(os.path.basename(os.path.abspath('./stu0915.py')))
# os.chdir("./wxuiato")
# print(os.path.exists('outputs'))
# print(os.path.isabs("F:\stu\stu0915.py"))

def test_os(func,args):
    print(func(args))
# add_time=test_os(os.path.getatime,'test')
# m_time = test_os(os.path.getmtime,'test')
# c_time = test_os(os.path.getctime,'test')
# file_size = test_os(os.path.getsize,'test')
# print(file_size)
# add_time=time.ctime(add_time)
# m_time = time.ctime(m_time)
# c_time = time.ctime(c_time)
# print(add_time)
# print(m_time)
# print(c_time)

# import sys
# for index,args in enumerate(sys.argv):
#     print("第%d个参数是:%s"%(index,args))

import inspect

# print(inspect.signature(psutil.cpu_percent))

def func2(f):
    print("enter func2")
    def innter_func2():
        print('inner_func2')
        f()
        print('exit inner_func2')
    return innter_func2

def func1(f):
    print("enter func1")
    def innter_func1():
        print('inner_func1')
        f()
        print('exit inner_func1')
    return innter_func1

@func2
@func1
def fun_a():
    print("hello word")


fun_a()