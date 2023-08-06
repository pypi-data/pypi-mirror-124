#!/usr/bin/expect -f
#coding:utf-8

# set NameQQ [lindex $argv 0 ]   # 接收第1個引數,作為 NameQQ  ### 失敗
# set PassAA [ lindex $argv 1 ]     # 接收第1個引數,作為 AA
# set PassBB [ lindex $argv 2 ]     # 接收第2個引數,作為 BB

set timeout 10                   
# 設定超時時間
 
# 向遠端伺服器請求開啟一個FTP會話，並等待伺服器詢問使用者名稱
spawn mysql_secure_installation
    # expect "$NameQQ\r"
    send "y\r"

    send "0\r"

    expect "輸入密碼\r"
    send "hello123\r"

    expect "載入輸入密碼\r"
    send "hello123\r"

    send "y\r"

    send "y\r"

    send "y\r"

    send "y\r"

    send "y\r"
    
    expect eof