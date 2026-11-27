# peshev.docker.docker_registry

Contains scaffolding for deploying a Docker Registry service on Swarm. The [Compose template](templates/docker-compose.yml.j2) publishes the configured host port to port 5000 in the container and mounts persistent storage at `/var/lib/registry`.

The [main task file](tasks/main.yml) has an incomplete stack definition. It references the `docker_manager` inventory group and does not wire in the Compose template or the separate image installation tasks. Complete that wiring before using this role for deployment.

| Variable | Purpose |
| --- | --- |
| `docker_registry_host` | Registry hostname. |
| `docker_registry_port` | Published host port. |
| `docker_registry_storage_dir` | Host directory for registry data. |
| `docker_registry_ip_address` | Optional address for an entry in the managed host’s `/etc/hosts`. |
| `docker_registry_image` | Image repository, defaulting to `registry`. |
| `docker_registry_image_version` | Image tag, defaulting to `2`. |

See [role defaults](defaults/main.yml) and the [registry client configuration role](../docker_registry_config/README.md).
