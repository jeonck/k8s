# 권한 부여 예시 
```bash
CREATE USER 'root'@'10.%' IDENTIFIED BY 'your_password';   
 
GRANT ALL PRIVILEGES ON *.* TO 'root'@'10.%';   
 
SELECT User, Host FROM mysql.user; 
```


# 계정 생성과 권한 부여 예시
```bash
-- sample 계정 생성  
CREATE USER 'sample'@'%' IDENTIFIED BY 'sample123!@#';  
  
-- sample 계정에 표준적인 권한 부여  
GRANT SELECT, INSERT, UPDATE, DELETE, CREATE, DROP, RELOAD, PROCESS, REFERENCES, INDEX, ALTER, SHOW DATABASES, CREATE TEMPORARY TABLES, LOCK TABLES, EXECUTE, REPLICATION SLAVE, REPLICATION CLIENT, CREATE VIEW, SHOW VIEW, CREATE ROUTINE, ALTER ROUTINE, EVENT, TRIGGER, CREATE ROLE, DROP ROLE ON *.* TO 'sample'@'%';  
  
-- CREATE USER 권한 철회  
REVOKE CREATE USER ON *.* FROM 'sample'@'%';  
  
-- 변경 사항 적용  
FLUSH PRIVILEGES;  
  
-- 권한 확인  
SHOW GRANTS FOR 'sample'@'%';  
```

# 테이블 생성
```bash
mysql> CREATE DATABASE sample_table DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci;
Query OK, 1 row affected (0.04 sec)
```
