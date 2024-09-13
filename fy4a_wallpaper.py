# 解析风云4A卫星云图并作为壁纸（Windows）
# 先安装 pip install requests
# pythonw fy4a_wallpaper.py

import ctypes
import os
import time
import winreg
import requests
import xml.etree.ElementTree as ET

url = 'http://img.nsmc.org.cn/PORTAL/NSMC/XML/FY4A/FY4A_AGRI_IMG_REGI_MTCC_GLL.xml'
try:
    while True:
        response = requests.get(url)
        root = ET.fromstring(response.content)
        for child in root:
            response_pic = requests.get(child.attrib['url'])
            with open("0.jpg", "wb") as file:
                file.write(response_pic.content)
                file = os.path.dirname(__file__) + "\\" + "0.jpg"
                ctypes.windll.user32.SystemParametersInfoW(20, 0, file, 0)
                reg_key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Control Panel\Desktop", 0, winreg.KEY_WRITE)
                winreg.SetValueEx(reg_key, "WallpaperStyle", 0, winreg.REG_SZ, "2")
                winreg.SetValueEx(reg_key, "TileWallpaper", 0, winreg.REG_SZ, "0")
                winreg.CloseKey(reg_key)
                print("获取并设置壁纸成功", time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
                break
        time.sleep(1800)
except Exception as e:
    print(f"An error occurred: {e}")