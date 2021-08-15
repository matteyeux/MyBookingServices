# Booking API

This is the directory containing the code for the Booking API.

### API folder structure
```
.
├── booking
│   ├── app.py
│   ├── config.py
│   ├── database.py
│   ├── __init__.py
│   ├── main.py
│   ├── models
│   │   ├── book.py
│   │   ├── __init__.py
│   │   └── rooms.py
│   └── routers
│       ├── book.py
│       ├── __init__.py
│       └── rooms.py
├── poetry.lock
├── pyproject.toml
├── README.md
└── tests
    ├── test_app.py
    ├── test_book.py
    ├── test_config.py
    └── test_rooms.py
```

## Setup dev environment

How to setup a basic env for the booking API

### booking API

Install `poetry` and `virtualenv`.

Use `poetry` to instal dependencies (`poetry install`). You should be ready to work.

### MySQL

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

### Tests

Tests are run by Github Actions but you can run them localy :
```
λ pytest -sv  --cov-report term-missing --cov=booking

tests/test_app.py::test_read_root PASSED

----------- coverage: platform linux, python 3.9.5-final-0 -----------
Name                       Stmts   Miss  Cover   Missing
--------------------------------------------------------
booking/__init__.py            0      0   100%
booking/app.py                 8      0   100%
booking/book.py                4      4     0%   1-7
booking/main.py               17     17     0%   2-60
booking/routers/users.py      11      3    73%   9, 14, 19
--------------------------------------------------------
TOTAL                         40     24    40%
```
