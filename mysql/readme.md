# into 
docker exec -it mc_mysql mysql -uroot -p
##  create struct
-- init.sql
-- 创建数据库
CREATE DATABASE IF NOT EXISTS Mydata; 

-- 创建用户
CREATE USER 'mc'@'%' IDENTIFIED BY '';

-- 授权
GRANT ALL PRIVILEGES ON Mydata.* TO 'mc'@'%';
GRANT SELECT ON Mydata.* TO 'mc'@'%';
FLUSH PRIVILEGES;

-- 切换到新数据库
USE Mydata;

-- 建表
 CREATE TABLE wardrobe (     
    id INT NOT NULL AUTO_INCREMENT,                
    timestamp DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,      
    type VARCHAR(50) NOT NULL,                     
    temperature DECIMAL(5,2),                      
    price DECIMAL(10,2),                           
    PRIMARY KEY (id) 
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;