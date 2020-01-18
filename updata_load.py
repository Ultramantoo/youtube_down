#!/usr/bin/env python
# coding: utf-8
# from os import rename
import time
from os import path
import win32ui
# import sys
# import re
import datetime
import common

import youtube_dl
import schedule
import xlwings as wx

'''
流程
1.读取表信息 包括配置信息 下载信息
2.轮询下载表频道
3.下载完成一个记录日期，记录数
4.下载错误或异常，跳过式下班
5.文件处理完成，同步备份到百度网盘
6.完成下载，等待下次轮询
'''
"""
其他，及时集合下载

20191206 目标
完成读表导入数据
完成会类，生成每日
"""


# noinspection SpellCheckingInspection
class GetItem(object):

    def __init__(self):
        # 打开表配置信息
        config_files = self.file_path()
        print(config_files)
        config_file = config_files[0]
        # 打开表格
        visible_in = True
        app = wx.App(visible=visible_in, add_book=False)
        self.wb_info = app.books.open(config_file)
        # 获取列表数
        self.sheet_list = self.wb_info.sheets

    def file_path(self, info_path=None):
        # info_path = None
        # common.deadline()
        # 创建文件获取路径
        common.mkdir("_tmp")
        common.del_dir(r"_tmp\tmp_text.txt")
        print("读取配置信息...")
        # 1表示打开文件对话框
        with open(r'_tmp\filepath.txt', 'w') as f:
            # print("写入")
            f.write('Hello, world!')
        # 1表示打开文件对话框
        file = path.abspath(r'_tmp\filepath.txt')
        # print(file)
        files = file.replace(r'filepath.txt', "")
        files_s = file.replace(r'_tmp\filepath.txt', "")
        # 注册码校准
        # common.check_info()
        # print(files)
        # print(files_s)
        print("导入文件...请选择需要导入的文件")
        if info_path is None:
            dlg = win32ui.CreateFileDialog(1)
            dlg.SetOFNInitialDir(files_s)  # 设置打开文件对话框中的初始显示目录
            dlg.DoModal()
            filename = dlg.GetPathName()  # 获取选择的文件路径
        else:
            filename = files_s + info_path
        # print(filename)
        # 读取创建一个新的，并写入保存，关闭
        with open(r'_tmp\filepath.txt', 'w') as f:
            # print('正在写入')
            f.write(filename)
        # print([filename, files_s, files])
        return [filename, files_s, files]

    @staticmethod
    def rename_hook(d):
        # 重命名下载的视频名称的钩子
        print(d['status'])
        if d['status'] == 'finished':
            print(d['filename'])
            # file_name = r'D:\text2{}.mp4'.format(int(time.time()))
            # rename(d['filename'], file_name)
            # print('下载完成')
        elif d['status'] == "downloading":
            print(d['fragment_count'])

    def deal_gather(self):
        # 处理其本设置
        set_sheet = [sheet for sheet in self.sheet_list if sheet.name == "其本设置"][0]
        print(set_sheet)
        rc_max_set_sheet = set_sheet.range(1, 1).expand().shape
        print(rc_max_set_sheet)
        set_sheet_list = set_sheet.range("A1:B" + str(rc_max_set_sheet[0])).value
        print(set_sheet_list)
        # 日期
        time_now = datetime.datetime.now()
        # print(time_now)
        now_date = (time_now + datetime.timedelta(hours=-16)).strftime("%Y%m%d")
        print(now_date)
        # now_date = str(time.strftime('%Y%m%d', time.localtime(time.time())))
        # 搜所有子小表, 分类处理表格
        for sheet in self.sheet_list:
            # e.g
            if sheet.name in ['女团饭拍','8K视频','女团专辑']:
                print(sheet.name)
                # 获取数据信息
                rc_max_sheet = sheet.range(1, 1).expand().shape
                sheet_list = sheet.range("A1:H" + str(rc_max_sheet[0])).value
                # print(sheet_list)
                # 获取开关信息
                open_info = sheet.range("K1:K20").value
                print(open_info)
                print(open_info[0])
                if open_info[0] == "开":
                    # 对有效列表进行下载
                    for i in range(1, len(sheet_list)):
                        print(sheet_list[i])
                        if sheet_list[i][7] == '是':
                            self.download(sheet_list[i], open_info)
                            # 处理完成写入结果日期
                            if open_info[3] =='否':
                                sheet.range('G' + str(i + 1)).value = now_date
                                # 保存excel
                                self.wb_info.save()
                                # 处理下载后的文件名称（重命名为有规）
                        else:
                            print("频道，非执行频道...")

                else:
                    print("未启动")

        print("更新执行完成，等待下一次，启动...")

    def download(self, fan_list, dir_info):
        # 差异化设置
        time_now = datetime.datetime.now()
        # print(time_now)
        now_date = (time_now + datetime.timedelta(hours=-16)).strftime("%Y%m%d")
        # now_date = str(time.strftime('%Y%m%d', time.localtime(time.time())))
        # 输出格式
        if dir_info[9] is None:
            out_format = 'bestvideo+bestaudio'
        else:
            out_format = dir_info[9]
            # print(out_format)
        # 合并格式
        merge_format = 'mkv'
        # 下载历史视频的设置
        if dir_info[3] == "是":
            tmp_his = 'old_' + dir_info[4] + "-" + dir_info[5]
        else:
            tmp_his = now_date
        # 另存为名字
        file_name = dir_info[2] + "\\" + tmp_his + "\\%(title)s_%(width)s_%(height)s_" + fan_list[
            0] + ".%(ext)s"
        # print(file_name)
        # 开始结束日期
        date_start = fan_list[6]
        date_end = now_date
        # if dir_info[3] == "是":
        #     date_start = dir_info[4]
        #     date_end = dir_info[5]
        # date_end = "20191123"
        num = int(date_end) - int(date_start)
        # print(num)
        list_date = [str(int(date_start) + i) for i in range(num)]
        # print(list_date)
        # 结束列表
        list_start = int(dir_info[6])
        list_end = int(dir_info[7])
        # 定义某些下载参数
        ydl_opts = {
            # 中间件参数
            'progress_hooks': [self.rename_hook],
            # 其他参数
            'writethumbnail': True,
            'playlistreverse': True,
            # 'listformats': True,
            'merge_output_format': merge_format,
            # 格式化下载后的文件名，避免默认文件名太长无法保存
            'outtmpl': file_name,
            'format': out_format,
            'proxy': 'http://127.0.0.1:1081/',
            'external_downloader': "aria2c",
            'external_downloader_args': ['--min-split-size', '1M', '--max-connection-per-server', '16'],
            'daterange': list_date,
            'playliststart': list_start,
            'playlistend': list_end
        }
        del ydl_opts['playlistreverse']

       # 下载历史视频的设置
        if dir_info[3] == "是":
            # del ydl_opts['playliststart']
            # del ydl_opts['playlistend']
            del ydl_opts['daterange']
            pass

        print(ydl_opts)
        if num <= 0 and dir_info[3] =="否":
            print("频道，当天的更新已完成")
            return

        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            # 下载给定的URL列表
            # print(ydl_opts["outtmpl"])
            # result = ydl.download([youtube_url])
            # print("start")
            num_lists = ["date", str(fan_list[6]).replace(".0", ""), dir_info[3], dir_info[4], dir_info[5]]
            # num_lists = "num"
            # print(num_lists)
            playlist_dict = ydl.extract_info(fan_list[2], download=True, num_list=num_lists)
            if num_lists[3]=='否':
                # print(playlist_dict)
                return


if __name__ == '__main__':
    # 地址
    # youtube-dl https://www.youtube.com/channel/UCStCNbOUMKtbL2sVoTJSt6w/videos
    # https://www.youtube.com/channel/UCv6colBP34LrC9xxf0lzQag/videos    # zam
    # url_into = 'https://www.youtube.com/channel/UCv6colBP34LrC9xxf0lzQag/videos'

    getItem = GetItem()
    # getItem.download(url_into)
    print("ok")
    # test
    getItem.deal_gather()
    # def job():
    #     print("I'm working...")
    # 工作标记
    # schedule.every(10).seconds.do(job)
    # 处理每日轮询扫描 update 更新
    # schedule.every().day.at("18:38").do(getItem.deal_gather)

    # while True:
    #     schedule.run_pending()
    #     time.sleep(2)
