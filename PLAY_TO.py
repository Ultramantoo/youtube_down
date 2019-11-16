from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
from moviepy.editor import VideoFileClip
import os
import time
import psutil


def clean_ffmpeg():
    # 旧EXCEL
    try:
        pids = psutil.pids()
        for pid in pids:
            p = psutil.Process(pid)
            # print('pid-%s,pname-%s' % (pid, p.name()))
            if p.name() == 'ffmpeg-win32-v4.1.exe':
                cmd = 'taskkill /F /IM ffmpeg-win32-v4.1.exe'
                os.system(cmd)
    except:
        pass


def cut_movie(file_dir):
    for root, dirs, files in os.walk(file_dir):
        # print(root)  # 当前目录路径
        # print(dirs)  # 当前路径下所有子目录
        # print(files)  # 当前路径下所有非目录子文件
        if len(files) >= 1 and "out_to" not in dirs:
            # print(len(files))
            print("发现需处理的文件")
            for file_info in files:
                # print(file_info[-3:])
                if file_info[-3:] == "mp4":
                    # 新建输出文件夹
                    if not os.path.exists(root + "\\out_to\\"):
                        os.makedirs(root + "\\out_to\\")
                    # print(file_info)
                    # 获取视频时间
                    file_dirs = root + "\\" + file_info
                    # print(file_dirs)
                    clip = VideoFileClip(file_dirs)
                    # print(clip.end)
                    # 分割
                    print(root + "\\out_to\\" + file_info)
                    ffmpeg_extract_subclip(file_dirs, 3.4, clip.end - 9.8,
                                           targetname=root + "\\out_to\\" + file_info.replace(" ", "").replace("000",""))
                    time.sleep(1.5)
                    clean_ffmpeg()


file_dirs = r"D:\运动教程"
cut_movie(file_dirs)

# clip = VideoFileClip(r"D:\运动教程\游泳教程\1、入门_学游泳_认识科普（高清精选）\22螺旋式游泳姿势.mp4")
# print(clip.end)
#
#
# ffmpeg_extract_subclip("00001-羽毛球：认识羽毛球拍 _ Badminton_1920_1080.mp4", 3.4, clip.end-9.8, targetname="test.mp4")
