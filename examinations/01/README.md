# Examination 1 - Understanding SSH and public key authentication

Connect to one of the virtual lab machines through SSH, i.e.

    $ ssh -i deploy_key -l deploy webserver

Study the `.ssh` folder in the home directory of the `deploy` user:

    $ ls -ld ~/.ssh

Look at the contents of the `~/.ssh` directory:

    $ ls -la ~/.ssh/

## QUESTION A

What are the permissions of the `~/.ssh` directory?

Answer: The permissions are set to drwx------ for the "deploy" user.
This means it is a directory (d), and the owner (deploy) has read, write, and execute permissions, while no other users have access.

Why are the permissions set in such a way?

**Answer** 

These permissions ensure that only the deploy user can access and modify the SSH configuration and keys. This prevents other users on the system from viewing or tampering with private keys, which enhances the security of SSH authentication.

## QUESTION B

What does the file `~/.ssh/authorized_keys` contain?

**Answer** 

The authorized_keys file contains one or more public SSH keys that identify which clients are allowed to log in to the user account. When you try to connect via SSH, the server checks if your public key (stored in this file) matches your private key on the host computer. If they match, access is granted without using a password.

## QUESTION C

When logged into one of the VMs, how can you connect to the
other VM without a password?

**Answer** 

First, I log in to my dbserver to change the password if needed. Then, I generate a new SSH key pair on my webserver.
Once the keys are created, I use the ssh-copy-id command to copy my public key to the dbserver. After that, I can easily connect from my webserver to the dbserver using my private key, without having to enter a password

Changing password in my dbserver: 
sudo passwd deploy
Generating keys in my webserver: 
ssh-keygen -t ed25519
Copy the public key from my webserver to my dbserver(I have to submit my password to the dbserver which i just created): ssh-copy-id -i ~/.ssh/id_ed25519.pub deploy@192.168.121.202
Get access to my dbserver from my webserver with ssh: 
ssh deploy@dbserver

### Hints:

* man ssh-keygen(1)
* ssh-copy-id(1) or use a text editor

## BONUS QUESTION

Can you run a command on a remote host via SSH? How?

**Answer**
Yes, you can easily run a command on a remote host using the standard ssh command, followed by the command you want to execute inside quotation marks. This will not open up an interactive session.

```bash
ssh deploy@dbserver "ls -l /home/files
```
