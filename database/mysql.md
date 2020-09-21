

# Remote permission issue
docker exec -it mysqltest bash
mysql -uroot -ppassword
CREATE USER 'root'@'%' IDENTIFIED BY 'password';
grant all on *.* to 'root'@'%';
SELECT host, user FROM mysql.user;

ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY 'password';
ALTER USER 'root'@'%' IDENTIFIED WITH mysql_native_password BY 'password';


# Some other docker-compose file
#MySQL Service
  mysql:
    image: mysql:8
    container_name: mysql
    restart: unless-stopped
    tty: true
    ports:
      - "3306:3306"
    environment:
      MYSQL_DATABASE: database
      MYSQL_ROOT_PASSWORD: root
      SERVICE_TAGS: dev
      SERVICE_NAME: mysql
    volumes:
      - ./mysql/dbdata:/var/lib/mysql/
      - ./mysql/my.cnf:/etc/mysql/my.cnf
    networks:
      - app-network

and my.cnf file

[mysqld]
general_log = 1
general_log_file = /var/lib/mysql/general.log
secure-file-priv= NULL
#Accept connections from any IP address
bind-address = 0.0.0.0

-- https://github.com/docker-library/mysql/issues/275


```bash
# Use root/example as user/password credentials
version: '3.1'

services:

  db:
    image: mysql
    command: --default-authentication-plugin=mysql_native_password
    restart: always
    environment:
      MYSQL_ROOT_PASSWORD: password
    ports:
      - 3306:3306
    volumes:
      - /Users/pankaj.singh/my-projects/Code/database/storage/mysql-data:/var/lib/mysql

  adminer:
    image: adminer
    restart: always
    ports:
      - 8090:8080
```

mysql -uroot -ppassword -h127.0.0.1 -P3306 -e 'show global variables like "max_connections"';


## Reference
https://hub.docker.com/_/mysql