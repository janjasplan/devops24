# Examination 9 - Use Ansible Vault for sensitive information

In the previous examination we set a password for the `webappuser`. To keep this password
in plain text in a playbook, or otherwise, is a huge security hole, especially
if we publish it to a public place like GitHub.

There is a way to keep sensitive information encrypted and unlocked at runtime with the
`ansible-vault` tool that comes with Ansible.

https://docs.ansible.com/ansible/latest/vault_guide/index.html

*IMPORTANT*: Keep a copy of the password for _unlocking_ the vault in plain text, so that
I can run the playbook without having to ask you for the password.

# QUESTION A

Make a copy of the playbook from the previous examination, call it `09-mariadb-password.yml`
and modify it so that the task that sets the password is injected via an Ansible variable,
instead of as a plain text string in the playbook.

**Answer**

I create a file called `secrets.yml` and add the line `db_password: secretpassword`.
In my playbook, I then add the argument `vars_files:` at the playbook level and assign `secrets.yml` as its value.

The `password:` argument under the task "Create database user 'webappuser'" is then modified to use the value `{{ db_password }}`.
The double curly brackets indicate that the value of the variable is inserted here. 

# QUESTION B

When the [QUESTION A](#question-a) is solved, use `ansible-vault` to store the password in encrypted
form, and make it possible to run the playbook as before, but with the password as an
Ansible Vault secret instead.

**Answer**

To run the same playbook but instead using an Ansible Vault secret as a password i simply encrypt my `secrets.yml` file. When i run command `ansible-vault encrypt secrets.yml` a prompt tells me to give the file a password, and then the tool proceeds to encrypt the file. 

It is not considered best practice to always type in the Vault password manually. With the command `echo "Linux4Ever" > ~/.vault_pass.txt`, I create a file that stores my Vault password. I then change the file permissions using `chmod 600 ~/.vault_pass.txt` so that only I can read and write to it. In the ansible.cfg file, I add the line vault_password_file = ~/.vault_pass.txt under the `[defaults]` section. This way, whenever I run my playbook in the future, Ansible will automatically retrieve the Vault password from the configuration file, allowing it to decrypt and use the encrypted variables without requiring any manual password input. 