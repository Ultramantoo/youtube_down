# from os import rename
import youtube_dl
import time
import schedule

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
        pass
        # 打开表格
        # 提取数据

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

    def download(self, youtube_url):
        # 差异化设置
        # 输出格式
        out_format = 'bestvideo+bestaudio'
        # 合并格式
        merge_format = 'mkv'
        # 另存为名字
        file_name = r'D:\%(title)s_%(width)s_%(height)s.%(ext)s'
        # 开始结束日期
        date_start = "20191201"
        date_end = str(time.strftime('%Y%m%d', time.localtime(time.time())))
        # date_end = "20191123"
        num = int(date_end) - int(date_start)
        # print(num)
        list_date = [str(int(date_start) + i) for i in range(num + 1)]
        # print(list_date)
        # 结束列表
        list_end = 10
        # 定义某些下载参数
        ydl_opts = {
            # 中间件参数
            'progress_hooks': [self.rename_hook],
            # 其他参数
            'writethumbnail': True,
            # 'playlistreverse': True,
            # 'listformats': True,
            'merge_output_format': merge_format,
            # 格式化下载后的文件名，避免默认文件名太长无法保存
            'outtmpl': file_name,
            'format': out_format,
            'proxy': 'http://127.0.0.1:1081/',
            'external_downloader': "aria2c",
            'external_downloader_args': ['--min-split-size', '1M', '--max-connection-per-server', '16'],
            'daterange': list_date,
            'playliststart': 1,
            'playlistend': list_end

        }
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            # 下载给定的URL列表
            # print(ydl_opts["outtmpl"])
            # result = ydl.download([youtube_url])
            # print("start")
            num_lists = ["date", "20191202"]
            # num_lists = "num"
            playlist_dict = ydl.extract_info([youtube_url][0], download=True, num_list=num_lists)
            if num_lists:
                # print(playlist_dict)
                return
            for video in playlist_dict['entries']:
                print(len(playlist_dict['entries']))
                print("test")
                if not video:
                    print('ERROR: Unable to get info. Continuing...')
                    continue
                for tmp in ['thumbnail', 'id', 'title', 'description', 'duration']:
                    print(tmp, '--', video.get(tmp))
            # print(info_dict)
            # video_url = info_dict.get("webpage_url", None)
            # print(video_url)
            # video_title = info_dict.get('title', None)
            # print(video_title)
        # from youtube_dl import YoutubeDL
        # video = "http://www.youtube.com/watch?v=BaW_jenozKc"
        # with YoutubeDL(youtube_dl_opts) as ydl:
        #       info_dict = ydl.extract_info(video, download=False)
        #       video_url = info_dict.get("url", None)
        #       video_id = info_dict.get("id", None)
        #       video_title = info_dict.get('title', None)


if __name__ == '__main__':
    # 地址
    # youtube-dl https://www.youtube.com/channel/UCStCNbOUMKtbL2sVoTJSt6w/videos
    # https://www.youtube.com/channel/UCv6colBP34LrC9xxf0lzQag/videos    # zam
    url_into = 'https://www.youtube.com/channel/UCv6colBP34LrC9xxf0lzQag/videos'

    getItem = GetItem()
    # getItem.download(url_into)
    print("ok")


    def job():
        print("I'm working...")


    # 工作标记
    schedule.every(10).seconds.do(job)
    # 处理每日轮询扫描 update 更新
    schedule.every().day.at("01:09").do(getItem.download, url_into)

    while True:
        schedule.run_pending()
        time.sleep(2)
