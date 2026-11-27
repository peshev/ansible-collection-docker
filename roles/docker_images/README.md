# peshev.docker.docker_images

Pulls container images on managed hosts. Failed pulls can fall back to the controller, where the role can also build images from a local context. It can export controller images to an archive and load them on managed hosts.

Install `community.docker` and make Docker available on managed hosts and on the controller when pulling, building, or exporting there.

```yaml
- hosts: docker_hosts
  become: true
  roles:
    - role: peshev.docker.docker_images
      vars:
        docker_images_install_offline: false
        docker_images:
          - alpine:3
          - image: example/web:local
            pull: build
            build:
              context: "{{ playbook_dir }}/web"
```

| Variable | Purpose |
| --- | --- |
| `docker_images` | List of image strings or mappings. |
| `docker_images_default_pull_policy` | Default pull policy, set to `not_present`. |
| `docker_images_registry_logins` | Registry credentials for the managed-host login step. |
| `docker_images_offline_assets_dir` | Controller archive directory, which defaults to `offline_assets/` beside the playbook. |
| `docker_images_transfer_load` | Copy and load the image archive on managed hosts. Defaults to `true`. |
| `docker_images_transfer_push` | Enable registry push. Requires `docker_image_private_registry`. |

The tasks check `docker_images_install_offline` even though [role defaults](defaults/main.yml) define `docker_images_offline`. Set `docker_images_install_offline: false` for normal pulls. Set it to `true` to source images on the controller. The archive is exported during the transfer step, so running only the `prepare-offline` tag leaves that step out.
