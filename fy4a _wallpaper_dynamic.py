# 动态卫星云图壁纸，此文件尚未开发完，仅供测试思路之用

# 解析风云4A卫星云图并作为壁纸（Windows）
# 先安装 pip install requests
# pythonw fy4a_wallpaper.py

import ctypes
import os
import threading
import time
import winreg
from time import sleep
import requests
import shutil
import re

# live_wallpaper = False #是否开启动态壁纸
# live_shift_time = 0.1 #
# pic_source = 0 #数据源(0为NMC，1为.......)

def set_pic():
    sign_num = 7
    while True:
        try:
            target_filenames = ['0.jpg','1.jpg', '2.jpg', '3.jpg', '4.jpg', '5.jpg', '6.jpg', '7.jpg']
            # 检查目标文件是否存在
            missing_files = [filename for filename in target_filenames if not os.path.exists(filename)]
            if not missing_files:
                file = os.path.dirname(__file__) + "\\" + str(sign_num) + ".jpg"
                ctypes.windll.user32.SystemParametersInfoW(20, 0, file, 0)
                reg_key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Control Panel\Desktop", 0, winreg.KEY_WRITE)
                winreg.SetValueEx(reg_key, "WallpaperStyle", 0, winreg.REG_SZ, "2")
                winreg.SetValueEx(reg_key, "TileWallpaper", 0, winreg.REG_SZ, "0")
                winreg.CloseKey(reg_key)
                # print("设置壁纸成功", time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
                sleep(0.5)
                sign_num = sign_num-1
                if sign_num == -1:
                    sign_num =7

        except Exception as e:
            print(f"An error occurred: {e}")


def net_get_pic():
    try:
        while True:
            resp = requests.get(
                'http://www.nmc.cn/rest/relevant/f36308b0aee44e64b81007a2e0c482c6?_=' + str(time.time())[:14].replace(".",
                                                                                                                      ""))
            wall_pic = ""
            for item in resp.json():
                if item['title'] == 'FY-4B':
                    r = requests.get("http://www.nmc.cn" + item['image'].replace("/medium", ""))
                    wall_pic = r

            if wall_pic != "":
                move_and_copy_pic()
                with open("0.jpg", "wb") as file:
                    file.write(wall_pic.content)
                copy0jpg()
                print("获取壁纸成功", time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
                sleep(1000)

            else:
                sleep(60)

    except Exception as e:
        print(f"An error occurred: {e}")


def copy0jpg():
    # 定义源文件名和目标文件名列表
    source_filename = '0.jpg'
    target_filenames = ['1.jpg', '2.jpg', '3.jpg', '4.jpg', '5.jpg', '6.jpg', '7.jpg']

    # 检查目标文件是否存在
    missing_files = [filename for filename in target_filenames if not os.path.exists(filename)]

    # 如果存在缺失的文件，则复制源文件
    if missing_files:
        for missing_file in missing_files:
            shutil.copy(source_filename, missing_file)

def move_and_copy_pic():
    # 获取当前目录下的所有.jpg文件
    files = [f for f in os.listdir('.') if f.endswith('.jpg') and re.match(r'^\d+\.jpg$', f)]

    # 根据文件名中的数字进行排序
    files.sort(key=lambda x: int(re.match(r'^\d+', x).group()), reverse=True)

    # 删除最后一个jgp
    if len(files) > 0:
        original_last_file = f"{len(files) - 1}.jpg"
        if os.path.exists(original_last_file):
            os.remove(original_last_file)
            print(f"删除文件 {original_last_file}")

    # 获取当前目录下的所有.jpg文件
    files = [f for f in os.listdir('.') if f.endswith('.jpg') and re.match(r'^\d+\.jpg$', f)]

    # 根据文件名中的数字进行排序
    files.sort(key=lambda x: int(re.match(r'^\d+', x).group()), reverse=True)

    # 批量移动原0-7jpg
    for filename in files:
        number = int(re.match(r'^\d+', filename).group())
        new_filename = f'{number + 1}.jpg'

        os.rename(filename, new_filename)
        print(f"重命名 {filename} 为 {new_filename}")



if __name__ == "__main__":
    # 创建线程
    thread_1 = threading.Thread(target=net_get_pic)
    thread_2 = threading.Thread(target=set_pic)

    # 启动线程
    thread_1.start()
    thread_2.start()

    # 等待所有线程完成
    thread_1.join()
    thread_2.join()
