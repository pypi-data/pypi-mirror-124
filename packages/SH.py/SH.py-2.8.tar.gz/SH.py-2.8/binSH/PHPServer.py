import os
os.chdir('/root')
#########
print('安裝中,請稍等候 ..') 
print('正在從.../www/EXE/SH/ 下載所需檔案!!') 
os.system('wget -qq https://drv.tw/~login0516@gmail.com/gd/www/EXE/SH/server.py       >> log.txt')
print('安裝 Nginx')
os.system('chmod +x server.py')
os.system('./server.py        >> log.txt')
############################################
os.system('wget -qq https://drv.tw/~login0516@gmail.com/gd/www/EXE/SH/MySQL.sh        >> log.txt')
os.system('wget -qq https://drv.tw/~login0516@gmail.com/gd/www/EXE/SH/MysqlAdmin.sh   >> log.txt')
print('安裝 MySQL')
os.system('chmod +x MySQL.sh')
print('安裝 MysqlAdmin')
########## 連接 目錄 ## 目錄權限沒改 ### 失敗
# os.system('ln -s /content/sample_drive/Colab_SQL/admin  /usr/share/nginx/html/admin')
######################
os.system('chmod +x MysqlAdmin.sh')
os.system('./MysqlAdmin.sh    >> log.txt')
print('安裝完成 .')  ### 可刪除 下載的