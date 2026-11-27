DOCUMENTATION = r"""
name: parse_docker_image_name
short_description: Split a Docker image reference into components
description:
  - Parses a tagged or untagged image reference into registry, namespace, repository, and tag.
  - A leading hostname-like component followed by a slash is treated as the registry. For example, C(team/web) sets C(registry) to C(team).
  - Digest references are unsupported.
positional: _input
options:
  _input:
    description: Docker image reference to split.
    type: str
    required: true
"""

EXAMPLES = r"""
image_parts: "{{ 'registry.example.com:5000/team/web:1.2' | peshev.docker.parse_docker_image_name }}"
"""

RETURN = r"""
_value:
  description: Dictionary with C(registry), C(namespace), C(repository), and C(tag) keys. Missing components are null.
  type: dict
"""

from ansible_collections.peshev.docker.plugins.module_utils.docker_images import parse_docker_image_name


class FilterModule:
    def filters(self):
        return {'parse_docker_image_name': parse_docker_image_name}
