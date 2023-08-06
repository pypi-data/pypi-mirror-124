CREATE USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY 'hello123';
GRANT ALL PRIVILEGES ON *.* TO 'root'@'localhost' WITH GRANT OPTION;




use mysql;
SET GLOBAL validate_password.policy=LOW;
alter user 'root'@'localhost' identified with mysql_native_password by 'hello123';FLUSH PRIVILEGES;




CREATE USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY 'hello123';
GRANT ALL PRIVILEGES ON *.* TO 'root'@'localhost' WITH GRANT OPTION;





