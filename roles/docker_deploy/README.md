# peshev.docker.docker_deploy

Renders deployment files, reads image references from the Compose template, and deploys the project with Docker Compose V2 or as a Docker Swarm stack.

Install Docker Engine and the `community.docker` collection. Use hosts with the Compose plugin for Compose projects and target Swarm managers for stacks. The Swarm tasks install `python3-jsondiff` and `python3-yaml` with the target package manager.

Create `templates/docker-compose.yml.j2` beside your playbook with a `services` mapping, then run:

```yaml
- hosts: docker_hosts
  become: true
  roles:
    - role: peshev.docker.docker_deploy
      vars:
        docker_deploy_stack_name: web
        docker_deploy_swarm: false
```

| Variable | Purpose |
| --- | --- |
| `docker_deploy_stack_name` | Compose project or Swarm stack name. |
| `docker_deploy_swarm` | Deploy to Swarm when `true` (the default), or use Compose when `false`. |
| `docker_deploy_project_dir` | Rendered files directory, normally under `/root/src`. |
| `docker_deploy_compose_file_name` | Compose filename. The role reads an identically named template with a `.j2` suffix. |
| `docker_deploy_templates` | Files to render into the project directory. |
| `docker_deploy_dirs` | Additional directories to create. |
| `docker_deploy_secrets` | Mapping of secret names to values. Swarm uses Docker secrets. Compose writes files under the project’s `secrets` directory by default. |
| `docker_deploy_offline` | Requests controller-side image preparation through the [image role](../docker_images/README.md). |

See [role defaults](defaults/main.yml) for paths and the full variable list.
