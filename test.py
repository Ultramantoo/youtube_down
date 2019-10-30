from os import rename
import youtube_dl
import time


class GetItem(object):

    def rename_hook(self, d):
        # 重命名下载的视频名称的钩子
        if d['status'] == 'finished':
            print(d['filename'])
            file_name = r'H:\video\text2{}.mp4'.format(int(time.time()))
            rename(d['filename'], file_name)
            print('下载完成{}'.format(file_name))

    def download(self, youtube_url):
        # 定义某些下载参数

        ydl_opts = {
            'listformats': True,
            'merge_output_format': 'mp4',
            # 'progress_hooks': [self.rename_hook],
            # 格式化下载后的文件名，避免默认文件名太长无法保存
            'outtmpl': '001%(title)stext3-%(id)s.%(ext)s',
        }
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            # 下载给定的URL列表
            # print(ydl_opts["outtmpl"])
            result = ydl.download([youtube_url])
            print(result)


if __name__ == '__main__':
    getItem = GetItem()
    getItem.download('https://www.bilibili.com/video/av70638973')

# if __name__ == '__main__':
# download('https://www.bilibili.com/video/av70638973')

# ydl_opts = {
#     'format': 'bestvideo',
#     # 'outtmpl': os.path.join(app.config['VIDEOS_FOLDER'], '%(id)s.%(ext)s'),
#     # 'logger': MyLogger(),
#     'progress_hooks': [self.hook_progress],
# }
#
# ydl_opts = ({'outtmpl': '%(title)s%(ext)s',
#              'proxy': '127.0.0.1:1087'}) # 默认HTTP代理
