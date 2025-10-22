# Examination 15 - Metrics (VG)

[Prometheus](https://prometheus.io/) is a powerful application used for event monitoring and alerting.

[Node Exporter](https://prometheus.io/docs/guides/node-exporter/) collects metrics for Prometheus from
the hardware and the kernel on a machine (virtual or not).

Start by running the Prometheus server and a Node Exporter in containers on your Ansible controller
(the you're running Ansible playbooks from). This can be accomplished with the [prometheus.yml](prometheus.yml)
playbook.

You may need to install [podman](https://podman.io/docs/installation) first.

If everything worked correctly, you should see the data exported from Node Exporter on http://localhost:9090/,
and you can browse this page in a web browser.

# QUESTION A

Make an Ansible playbook, `15-node_exporter.yml` that installs [Node Exporter](https://prometheus.io/download/#node_exporter)
on each of the VMs to export/expose metrics to Prometheus.

Node exporter should be running as a `systemd` service on each of the virtual machines, and
start automatically at boot.

You can find `systemd` unit files that you can use [here](https://github.com/prometheus/node_exporter/tree/master/examples/systemd), along with the requirements regarding users and permissions.

Consider the requirements carefully, and use Ansible modules to create the user, directories, copy files,
etc.

Also, consider the firewall configuration we implemented earlier, and make sure we can talk to the node
exporter port.

HINT: To get the `firewalld` service names available in `firewalld`, you can use

    $ firewall-cmd --get-services

on the `firewalld`-enabled hosts.

Note also that while running the `podman` containers on your host, you may sometimes need to stop and
start them.

    $ podman pod stop prometheus

and

    $ podman pod start prometheus

will get you on the right track, for instance if you've changed any of the Prometheus configuration.

# Resources and Information

* https://github.com/prometheus/node_exporter/tree/master/examples/systemd
* https://prometheus.io/docs/guides/node-exporter/


**Answer**

First i need to configure the `prometheus.yml` file with the ip adresses to my servers under the `targets:` argument. I then download the `systemd` unit files and move them to my `files` directory. To make sure node exporter is installed and enabled in my servers i followed theese steps:

1. I create a `vars:` that will act as the version of the node_exporter `node_exporter_version: "1.9.1"`. In case i want to run the playbook with a different version i can easily just change this value instead of changing it throughout of the script.

2. `Ensure node_exporter user exists` - I make sure that the `node_exporter` user exists and defines it as a system user. I also prevents anyone from loggin in interactively as the user. The `create:home:` argument is set to false since i dont want a home catalogue to be created.

3. `Download Node Exporter archive to temporary folder` - Here i create a temporary folder that i download the node_exporter archive to. 

4. `Extract Node Exporter binary` - I extract the Node Exporter binary with the `ansible.builtin.unarchive` module. And i set `remote_src:` to true which informs Ansible that the targeted archive file is on the remote host.

5. `Copy Node Exporter binary to /usr/sbin/node_exporter` - I then copy the Node Exporter binary to the selected `dest:`. I make sure that the owner and group to the binary file is `node_exporter`. I also set the `remote_src:` value to true.

6. `Create textfile collector directory` - Here i create a directory which is called textfile_collector. If i want any specific metrics that prometheus is gonna gather from Node Exporter i can add them here. 

7. `Copy Node Exporter systemd service and socket files` - I use the `loop` directive to create `items` of my `node_exporter.socket` and `node_exporter.service` which is then stored in the `dest:` value. With the `notify:` argument i call to a handler which will reload the systemd service. 

8. `Copy sysconfig file` - I also need to copy the `sysconfig.node_exporter` file to the set `dest:`.

9. `Start and enable the Node Exporter socket` - I proceed with a task which enables the `node_exporter.socket`. The `state:` is set to "started" so that it runs instantly and with the `enabled:` argument i make sure that it is started at boot.

10. `Enable Node Exporter service in firewalld` - I configure the `firewalld` service so that `node_exporters`TCP port (9100) is opened. The rule is enabled so that it will be set at boot. The argument `immediate:` is set to true so that the rule is set instantly. I also set `permanent:` to true so that the rule is set as long as it isnt changed.

11. Lastly i create a `handler:` which will reload systemd when i notify it. The `daemon_reload:` is set to true since `node_exporter.socket` and `node_exporter.service` both acts as services in the background. 