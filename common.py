# -*- coding: utf-8 -*-”
import win32clipboard
import os
import psutil
import time
from email.mime.text import MIMEText
from email.header import Header
from smtplib import SMTP_SSL
import win32api, win32con
import sys
import datetime
import calendar
# 加密
import base64
# noinspection SpellCheckingInspection
from Crypto.Cipher import PKCS1_v1_5 as Cipher_pksc1_v1_5
from Crypto.PublicKey import RSA
import re

from Cryptodome.Cipher import AES
from Cryptodome import Random
from binascii import unhexlify
from binascii import hexlify
import wmi
import hashlib
from configobj import ConfigObj

date = str(time.strftime('%Y%m%d', time.localtime(time.time())))

def use_times(func):
    def wrapped_func(*args, **kwargs):
        start = time.time()
        func(*args, **kwargs)
        info_time = change_time(int(time.time() - start))
        print('[info]耗时：{} '.format(info_time))
        errorbox("[处理完成，info]耗时:{}".format(info_time))

    return wrapped_func


def pc_info():
    pc = wmi.WMI()
    # cpu_id
    # print(pc.Win32_Processor()[0])
    cupid = pc.Win32_Processor()[0].ProcessorId.strip()
    # print(cupid)
    # boards
    boards_uuid = pc.Win32_BaseBoard()[0].qualifiers['UUID'][1:-1]
    # print(boards_uuid)
    boards_num = pc.Win32_BaseBoard()[0].SerialNumber
    # print(boards_num)
    # Disk
    disk_uuid = pc.Win32_DiskDrive()[0].qualifiers['UUID'][1:-1]
    # print(disk_uuid)
    mac = cupid + boards_uuid + boards_num + disk_uuid
    # print(mac)
    # 进行MD5加密
    hl = hashlib.md5()
    hl.update(mac.encode())
    my_info = hl.hexdigest()
    # print("机器码： %s" % my_info)
    return my_info


def keygen(data):
    # 要加密的明文
    # data = '3432aaa323_asd234-DDf'
    # 密钥key 长度必须为16（AES-128）、24（AES-192）、或32（AES-256）Bytes 长度.
    # 目前AES-128足够用
    key = '你来打我啊! 呵呵!'.encode()
    # print(type(key))
    # 生成长度等于AES块大小的不可重复的密钥向量
    iv = Random.new().read(AES.block_size)
    # print(iv)
    # 使用key和iv初始化AES对象, 使用MODE_CFB模式
    my_cipher = AES.new(key, AES.MODE_CFB, iv)
    # 加密的明文长度必须为16的倍数，如果长度不为16的倍数，则需要补足为16的倍数
    # 将iv（密钥向量）加到加密的密文开头，一起传输
    cipher_text = iv + my_cipher.encrypt(data.encode())
    # 解密的话要用key和iv生成新的AES对象
    my_decrypt = AES.new(key, AES.MODE_CFB, cipher_text[:16])
    # 使用新生成的AES对象，将加密的密文解密
    decrypt_text = my_decrypt.decrypt(cipher_text[16:])
    # print('密钥key为：%s'% key.decode())
    print("【注册信息如下】")
    print('机器码：', decrypt_text.decode())
    print('注册码：', hexlify(cipher_text).decode())
    loggers = hexlify(cipher_text).decode()
    return loggers


# noinspection PyBroadException
def decoder(text_info, my_pc_infos):
    key = '你来打我啊! 呵呵!'.encode()
    # 编码
    text_infos = text_info.encode()
    # print(text_infos)
    # 返译 十六 到 二进
    try:
        cipher_text = unhexlify(text_infos)
        # print(cipher_text)
        # 解密的话要用key和iv生成新的AES对象
        my_decrypt = AES.new(key, AES.MODE_CFB, cipher_text[:16])
        # 使用新生成的AES对象，将加密的密文解密
        decrypt_text = my_decrypt.decrypt(cipher_text[16:])
        end_code = decrypt_text.decode()
    except:
        return False
    # print('机器码：', decrypt_text.decode())
    if end_code == my_pc_infos:
        # print("匹配成功")
        return True
    else:
        return False


# [软件]
def check_info():
    # 获取机器码
    my_pc_info = pc_info()
    # print(my_pc_info)
    # 获取注册码
    # a.配置获取
    # print(common.is_file(r"_tmp\config.ini"))
    if is_file(r"_tmp\config.ini"):
        config = ConfigObj(r"_tmp\config.ini", encoding='UTF8')
        # 读配置
        # print(config['test_section'])
        # print(config['logger_section']['logger_param'])
        logger_info = config['logger_section']['logger_param']
    else:
        # b.input 获取
        print("机器码：{} [如未注册，发送给，开发者注册]".format(my_pc_info))
        logger_info = input("【校准】未发现注册信息，请输入注册码：")
    # 校验注册
    if logger_info in ["root", "superman"]:
        print("跳过注册...")
    else:
        if decoder(logger_info, my_pc_info):
            if not is_file(r"_tmp\config.ini"):
                # 保存注册码到配置信息
                config = ConfigObj(r"_tmp\config.ini", encoding='UTF8')
                config['logger_section'] = {}
                config['logger_section']['logger_param'] = logger_info
                config.write()
                print("注册成功")
        else:
            print("校验失败，请关闭重启动进行注册...")
            del_dir(r"_tmp\config.ini")
            errorbox("校验失败，请关闭重启动进行注册...")
            time.sleep(2)
            sys.exit()


# 判断变量类型的函数
def typeof(variate):
    types = None
    if isinstance(variate, int):
        types = "int"
    elif isinstance(variate, str):
        types = "str"
    elif isinstance(variate, float):
        types = "float"
    elif isinstance(variate, list):
        types = "list"
    elif isinstance(variate, tuple):
        types = "tuple"
    elif isinstance(variate, dict):
        types = "dict"
    elif isinstance(variate, set):
        types = "set"
    return types


# 返回变量类型
def gettype(variate):
    arr = {"int": "整数", "float": "浮点", "str": "字符串", "list": "列表", "tuple": "元组", "dict": "字典", "set": "集合"}
    var_type = typeof(variate)
    if not (var_type in arr):
        return "未知类型"
    return arr[var_type]


def zh_exist(contents):
    zh_model = re.compile(u'[\u4e00-\u9fa5]')  # 检查中文
    match = zh_model.search(contents)
    if match: return True


def exist_str(words, str_in):
    if words in str_in:
        return True
    else:
        return False


cum_id = {"1": "A", "2": "B", "3": "C", "4": "D", "5": "E", "6": "F", "7": "G", "8": "H", "9": "I", "10": "J",
          "11": "K", "12": "L", "13": "M", "14": "N", "15": "O", "16": "P", "17": "Q", "18": "R", "19": "S", "20": "T",
          "21": "U", "22": "V", "23": "W", "24": "X", "25": "Y", "26": "Z", "27": "AA", "28": "AB", "29": "AC",
          "30": "AD",
          "31": "AE", "32": "AF"}


def num_char(num):
    """数字转中文"""
    num = str(num)
    # new_str=""
    num_dict = {"0": u"零", "1": u"一", "2": u"二", "3": u"三", "4": u"四", "5": u"五", "6": u"六", "7": u"七", "8": u"八",
                "9": u"九"}
    list_num = list(num)
    # print(list_num)
    shu = []
    for i in list_num:
        # print(num_dict[i])
        shu.append(num_dict[i])
    new_str = "".join(shu)
    # print(new_str)
    return new_str


# from PIL import Image
def get_month_day(year=None, month=None):
    """
    :year: 年份，默认是本年，可传int或str类型
    :month: 月份，默认是本月，可传int或str类型
    firstDay: 当月的第一天，datetime.date类型
    lastDay: 当月的最后一天，datetime.date类型
    """
    if year:
        year = int(year)
    else:
        year = datetime.date.today().year
    if month:
        month = int(month)
    else:
        month = datetime.date.today().month
    # 获取当月第一天的星期和当月的总天数
    first_day_week, month_range = calendar.monthrange(year, month)
    # 获取当月的第一天
    first_day = datetime.date(year=year, month=month, day=1).strftime('%Y-%m-%d')
    last_day = datetime.date(year=year, month=month, day=month_range).strftime('%Y-%m-%d')
    # 返回列表 str 列表
    return [first_day, last_day]


def get_use_date(go_true=False, go_end=3, go_start=8):
    end_month = int(str(time.strftime('%m', time.localtime(time.time()))))
    end_year = int(str(time.strftime('%Y', time.localtime(time.time()))))
    if go_true:
        end_month -= go_end
        if end_month <= 0:
            end_month += 12
            end_year -= 1
        start_month = 1
        start_year = end_year
    # if go_true:
    #     start_month = end_month - go_start
    #     start_year = end_year
    #     if start_month <= 0:
    #         start_month += 12
    #         start_year -= 1
    else:
        start_month = 1
        start_year = end_year
    return [[start_year, start_month], [end_year, end_month]]


def convert_image(img, standard=127.5):
    # 1) 将图片进行降噪处理, 通过二值化去掉后面的背景色并加深文字对比度
    # 【灰度转换】
    image = img.convert('L')
    # 【二值化】
    # 根据阈值 standard , 将所有像素都置为 0(黑色) 或 255(白色), 便于接下来的分割
    pixels = image.load()
    for x in range(image.width):
        for y in range(image.height):
            if pixels[x, y] > standard:
                pixels[x, y] = 255
            else:
                pixels[x, y] = 0
    return image
    # 设置打开路径


# noinspection SpellCheckingInspection
def encrpt(word):
    public_key = ('-----BEGIN PUBLIC KEY-----\n'
                  'MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQCwjDm1HXDw8QH5ZtGMQIl2h/I8E+chOQA8aQ8xCR/+aHnROaN/ZU5Vmd2Zz7g6cAacR9BSm60+iSCYtvEGJKl0WqvbPGJkc8tedjNF1QqgWqkkuE6Udgw2OkEKJCxDg6PrAniR7Cc0io9G8bW4P8JDJjSbbafvMPDDFbVVUWJxxwIDAQAB\n'
                  '-----END PUBLIC KEY-----\n')
    rsakey = RSA.importKey(public_key)
    # noinspection PyTypeChecker
    cipher = Cipher_pksc1_v1_5.new(rsakey)
    cipher_text = base64.b64encode(cipher.encrypt(word.encode()))
    return cipher_text.decode()


# 过期检测：
def deadline():
    times = "2019/12/30 23:59:59"
    out_time = datetime.datetime.strptime(times, "%Y/%m/%d %H:%M:%S")
    # print(out_time)
    plan_time = datetime.datetime.now()
    # print(plan_time)
    dif = int((out_time - plan_time).days)
    # print(dif)
    if dif < 0:
        print("获取时间异常，退出...")
        errorbox("获取时间异常，退出...")
        time.sleep(5)
        sys.exit()
    pass


def error_log():
    error_name = 'errors.txt'
    a, b = 3, 0
    try:
        c = a / b
    except Exception as e:
        print(repr(e))
        with open(error_name, 'w') as f:
            f.write(repr(e))
        print('save error message to {}'.format(error_name))
    else:
        print(c)


# error_log()
def js_value(types, browsers, ids, into_text):  # , fr_lt=None
    # js = None
    if types == "id":
        js = "window.document.getElementById('" + ids + "').value = \"" + into_text + "\";"
        "].contentWindow.document.getElementById('" + ids + "').value = \"" + into_text + "\";"
    else:
        js = "window.document.getElementsByClassName('" + ids + "')[0].value = \"" + into_text + "\";"
    browsers.execute_script(js)


def errorbox(str_text):
    # 告警提醒
    win32api.MessageBox(0, str_text, "提醒", win32con.MB_ICONWARNING)


# noinspection SpellCheckingInspection
def send_mail(send_qq, receive_mail, mail_code, pv_uv):
    # 需要能够连接外网
    now_time = time.strftime("%Y/%m/%d %H:%M", time.localtime())
    # 邮件的正文内容
    if pv_uv[0] == "error":
        mail_content = "[%s]【提醒】小主，工单处理出现异常【%s】啦，快去看吧！！！" % (now_time, pv_uv[0])
    else:
        mail_content = "[%s]【提醒】小主，工单处理：【%s】，很棒棒！！！" % (now_time, pv_uv[0])
    # qq邮箱smtp服务器
    host_server = 'smtp.139.com'
    send_email = send_qq + '@139.com'
    # ssl登录
    smtp = SMTP_SSL(host_server)
    smtp.login(send_qq, mail_code)
    msg = MIMEText(mail_content, _charset='utf-8')
    msg["Subject"] = Header("[" + now_time + "]【温馨提醒】工单运行情况：【" + pv_uv[0] + "】", 'utf-8')
    msg["From"] = send_email
    msg["To"] = receive_mail  # 发多人用列表，重写
    # msg['To'] = ';'.join(receive_mail)  # 发送多人邮件写法
    smtp.sendmail(send_email, receive_mail, msg.as_string())
    smtp.quit()


def is_file(tmp):
    is_exist = os.path.exists(tmp)
    if not is_exist:
        return False
    else:
        return True


def del_dir(tmp):
    # 判断是否存在
    is_exist = os.path.exists(tmp)
    # 目录
    if not is_exist:
        return True
    else:
        os.remove(tmp)
        return False


def mkdir(tmp):
    # 判断是否存在
    is_exist = os.path.exists(tmp)
    # 目录
    if not is_exist:
        os.makedirs(tmp)
        return False
    else:
        return True


# noinspection SpellCheckingInspection,PyBroadException
def use_excel():
    try:
        pids = psutil.pids()
        for pid in pids:
            p = psutil.Process(pid)
            # print('pid-%s,pname-%s' % (pid, p.name()))
            if p.name() == 'EXCEL.EXE':
                return True
            else:
                return False
    except:
        pass


# noinspection SpellCheckingInspection,PyBroadException
def clean_excel():
    # 旧EXCEL
    try:
        pids = psutil.pids()
        for pid in pids:
            p = psutil.Process(pid)
            # print('pid-%s,pname-%s' % (pid, p.name()))
            if p.name() == 'EXCEL.EXE':
                cmd = 'taskkill /F /IM EXCEL.EXE'
                os.system(cmd)
    except:
        pass


# noinspection SpellCheckingInspection,PyBroadException
def clean_old():
    # 清理旧程序
    try:
        pids = psutil.pids()
        for pid in pids:
            p = psutil.Process(pid)
            # print('pid-%s,pname-%s' % (pid, p.name()))
            if p.name() == 'EXCEL.EXE':
                cmd = 'taskkill /F /IM EXCEL.EXE'
                os.system(cmd)
        # 旧驱动
        pids = psutil.pids()
        for pid in pids:
            p = psutil.Process(pid)
            # print('pid-%s,pname-%s' % (pid, p.name()))
            if p.name() == 'chromedriver.exe':
                cmd = 'taskkill /F /IM chromedriver.exe'
                os.system(cmd)
    except:
        pass


# noinspection PyBroadException
def copy(texts):
    text = texts
    win32clipboard.OpenClipboard()
    win32clipboard.EmptyClipboard()
    win32clipboard.SetClipboardText(text, win32clipboard.CF_UNICODETEXT)
    time.sleep(0.1)
    try:
        win32clipboard.CloseClipboard()
    except:
        pass
        time.sleep(0.5)


def paste():
    win32clipboard.OpenClipboard()
    data = win32clipboard.GetClipboardData(win32clipboard.CF_UNICODETEXT)
    win32clipboard.CloseClipboard()
    return data


def change_time(when):
    days = 24 * 60 * 60
    hours = 60 * 60
    minutes = 60
    if when < minutes:
        # 秒级
        my_sec = int(when)
        return "%s秒" % my_sec
    elif when < hours:
        # 分钟级
        my_min = int(when / minutes)
        my_sec = int(when % minutes)
        return "%s分%s秒" % (my_min, my_sec)
    elif when < days:
        # 小时级# 获取分钟# 获取秒
        my_hour = int(when / hours)
        my_min = int(when % hours / minutes)
        my_sec = int(when % hours % minutes)
        return "%s时%s分%s秒" % (my_hour, my_min, my_sec)
    else:
        # 天级 # 小时级# 获取分钟 # 获取秒
        my_day = int(when / days)
        my_hour = int(when % days / hours)
        my_min = int(when % days % hours / minutes)
        my_sec = int(when % days % hours % minutes)
        return "%s天%s时%s分%s秒" % (my_day, my_hour, my_min, my_sec)
