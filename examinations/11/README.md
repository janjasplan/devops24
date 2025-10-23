# Examination 11 - Loops

Imagine that on the web server(s), the IT department wants a number of users accounts set up:

    alovelace
    aturing
    edijkstra
    ghopper

These requirements are also requests:

* `alovelace` and `ghopper` should be added to the `wheel` group.
* `aturing` should be added to the `tape` group
* `edijkstra` should be added to the `tcpdump` group.
* `alovelace` should be added to the `audio` and `video` groups.
* `ghopper` should be in the `audio` group, but not in the `video` group.

Also, the IT department, for some unknown reason, wants to copy a number of '\*.md' files
to the 'deploy' user's home directory on the `db` machine(s).

I recommend you use two different playbooks for these two tasks. Prefix them both with `11-` to
make it easy to see which examination it belongs to.

# QUESTION A

Write a playbook that uses loops to add these users, and adds them to their respective groups.

When your playbook is run, one should be able to do this on the webserver:

    [deploy@webserver ~]$ groups alovelace
    alovelace : alovelace wheel video audio
    [deploy@webserver ~]$ groups aturing
    aturing : aturing tape
    [deploy@webserver ~]$ groups edijkstra
    edijkstra : edijkstra tcpdump
    [deploy@webserver ~]$ groups ghopper
    ghopper : ghopper wheel audio

There are multiple ways to accomplish this, but keep in mind _idempotency_ and _maintainability_.

**Answer**

First, I create a YAML file that contains the users and their associated groups. The `users:` key defines each user with a name and the list of groups they should belong to. After that, I create a playbook and reference the YAML file using the `vars_files:` argument. I then define a task that uses the `loop:` directive to iterate over all users from the variable file. Each user is treated as an individual item, and I use this item variable to specify the username and the groups for each user in the task.


# QUESTION B

Write a playbook that uses

    with_fileglob: 'files/*.md5'

to copy all `\*.md` files in the `files/` directory to the `deploy` user's directory on the `db` server(s).

For now you can create empty files in the `files/` directory called anything as long as the suffix is `.md`:

    $ touch files/foo.md files/bar.md files/baz.md


**Answer**
First, I create the .md files in my `files` directory. After that, I create a new playbook, shown below. I configure Ansible to become the `deploy` user, and then add a task that uses the `ansible.builtin.copy` module. In this task, the `src:` argument is set to `"{{ item }}"`, which means that Ansible will iterate over all files returned by the `with_fileglob` directive. Each of these files will then be copied to the specified destination in `dest:` on the database server, with the file permissions defined by the `mode:` argument.


**PROMPT THAT PROVES THE FILES HAVE BEEN SUCCESFULLY ADDED TO DBSERVER**
```bash
jesper@jesdeb:~/ansible$ ansible db -m ansible.builtin.shell -a "ls -l /home/deploy"
192.168.121.202 | CHANGED | rc=0 >>
total 0
-rw-r--r--. 1 deploy deploy 0 Oct 20 11:17 bar.md
-rw-r--r--. 1 deploy deploy 0 Oct 20 11:17 baz.md
-rw-r--r--. 1 deploy deploy 0 Oct 20 11:17 foo.md
```

# BONUS QUESTION

Add a password to each user added to the playbook that creates the users. Do not write passwords in plain
text in the playbook, but use the password hash, or encrypt the passwords using `ansible-vault`.

There are various utilities that can output hashed passwords, check the FAQ for some pointers.


**Answer**

First i add the password argument in my "users and groups" file and i make sure to use the password_hash command and specify that it should be hashed with the SHA-512 standard. I then proceed with configuring the playbook by adding the line `password: "{{ item.password }}"` in my task that loops over my yaml file. I also want to make sure that the yaml file is encrypted so i use the command `ansible-vault encrypt 11-users.yaml`. I choose the same password that is stored within my `~/.vault_pass.txt` file. 

**YAML FILE WHICH SHOWS THE PASSWORD ARGUMENT**
```yaml
users:

  - name: alovelace
    groups:
      - wheel
      - video
      - audio
    password: "{{ 'secretpassword' | password_hash('sha512') }}"

  - name: aturing
    groups:
      - tape
    password: "{{ 'secretpassword' | password_hash('sha512') }}"

  - name: edijkstra
    groups:
      - tcpdump
    password: "{{ 'secretpassword' | password_hash('sha512') }}"

  - name: ghopper
    groups:
      - audio
    password: "{{ 'secretpassword' | password_hash('sha512') }}"
```

# BONUS BONUS QUESTION

Add the real names of the users we added earlier to the GECOS field of each account. Google is your friend.

**Answer**

By configuring the YAML file that contains the user information, I add the argument `real_name:` with the user's full name as its value. In my playbook, I then include the line `comment: "{{ item.real_name }}"` within the task that iterates through the users defined in the YAML file.  

# Resources and Documentation

* [loops](https://docs.ansible.com/ansible/latest/playbook_guide/playbooks_loops.html)
* [ansible.builtin.user](https://docs.ansible.com/ansible/latest/collections/ansible/builtin/user_module.html)
* [ansible.builtin.fileglob](https://docs.ansible.com/ansible/latest/collections/ansible/builtin/fileglob_lookup.html)
* https://docs.ansible.com/ansible/latest/reference_appendices/faq.html#how-do-i-generate-encrypted-passwords-for-the-user-module

