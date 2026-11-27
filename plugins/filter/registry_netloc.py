DOCUMENTATION = r"""
name: registry_netloc
short_description: Extract a registry hostname and port
description:
  - Extracts the hostname and explicit port from an HTTP or HTTPS URL.
  - Strings without an C(http://) or C(https://) prefix pass through unchanged.
positional: _input, specify_default_port
options:
  _input:
    description: Registry URL or hostname string.
    type: str
    required: true
  specify_default_port:
    description: Include port C(80) for HTTP or C(443) for HTTPS if the URL omits the port.
    type: bool
    default: false
"""

EXAMPLES = r"""
registry: "{{ 'https://registry.example.com/v2/' | peshev.docker.registry_netloc(specify_default_port=true) }}"
"""

RETURN = r"""
_value:
  description: Registry hostname with a port when applicable.
  type: str
"""

from ansible_collections.peshev.docker.plugins.module_utils.docker_images import registry_netloc


class FilterModule:
    def filters(self):
        return {'registry_netloc': registry_netloc}
