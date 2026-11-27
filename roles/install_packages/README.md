# peshev.docker.install_packages

Installs or removes system packages. Online mode uses the target’s package manager and repositories. Offline mode stages Debian or Red Hat family packages and their dependencies in a distribution-specific Docker container on the Ansible controller.

```yaml
- hosts: linux
  become: true
  roles:
    - role: peshev.docker.install_packages
      vars:
        install_packages:
          - curl
          - jq
```

| Variable | Default | Purpose |
| --- | --- | --- |
| `install_packages` | `[]` | Package names. An empty list skips the role. |
| `install_packages_state` | `present` | Use `absent` to remove packages. |
| `install_packages_offline` | Value of `offline_install`, or `false` | Enable the offline workflow. |
| `install_packages_offline_assets_dir` | Value of `offline_assets_dir`, or `offline_assets/` beside the playbook | Controller directory for package archives. |
| `install_packages_offline_docker_container_image` | Derived from the target distribution and version | Container image used for downloading packages. |

To stage packages, set `install_packages_offline: true` and run the playbook with `--tags prepare-offline` on a connected controller with Docker. Copy the assets directory to the same location on the air-gapped controller, then rerun the playbook with `--skip-tags prepare-offline`. Stage package sets separately for different target distributions or versions.

See [role defaults](defaults/main.yml) for package download commands and pre-install and post-install hooks.
