use mysql;
ALTER USER 'root'@'localhost' IDENTIFIED BY 'hello123' PASSWORD EXPIRE NEVER;
ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY 'hello123';
FLUSH PRIVILEGES;









