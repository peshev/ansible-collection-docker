# peshev.docker

An Ansible collection for installing Docker Engine, managing container images, and deploying applications with Docker Compose or Docker Swarm. It includes workflows for staging packages and images for air-gapped hosts.

## Installation

From the root of a source checkout, use an Ansible environment with `ansible-galaxy` available:

```sh
ansible-galaxy collection install -r roles/docker/requirements.yml
ansible-galaxy collection build
ansible-galaxy collection install peshev-docker-0.0.1.tar.gz
```

See the [Docker role documentation](roles/docker/README.md) for supported Linux distributions, configuration variables, and Molecule scenarios.

## Install Docker Engine

Add your managed hosts to a `docker_hosts` inventory group and save this playbook as `site.yml`:

```yaml
---
- name: Install Docker Engine
  hosts: docker_hosts
  become: true
  roles:
    - role: peshev.docker.docker
```

```sh
ansible-playbook -i inventory.yml site.yml
```

## Install Docker Engine on air-gapped hosts

Set `docker_offline_install: true` in the play. With Docker available on an internet-connected Ansible controller, stage the packages for the target distribution:

```sh
ansible-playbook -i inventory.yml site.yml --tags prepare-offline
```

Copy the `offline_assets/` directory alongside the playbook on the air-gapped controller. If you set `offline_assets_dir`, use that location. Run the same play against the target hosts using the staged packages:

```sh
ansible-playbook -i inventory.yml site.yml --skip-tags prepare-offline
```

## Roles

| Role | Purpose |
| --- | --- |
| [`peshev.docker.docker`](roles/docker/README.md) | Installs and configures Docker Engine and the Compose plugin. |
| [`peshev.docker.install_packages`](roles/install_packages/README.md) | Manages system packages using repositories or staged Debian and Red Hat package archives. |
| [`peshev.docker.docker_images`](roles/docker_images/README.md) | Pulls images and prepares, transfers, and loads image archives for offline use. |
| [`peshev.docker.docker_deploy`](roles/docker_deploy/README.md) | Renders project files and deploys a Compose project or Swarm stack. Supply a stack name and a Compose template. |
| [`peshev.docker.docker_registry_config`](roles/docker_registry_config/README.md) | Updates registry mirrors and private registry settings in an existing Docker daemon configuration and supports installing registry CA certificates. |
| [`peshev.docker.docker_registry`](roles/docker_registry/README.md) | Contains registry deployment scaffolding. The main task file has an incomplete Swarm stack definition. |
| [`peshev.docker.keepalived`](roles/keepalived/README.md) | Contains virtual IP configuration tasks. The package installation import currently references a misspelled role name. |

## Filters

- [Image filters](plugins/filter/docker_images.py) parse, format, and normalize image references and extract registry network locations.
- [Registry configuration filters](plugins/filter/docker_registry_config.py) update Docker daemon configuration dictionaries with registry mirrors and private registry settings.
