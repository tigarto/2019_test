

### Setting Up a MySQL Database ###

```bash
# Terminal bash
mysql -u root -p
```


```bash
# Terminal mysql
CREATE USER 'dsuser'@'localhost' IDENTIFIED BY 'badpassw0rd';
CREATE DATABASE dsdb;
GRANT ALL ON dsdb.* TO 'dsuser'@'localhost';
```

Nos salimos y accedemos como el otro usuario:


```bash
mysql -u dsuser -p dsdb
```

```bash
USE dsdb;
CREATE TABLE employee (empname TINYTEXT, salary FLOAT, hired DATE);

SHOW tables;

DROP TABLE employee;
```
```bash
CREATE TABLE employee (id INT PRIMARY KEY AUTO_INCREMENT,
updated TIMESTAMP, empname TINYTEXT NOT NULL, salary FLOAT NOT NULL,hired DATE);

SHOW tables;

DESCRIBE employee;
#
#DESCRIBE employee;
#+---------+-----------+------+-----+-------------------+-----------------------------+
#| Field   | Type      | Null | Key | Default           | Extra                       |
#+---------+-----------+------+-----+-------------------+-----------------------------+
#| id      | int(11)   | NO   | PRI | NULL              | auto_increment              |
#| updated | timestamp | NO   |     | CURRENT_TIMESTAMP | on update CURRENT_TIMESTAMP |
#| empname | tinytext  | NO   |     | NULL              |                             |
#| salary  | float     | NO   |     | NULL              |                             |
#| hired   | date      | YES  |     | NULL              |                             |
#+---------+-----------+------+-----+-------------------+-----------------------------+
#5 rows in set (0,01 sec)


ALTER TABLE employee ADD INDEX(hired); # if you want to use a column (variable) for 
                                       # sorting, searching, or joining, add an index 
                                       # to that column, too:

DESCRIBE employee;

#DESCRIBE employee;
#+---------+-----------+------+-----+-------------------+-----------------------------+
#| Field   | Type      | Null | Key | Default           | Extra                       |
#+---------+-----------+------+-----+-------------------+-----------------------------+
#| id      | int(11)   | NO   | PRI | NULL              | auto_increment              |
#| updated | timestamp | NO   |     | CURRENT_TIMESTAMP | on update CURRENT_TIMESTAMP |
#| empname | tinytext  | NO   |     | NULL              |                             |
#| salary  | float     | NO   |     | NULL              |                             |
#| hired   | date      | YES  | MUL | NULL              |                             |
#+---------+-----------+------+-----+-------------------+-----------------------------+
#5 rows in set (0,00 sec)


DROP INDEX hired ON employee;


ALTER TABLE employee ADD UNIQUE(empname(255));
```

###  Using a MySQL Database: Command Line ### 

#### Insertion ####

```sql
INSERT INTO [table] ([column], [column]) VALUES ('[value]', [value]');
```

```bash
INSERT INTO employee VALUES(NULL,NULL,"John Smith",35000,NOW());

SHOW WARNINGS;

SELECT * FROM employee;

INSERT INTO employee VALUES(NULL,NULL,"John Smith",35000,NOW());

INSERT IGNORE INTO employee VALUES(NULL,NULL,"John Smith",35000,NOW());

```

#### Deletion ####

```sql
DELETE FROM [table] WHERE [column] = [value];
DELETE FROM [table];
```

Es irreversible

```bash
# Remove John Smith if he is low-paid
DELETE FROM employee WHERE salary<11000 AND empname="John Smith";
SELECT * FROM employee;


# Remove everyone
DELETE FROM employee;
```

#### Mutation #### 

```sql
UPDATE [table] SET [column] = '[updated-value]' WHERE [column] = [value];
```

```bash
# Se agrego por que se borro antes
INSERT INTO employee VALUES(NULL,NULL,"John Smith",35000,NOW());
#Reset all recent hires' salary
UPDATE employee SET salary=35000 WHERE hired=CURDATE();
# Increase John Smith's salary again
UPDATE employee SET salary=salary+1000 WHERE empname="John Smith";
```

#### Selection ####

```bash
INSERT INTO employee VALUES(NULL,NULL,"Anon I. Muss",14000,'2000-01-01');


INSERT INTO employee VALUES(NULL,NULL,"Jane Doe",75000,'2011-11-11');

INSERT INTO employee VALUES(NULL,NULL,"Abe Lincoln",0.01,'1990-01-01');
```

```bash
SELECT empname,salary FROM employee WHERE empname="John Smith";

SELECT * FROM employee;


SELECT * FROM employee WHERE empname="John Smith";

SELECT * FROM employee WHERE hired>='2000-01-01' ORDER BY salary DESC;

# mysql> SELECT * FROM employee WHERE hired>='2000-01-01' ORDER BY salary DESC;
# +----+---------------------+--------------+--------+------------+
# | id | updated             | empname      | salary | hired      |
# +----+---------------------+--------------+--------+------------+
# |  6 | 2019-02-24 14:44:52 | Jane Doe     |  75000 | 2011-11-11 |
# |  4 | 2019-02-24 14:35:07 | John Smith   |  36000 | 2019-02-24 |
# |  5 | 2019-02-24 14:44:45 | Anon I. Muss |  14000 | 2000-01-01 |
# +----+---------------------+--------------+--------+------------+
# 3 rows in set (0,00 sec)





```

To group and aggregate the results, use the GROUP BY modifier and an aggregation function, such as COUNT(), MIN(), MAX(), SUM(), or AVG():

```bash
SELECT (hired>'2001-01-01') AS Recent,AVG(salary)
  FROM employee
  GROUP BY (hired>'2001-01-01');

# mysql> SELECT (hired>'2001-01-01') AS Recent,AVG(salary)
#     ->   FROM employee
#     ->   GROUP BY (hired>'2001-01-01');
# +--------+-------------------+
# | Recent | AVG(salary)       |
# +--------+-------------------+
# |      0 | 7000.004999999888 |
# |      1 |             55500 |
# +--------+-------------------+

SELECT AVG(salary),MIN(hired),MAX(hired) FROM employee
GROUP BY YEAR(hired);

# +----------------------+------------+------------+
# | AVG(salary)          | MIN(hired) | MAX(hired) |
# +----------------------+------------+------------+
# | 0.009999999776482582 | 1990-01-01 | 1990-01-01 |
# |                14000 | 2000-01-01 | 2000-01-01 |
# |                75000 | 2011-11-11 | 2011-11-11 |
# |                36000 | 2019-02-24 | 2019-02-24 |
# +----------------------+------------+------------+
# 4 rows in set (0,00 sec)

```

#### Join ####

```bash
# Prepare and populate another table
CREATE TABLE position (eid INT, description TEXT);

INSERT INTO position (eid,description) VALUES (6,'Imposter'),
(1,'Accountant'),(4,'Programmer'),(5,'President');

SELECT * FROM position;

# mysql> SELECT * FROM position;
# +------+-------------+
# | eid  | description |
# +------+-------------+
# |    6 | Imposter    |
# |    1 | Accountant  |
# |    4 | Programmer  |
# |    5 | President   |
# +------+-------------+
# 4 rows in set (0,00 sec)


ALTER TABLE position ADD INDEX(eid);

SELECT * FROM position;

# mysql> SELECT * FROM position;
# +------+-------------+
# | eid  | description |
# +------+-------------+
# |    6 | Imposter    |
# |    1 | Accountant  |
# |    4 | Programmer  |
# |    5 | President   |
# +------+-------------+
# 4 rows in set (0,00 sec)


# Fetch the joined data
SELECT employee.empname,position.description
FROM employee,position WHERE employee.id=position.eid
ORDER BY position.description;

# mysql> SELECT employee.empname,position.description
#     -> FROM employee,position WHERE employee.id=position.eid
#     -> ORDER BY position.description;
# +--------------+-------------+
# | empname      | description |
# +--------------+-------------+
# | Jane Doe     | Imposter    |
# | Anon I. Muss | President   |
# | John Smith   | Programmer  |
# +--------------+-------------+
# 3 rows in set (0,00 sec)

```
http://www.mysqltutorial.org/mysql-cheat-sheet.aspx
https://gist.github.com/hofmannsven/9164408

https://github.com/abulanov/sfc_app/blob/master/sfc_app.py