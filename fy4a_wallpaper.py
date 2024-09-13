# 解析风云4A卫星云图并作为壁纸（Windows）
# 先安装 pip install requests
# pythonw fy4a_wallpaper.py

import ctypes
import os
import time
import winreg
from time import sleep
import requests

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
            with open("0.jpg", "wb") as file:
                file.write(wall_pic.content)
                file = os.path.dirname(__file__) + "\\" + "0.jpg"
            ctypes.windll.user32.SystemParametersInfoW(20, 0, file, 0)
            reg_key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Control Panel\Desktop", 0, winreg.KEY_WRITE)
            winreg.SetValueEx(reg_key, "WallpaperStyle", 0, winreg.REG_SZ, "2")
            winreg.SetValueEx(reg_key, "TileWallpaper", 0, winreg.REG_SZ, "0")
            winreg.CloseKey(reg_key)
            print("获取并设置壁纸成功", time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
            sleep(1800)

        else:
            sleep(60)

except Exception as e:
    print(f"An error occurred: {e}")
