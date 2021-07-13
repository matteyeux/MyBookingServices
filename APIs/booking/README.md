# Booking API

This is the directory containing the code for the Booking API.


### Setup dev environment

This is a

##### booking API

Install `poetry` and `virtualenv`.

Use `poetry` to instal dependencies (`poetry install`). You should be ready to work.

##### MySQL

Setup MySQL container : `docker run --name mysql -p 3306:3306 -e MYSQL_ROOT_PASSWORD=root -d mysql`.

Test connection :
```
λ ~ » mysql --host=127.0.0.1 -P 3306 -u root -p
Enter password:
Welcome to the MySQL monitor.  Commands end with ; or \g.
Your MySQL connection id is 8
Server version: 8.0.25 MySQL Community Server - GPL

Copyright (c) 2000, 2021, Oracle and/or its affiliates.

Oracle is a registered trademark of Oracle Corporation and/or its
affiliates. Other names may be trademarks of their respective
owners.

Type 'help;' or '\h' for help. Type '\c' to clear the current input statement.

mysql>
```
