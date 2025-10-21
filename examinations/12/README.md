# Examination 12 - Roles

So far we have been using separate playbooks and ran them whenever we wanted to make
a specific change.

With Ansible [roles](https://docs.ansible.com/ansible/latest/playbook_guide/playbooks_reuse_roles.html) we
have the capability to organize tasks into sets, which are called roles.

These roles can then be used in a single playbook to perform the right tasks on each host.

Consider a playbook that looks like this:

    ---
    - name: Configure the web server(s) according to specs
      hosts: web
      roles:
        - webserver

    - name: Configure the database server(s) according to specs
      hosts: db
      roles:
        - dbserver

This playbook has two _plays_, each play utilizing a _role_.

This playbook is also included in this directory as [site.yml](site.yml).

Study the Ansible documentation about roles, and then start work on [QUESTION A](#question-a).

# QUESTION A

Considering the playbook above, create a role structure in your Ansible working directory
that implements the previous examinations as two separate roles; one for `webserver`
and one for `dbserver`.

Copy the `site.yml` playbook to be called `12-roles.yml`.

HINT: You can use

    $ ansible-galaxy role init [name]

to create a skeleton for a role. You won't need ALL the directories created by this,
but it gives you a starting point to fill out in case you don't want to start from scratch.



**Answer**
Under the directory roles, I have created two roles using `ansible-galaxy role init`.
Since some software is shared between both roles, I also created a separate `base` role that contains the common installation tasks.

Because the roles I call in my main playbook are themselves executed as task sets, I needed to remove the top-level `tasks:` key from all included playbooks. Similarly, the `enabled: true` configuration is only required in my main playbook, so I removed it from the individual playbooks within each role.

Each role has its own playbooks placed under the tasks directory, alongside the `main.yml` file. Inside `main.yml`, I use the `include_tasks:` directive to reference all the task files that should be executed for that specific role.

Finally, I also include the variable files that contain encrypted data, so that sensitive information can be accessed securely within the roles. I did this by using the `ansible.builtin.include_vars:` module.
