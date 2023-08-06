
# 尋找
```
$ sudo find /* -name my.cnf
$ cd [檔案路徑]
$ sudo vim my.cnf
```

## 尋找 內文
```
$  find / -name *.cnf -exec grep -l -F "[mysqld]" {} \;

```

## 重新開機
```
$ sudo reboot
```