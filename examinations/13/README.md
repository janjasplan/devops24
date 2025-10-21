# Examination 13 - Handlers

In [Examination 5](../05/) we asked the question what the disadvantage is of restarting
a service every time a task is run, whether or not it's actually needed.

In order to minimize the amount of restarts and to enable a complex configuration to run
through all its steps before reloading or restarting anything, we can trigger a _handler_
to be run once when there is a notification of change.

Read up on [Ansible handlers](https://docs.ansible.com/ansible/latest/playbook_guide/playbooks_handlers.html)

In the previous examination ([Examination 12](../12/)), we changed the structure of the project to two separate
roles, `webserver` and `dbserver`.

# QUESTION A

Make the necessary changes to the `webserver` role, so that `nginx` only reloads when it's configuration
has changed in a task, such as when we have changed a `server` stanza.

Also note the difference between `restarted` and `reloaded` in the [ansible.builtin.service](https://docs.ansible.com/ansible/latest/collections/ansible/builtin/service_module.html) module.

In order for `nginx` to pick up any configuration changes, it's enough to do a `reload` instead of
a full `restart`.

**Answer**

First, I create a handler inside the `handlers` directory within my webserver role.
In this handler, I use the `ansible.builtin.service` module with the arguments `name: nginx` and `state: reloaded`.
This ensures that the nginx service will be reloaded instead of restarted when I notify the handler.
I then include my handler in `handlers/main.yml` using the `import_tasks:` directive.

Next, I make sure that the handler is triggered when needed by adding the `notify:` argument to the task that updates the users, and setting the value to the handler’s name (reload nginx).
Finally, I remove the original task that restarted nginx after every configuration change, since the handler now takes care of reloading the service only when it’s actually required. 
