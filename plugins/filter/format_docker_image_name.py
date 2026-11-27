DOCUMENTATION = r"""
name: format_docker_image_name
short_description: Assemble a Docker image reference
description:
  - Joins image components into a tagged or untagged Docker image reference.
positional: _input
options:
  _input:
    description: Image components with a required C(repository) and optional C(registry), C(namespace), and C(tag) keys.
    type: dict
    required: true
"""

EXAMPLES = r"""
image_name: "{{ {'repository': 'web', 'tag': '1.2'} | peshev.docker.format_docker_image_name }}"
"""

RETURN = r"""
_value:
  description: Image reference string. Empty or null optional components are omitted.
  type: str
"""

from ansible_collections.peshev.docker.plugins.module_utils.docker_images import format_docker_image_name


class FilterModule:
    def filters(self):
        return {'format_docker_image_name': format_docker_image_name}
