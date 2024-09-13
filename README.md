# fy4a_wallpaper 介绍
自动获取风云4a卫星云图作为壁纸(Windows)
解析风云官方XML接口，并保存图片，设置壁纸

# 需要安装的库
先安装 pip install requests

# 无界面运行
PowerShell下 pythonw fy4a_wallpaper.py

# 自用的BAT引导脚本
放在同目录下 命名start.bat
@echo off
@mode con cols=40 lines=11
cd C:\fy4a （你的目录）
python fy4a_wallpaper.py
