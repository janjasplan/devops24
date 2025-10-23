# Examination 7 - MariaDB installation

To make a dynamic web site, many use an SQL server to store the data for the web site.

[MariaDB](https://mariadb.org/) is an open-source relational SQL database that is good
to use for our purposes.

We can use a similar strategy as with the _nginx_ web server to install this
software onto the correct host(s). Create the playbook `07-mariadb.yml` with this content:

    ---
    - hosts: db
      become: true
      tasks:
        - name: Ensure MariaDB-server is installed.
          ansible.builtin.package:
            name: mariadb-server
            state: present

# QUESTION A

Make similar changes to this playbook that we did for the _nginx_ server, so that
the `mariadb` service starts automatically at boot, and is started when the playbook
is run.

**Answer**

See playbook

# QUESTION B

When you have run the playbook above successfully, how can you verify that the `mariadb`
service is started and is running?

**Answer**

I can connect to the db server and use the command `systemctl status mariadb` but its a lot easier to just run the command `ansible db -m ansible.builtin.shell -a "systemctl status mariadb"` from my host.

# BONUS QUESTION

How many different ways can use come up with to verify that the `mariadb` service is running?

**Answer**

Checks full service status: ansible db -m ansible.builtin.shell -a "systemctl status mariadb"
Check only the active state: ansible db -m ansible.builtin.shell -a "systemctl is-active mariadb"
Process check: ansible db -m ansible.builtin.shell -a "ps aux | grep [m]ariadb"