# peshev.docker.keepalived

Configures a shared virtual IP with Keepalived and VRRP. The [template](templates/keepalived.conf.jinja2) tracks the local HAProxy process with `killall -0 haproxy` and uses VRRP router ID `51`.

The [main task file](tasks/main.yml) imports the package role as `peshev.docker.install_pacakges`. Correct that reference to `peshev.docker.install_packages` before running this role.

| Variable | Default | Purpose |
| --- | --- | --- |
| `keepalived_interface` | `ens192` | Interface carrying VRRP traffic. Set this per host as needed. |
| `keepalived_state` | `MASTER` | Initial VRRP state. Set the peer to `BACKUP`. |
| `keepalived_priority` | `100` | Election priority. Set a lower value on the backup. |
| `keepalived_vip` | Unset | Virtual IP to configure on each peer. |
| `keepalived_conf_path` | `/etc/keepalived/keepalived.conf` | Rendered configuration path. |

Run with privilege escalation on both peers. The role enables `net.ipv4.ip_nonlocal_bind` and starts and enables Keepalived.
