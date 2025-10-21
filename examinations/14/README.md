# Examination 14 - Firewalls (VG)

The IT security team has noticed that we do not have any firewalls enabled on the servers,
and thus ITSEC surmises that the servers are vulnerable to intruders and malware.

As a first step to appeasing them, we will install and enable `firewalld` and
enable the services needed for connecting to the web server(s) and the database server(s).

# QUESTION A

Create a playbook `14-firewall.yml` that utilizes the [ansible.posix.firewalld](https://docs.ansible.com/ansible/latest/collections/ansible/posix/firewalld_module.html) module to enable the following services in firewalld:

* On the webserver(s), `http` and `https`
* On the database servers(s), the `mysql`

You will need to install `firewalld` and `python3-firewall`, and you will need to enable
the `firewalld` service and have it running on all servers.

When the playbook is run, you should be able to do the following on each of the
servers:

## dbserver

    [deploy@dbserver ~]$ sudo cat /etc/firewalld/zones/public.xml
    <?xml version="1.0" encoding="utf-8"?>
    <zone>
      <short>Public</short>
      <description>For use in public areas. You do not trust the other computers on networks to not harm your computer. Only selected incoming connections are accepted.</description>
      <service name="ssh"/>
      <service name="dhcpv6-client"/>
      <service name="cockpit"/>
      <service name="mysql"/>
    <forward/>
    </zone>

## webserver

    [deploy@webserver ~]$ sudo cat /etc/firewalld/zones/public.xml
    <?xml version="1.0" encoding="utf-8"?>
    <zone>
      <short>Public</short>
      <description>For use in public areas. You do not trust the other computers on networks to not harm your computer. Only selected incoming connections are accepted.</description>
      <service name="ssh"/>
      <service name="dhcpv6-client"/>
      <service name="cockpit"/>
      <service name="https"/>
      <service name="http"/>
      <forward/>
    </zone>

# Resources and Documentation

https://firewalld.org/


**Answer**

In this playbook, I am using three different play levels. The first one contains tasks that affect all hosts. These tasks install the `firewalld` and `python3-firewall` packages and ensure that the `firewalld` service is enabled and running.

In the second level, I configure firewalld on the webserver. Using a loop, I iterate over the services `http` and `https` and enable each one. The `permanent:` argument ensures that the configuration changes are saved and persist after a reboot, while the `immediate:` argument applies the changes immediately without requiring a reload.

Finally, I add a third level that configures firewalld on the database server by enabling the mysql service.


**Output that shows that the services http and https are enabled in my firewall within the webserver**
```bash
jesper@jesdeb:~/ansible$ ansible web -m ansible.builtin.command -a "sudo cat /etc/firewalld/zones/public.xml"
192.168.121.219 | CHANGED | rc=0 >>
<?xml version="1.0" encoding="utf-8"?>
<zone>
  <short>Public</short>
  <description>For use in public areas. You do not trust the other computers on networks to not harm your computer. Only selected incoming connections are accepted.</description>
  <service name="ssh"/>
  <service name="dhcpv6-client"/>
  <service name="cockpit"/>
  <service name="http"/>
  <service name="https"/>
  <forward/>
</zone>
```

**Output that shows that the mysql service are enabled in the firewall within the dbserver**
```bash
jesper@jesdeb:~/ansible$ ansible db -m ansible.builtin.command -a "sudo cat /etc/firewalld/zones/public.xml"
192.168.121.202 | CHANGED | rc=0 >>
<?xml version="1.0" encoding="utf-8"?>
<zone>
  <short>Public</short>
  <description>For use in public areas. You do not trust the other computers on networks to not harm your computer. Only selected incoming connections are accepted.</description>
  <service name="ssh"/>
  <service name="dhcpv6-client"/>
  <service name="cockpit"/>
  <service name="mysql"/>
  <forward/>
</zone>
```