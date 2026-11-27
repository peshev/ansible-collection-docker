DOCUMENTATION = r"""
name: add_private_registries
short_description: Add private registries to Docker daemon configuration
description:
  - Processes HTTP entries and entries without a nonempty C(ca) as insecure registries.
  - Qualifying entries are intended to add hostnames and explicit ports to C(insecure-registries), skipping duplicates in append mode.
positional: _input, private_registries, replace
options:
  _input:
    description: Docker daemon configuration dictionary to update.
    type: dict
    required: true
  private_registries:
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
    description: Replace C(insecure-registries) when there are entries to add. An empty result leaves the existing key unchanged.
    type: bool
    default: false
notes:
  - Entries that qualify for C(insecure-registries) currently raise an undefined-name error because the implementation lacks a C(registry_netloc) import.
"""

EXAMPLES = r"""
daemon_config: "{{ {} | peshev.docker.add_private_registries([{'url': 'https://registry.example.com:5000', 'ca': 'registry-ca.crt'}]) }}"
"""

RETURN = r"""
_value:
  description: The input Docker daemon configuration dictionary after any updates.
  type: dict
"""

from ansible_collections.peshev.docker.plugins.module_utils.docker_registry_config import add_private_registries


class FilterModule:
    def filters(self):
        return {'add_private_registries': add_private_registries}
