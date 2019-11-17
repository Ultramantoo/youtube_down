from os import rename
import youtube_dl
import time


class GetItem(object):

    def rename_hook(self, d):
        # 重命名下载的视频名称的钩子
        print(d['status'])
        if d['status'] == 'finished':
            print(d['filename'])
            # file_name = r'D:\text2{}.mp4'.format(int(time.time()))
            # rename(d['filename'], file_name)
            print('下载完成')
        elif d['status'] =="downloading":
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
        date_start = "20191117"
        date_end = str(time.strftime('%Y%m%d', time.localtime(time.time())))
        # 结束列表
        list_end = 10
        # 定义某些下载参数
        ydl_opts = {
            # 中间件参数
            'progress_hooks': [self.rename_hook],
            # 其他参数
            'writethumbnail': True,
            # 'listformats': True,
            'merge_output_format': merge_format,
            # 格式化下载后的文件名，避免默认文件名太长无法保存
            'outtmpl': file_name,
            'format': out_format,
            'proxy': 'http://127.0.0.1:1081/',
            'external_downloader': "aria2c",
            'external_downloader_args': ['--min-split-size', '1M', '--max-connection-per-server', '16'],
            'daterange': [date_start, date_end],
            'playliststart': 1,
            'playlistend': list_end

        }
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            # 下载给定的URL列表
            # print(ydl_opts["outtmpl"])
            result = ydl.download([youtube_url])
            # info_dict = ydl.extract_info([youtube_url][0], download=False)
            # # print(info_dict)
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
    url_into = 'https://www.youtube.com/playlist?list=PLmuH45fzaKzaB2O0xE4JJGCj_AaFSBE0G'

    getItem = GetItem()
    getItem.download(url_into)
