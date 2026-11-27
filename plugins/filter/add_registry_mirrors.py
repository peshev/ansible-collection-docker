DOCUMENTATION = r"""
name: add_registry_mirrors
short_description: Add registry mirrors to Docker daemon configuration
description:
  - Adds mirror URLs to C(registry-mirrors), skipping duplicates in append mode.
  - HTTP entries and entries without a nonempty C(ca) also qualify for C(insecure-registries).
  - O(replace) applies only to C(registry-mirrors).
positional: _input, registry_mirrors, replace
options:
  _input:
    description: Docker daemon configuration dictionary to update.
    type: dict
    required: true
  registry_mirrors:
    description: Registry entries to process.
    type: list
    elements: dict
    required: true
    suboptions:
      url:
        description: Registry URL.
        type: str
        required: true
      ca:
        description: CA reference used to classify HTTPS entries. Certificate installation is handled by the role.
        type: str
  replace:
    description: Replace C(registry-mirrors) when there are entries to add. An empty result leaves the existing key unchanged.
    type: bool
    default: false
notes:
  - Entries that qualify for C(insecure-registries) currently raise an undefined-name error because the implementation lacks a C(registry_netloc) import.
"""

EXAMPLES = r"""
daemon_config: "{{ {} | peshev.docker.add_registry_mirrors([{'url': 'https://mirror.example.com', 'ca': 'registry-ca.crt'}]) }}"
"""

RETURN = r"""
_value:
  description: The input Docker daemon configuration dictionary after any updates.
  type: dict
"""

from ansible_collections.peshev.docker.plugins.module_utils.docker_registry_config import add_registry_mirrors


class FilterModule:
    def filters(self):
        return {'add_registry_mirrors': add_registry_mirrors}
