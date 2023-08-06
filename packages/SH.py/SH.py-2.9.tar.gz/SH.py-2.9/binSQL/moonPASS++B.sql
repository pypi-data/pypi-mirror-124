CREATE USER 'user'@'localhost' IDENTIFIED WITH mysql_native_password BY 'yourpassword';
GRANT ALL PRIVILEGES ON *.* TO 'user'@'localhost' WITH GRANT OPTION;


SET GLOBAL validate_password.policy=LOW;
ALTER USER 'root'@'localhost' IDENTIFIED BY 'hello123' PASSWORD EXPIRE NEVER;
ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY 'hello123';
FLUSH PRIVILEGES;






mysql> ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY 'hello123';
Query OK, 0 rows affected (0.00 sec)
 
mysql> ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY 'hello123';
FLUSH PRIVILEGES;


use mysql;alter user 'root'@'localhost' identified with mysql_native_password by 'hello123';FLUSH PRIVILEGES;




#######################################################################################
## mysqld --default-authentication-plugin=mysql_native_password  ## 錯誤


mysqld --default-authentication-plugin=mysql_native_password --initialize

mysqld --default-authentication-plugin=mysql_native_password --initialize-insecure 

### 解決  https://learnku.com/articles/10736/some-craters-in-mysql-8011
遇到的坑
1、Authentication type：
用户的 Authentication type 默认为 caching_sha2_password，导致数据库连接错误，抛出如下异常：
Illuminate\Database\QueryException : SQLSTATE[HY000] [2054] The server requested authentication method unknown to the client
解决方案：修改密码认证方式
ALTER USER 'YOURUSERNAME'@'localhost' IDENTIFIED WITH mysql_native_password BY 'YOURPASSWORD';

2、删除了 NO_AUTO_CREATE_USER 模式
在 5.7.* 的日志中提到已废除该模式，在 8.0.11 中删除了，迁移时会抛出如下异常：
Illuminate\Database\QueryException : SQLSTATE[42000]: Syntax error or access violation: 1231 Variable 'sql_mode' can't be set to the value of 'NO_AUTO_CREATE_USER'

解决方案：将 config/database.php 配置文件中 mysql 的 strict 的值改为 false 即可！
目前就发现这两个，如有有其他的坑可以评论一下

————————————————
原文作者：Jinrenjie
转自链接：https://learnku.com/articles/10736/some-craters-in-mysql-8011
版权声明：著作权归作者所有。商业转载请联系作者获得授权，非商业转载请保留以上作者信息和原文链接。


