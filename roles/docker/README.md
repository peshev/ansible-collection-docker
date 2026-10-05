# Ansible Role: Docker

Installs and configures Docker Engine on Debian- and Red Hat-based Linux systems. The role supports both normal repository-based installation and package staging for offline or air-gapped hosts.

## Supported platforms

- Ubuntu 22.04, 24.04, and 26.04
- Debian 11, 12, and 13
- Red Hat Enterprise Linux 8, 9, and 10
- CentOS Stream 9 and 10
- Fedora 43, and 44

See [`meta/main.yml`](meta/main.yml) for the authoritative Galaxy platform metadata.

## Requirements

- Ansible 2.1 or newer
- Root privileges on managed hosts (`become: true`)
- The collections listed in [`requirements.yml`](requirements.yml)
- Internet access from managed hosts for a normal installation
- Docker Engine on the Ansible controller when preparing offline assets

Install the required collections with:

```shell
ansible-galaxy collection install -r requirements.yml
```

## Usage

```yaml
---
- name: Install Docker
  hosts: docker_hosts
  become: true
  roles:
    - role: peshev.docker
      vars:
        docker_users:
          - deploy
        docker_daemon_options:
          log-driver: json-file
          log-opts:
            max-size: 100m
            max-file: "3"
```

Users added to the `docker` group must start a new login session before the new group membership is available. Membership in this group grants root-equivalent privileges.

## Variables

The following are the principal user-facing variables. See [`defaults/main.yml`](defaults/main.yml) for the complete list and current defaults.

| Variable | Default | Description |
| --- | --- | --- |
| `docker_edition` | `ce` | Docker edition used to construct package names. |
| `docker_packages` | Docker Engine, CLI, rootless extras, containerd, and Buildx | Packages to install or remove. |
| `docker_packages_state` | `present` | Package state; must be `present` or `absent`. |
| `docker_install_compose_plugin` | `true` | Whether to manage the Docker Compose plugin. |
| `docker_compose_package` | `docker-compose-plugin` | Compose plugin package name. |
| `docker_repo_url` | `https://download.docker.com/linux` | Base URL for Docker repositories. |
| `docker_apt_release_channel` | `stable` | APT repository channel. |
| `docker_users` | `[]` | Users to append to `docker_group`. |
| `docker_group` | `docker` | Group allowed to use Docker without `sudo`. |
| `docker_daemon_options` | `{}` | Complete contents written to `/etc/docker/daemon.json`. |
| `docker_service_manage` | `true` | Whether to manage the Docker and containerd services. |
| `docker_service_state` | `started` | Desired service state. |
| `docker_service_enabled` | `true` | Whether services start at boot. |
| `docker_service_start_command` | `""` | Optional replacement for Docker's systemd `ExecStart` command. |
| `docker_system_prune` | `true` | Install and enable the scheduled prune timer. |
| `docker_system_prune_all` | `false` | Pass `--all` to `docker system prune`. |
| `docker_system_prune_volumes` | `false` | Pass `--volumes` to `docker system prune`. |
| `docker_system_prune_older_than` | `720h` | Prune objects older than this duration. |
| `docker_system_prune_frequency` | `daily` | systemd calendar expression for the prune timer. |

Setting `docker_daemon_options` replaces the role-managed daemon JSON file; include every option that should remain present.

## Offline installation

Offline mode first builds a distribution-specific container image on the Ansible controller, downloads the required packages and dependencies. It then copies and installs that archive on the managed host.

```yaml
---
- name: Install Docker from staged packages
  hosts: offline_docker_hosts
  become: true
  roles:
    - role: peshev.docker
      vars:
        docker_offline_install: true
```

Relevant variables:

| Variable | Default | Description |
| --- | --- | --- |
| `docker_offline_install` | `false` | Enable offline package preparation and installation. The legacy `offline_install` variable is also accepted. |

To prepare assets while the controller still has internet access, run the play with only the preparation tag:

```shell
ansible-playbook site.yml --tags prepare-offline
```

Copy the resulting offline-assets directory to the air-gapped controller, retain the same `docker_offline_assets_dir`, and install without rebuilding assets:

```shell
ansible-playbook site.yml --skip-tags prepare-offline
```

## Testing

The Molecule scenarios use Docker and systemd-enabled test containers. On Linux, load the NAT module if it is not already available:

```shell
sudo modprobe iptable_nat
tox
```

Individual scenarios can be run with environments such as `tox -e default`, `tox -e offline-prepare`, and `tox -e offline-install`.

## License

MIT-0

## Author

Peter Peshev
