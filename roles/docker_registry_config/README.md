# peshev.docker.docker_registry_config

Updates registry settings in an existing Docker daemon JSON file and can install a CA certificate for a private registry. The role defaults to `/etc/docker/daemon.json` and stores CA certificates under `/etc/docker/certs.d`. Changes notify the Docker restart handler.

```yaml
- hosts: docker_hosts
  become: true
  roles:
    - role: peshev.docker.docker_registry_config
      vars:
        registry_config_docker_private_registries:
          - url: https://registry.example.com:5000
            ca: registry-ca.crt
```

Place `registry-ca.crt` in the playbook’s `files/` directory. To manage registry mirrors, set `registry_config_docker_registry_mirrors` to a list of mappings with a `url` key. The private registry mappings accept `url`, `ca`, and `address`. For entries with a CA, an optional address adds a hostname mapping to `/etc/hosts`.

The current [filter implementation](../../plugins/filter/docker_registry_config.py) references an undefined helper when processing HTTP URLs or entries without a CA. Such entries can fail when the role updates an existing daemon configuration.

See [role defaults](defaults/main.yml) for paths, service name, and list replacement options.
