# Examination 8 - MariaDB configuration

MariaDB and MySQL have the same origin (MariaDB is a fork of MySQL, because of... Oracle...
it's a long story.) They both work the same way, which makes it possible to use Ansible
collections that handle `mysql` to work with `mariadb`.

To be able to manage MariaDB/MySQL through the `community.mysql` collection, you also
need to make sure the requirements for the collections are installed on the database VM.

See https://docs.ansible.com/ansible/latest/collections/community/mysql/mysql_db_module.html#ansible-collections-community-mysql-mysql-db-module-requirements

HINT: In AlmaLinux, the correct package to install on the VM host is called `python3-PyMySQL`.

# QUESTION A

Copy the playbook from examination 7 to `08-mariadb-config.yml`.

Use the `community.mysql` module in this playbook so that it also creates a database instance
called `webappdb` and a database user called `webappuser`.

Make the `webappuser` have the password "secretpassword" to access the database.

HINT: The `community.mysql` collection modules has many different ways to authenticate
users to the MariaDB/MySQL instance. Since we've just installed `mariadb` without setting
any root password, or securing the server in other ways, we can use the UNIX socket
to authenticate as root:

* The socket is located in `/var/lib/mysql/mysql.sock`
* Since we're authenticating through a socket, we should ignore the requirement for a `~/.my.cnf` file.
* For simplicity's sake, let's grant `ALL` privileges on `webapp.*` to `webappuser`

# Documentation and Examples
https://docs.ansible.com/ansible/latest/collections/community/mysql/index.html


**Answer**
First, I add a task that ensures that the Python package is installed. I then proceed with creating my database and a database user. With the `password` argument, I give the user a password. The `priv` argument is used to set the privileges that the user has in my database. `webappdb.*:ALL` makes sure that the user has all privileges to all tables inside the webappdb database. Since I don’t want to use a password to log in as root, I instead use the `login_unix_socket:` argument. I point to the file `/var/lib/mysql/mysql.sock`, where the MySQL server’s socket is located, allowing Ansible to connect as the root user without using a password.


**Command and output that shows the created user**
```bash
[deploy@dbserver ~]$ sudo mysql -S /var/lib/mysql/mysql.sock -e "SELECT Host, User FROM mysql.user;"
+-----------+-------------+
| Host      | User        |
+-----------+-------------+
| localhost | mariadb.sys |
| localhost | mysql       |
| localhost | root        |
| localhost | webappuser  |
+-----------+-------------+
```

**Command and output that shows our created database**
```bash
[deploy@dbserver ~]$ sudo mysql -S /var/lib/mysql/mysql.sock -e "SHOW DATABASES;"
+--------------------+
| Database           |
+--------------------+
| information_schema |
| mysql              |
| performance_schema |
| sys                |
| webappdb           |
+--------------------+

```
**Command and output that shows grants for our user**
```bash
[deploy@dbserver ~]$ sudo mysql -S /var/lib/mysql/mysql.sock -e "SHOW GRANTS FOR 'webappuser'@'localhost';"
+-------------------------------------------------------------------------------------------------------------------+
| Grants for webappuser@localhost                                                                                   |
+-------------------------------------------------------------------------------------------------------------------+
| GRANT USAGE ON *.* TO `webappuser`@`localhost` IDENTIFIED BY PASSWORD '*F89FFE84BFC48A876BC682C4C23ABA4BF64711A4' |
| GRANT ALL PRIVILEGES ON `webappdb`.* TO `webappuser`@`localhost`                                                  |
+-------------------------------------------------------------------------------------------------------------------+
```