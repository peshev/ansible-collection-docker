DOCUMENTATION = r"""
name: normalize_docker_image
short_description: Normalize a Docker image entry
description:
  - Accepts an image reference string or a dictionary with C(name) or C(image). If both keys are present, C(name) takes precedence.
  - Reads the policy from C(pull), C(pull_policy), or C(imagePullPolicy), in that order, before applying O(default_pull_policy).
  - Maps C(Always) and C(always) to C(always).
  - Maps C(IfNotPresent), C(if_not_present), C(not_present), and C(missing) to C(not_present).
  - Maps C(Never) and C(never) to null. Keeps C(build) as C(build). Policy values are case-sensitive.
  - A dictionary with an effective policy of C(build) must include a C(build) key. A string supplies the build context, a dictionary supplies build options, and null keeps the defaults.
  - Supported build keys are C(context), C(dockerfile), C(args), C(cache_from), C(extra_hosts), C(labels), C(network), C(no_cache), C(platforms), C(pull), and C(shm_size).
  - C(args) and C(labels) accept dictionaries or lists of C(KEY=VALUE) strings. C(extra_hosts) also accepts C(HOST:ADDRESS) list entries.
  - C(network) accepts C(default), C(none), and C(host).
positional: _input, default_pull_policy, default_build
options:
  _input:
    description: Image reference string or image entry dictionary.
    type: raw
    required: true
  default_pull_policy:
    description: Pull policy used when the input supplies none.
    type: str
    default: not_present
  default_build:
    description:
      - Initial build options.
      - Image-specific build options update this dictionary in place when it is nonempty.
    type: dict
"""

EXAMPLES = r"""
image: "{{ {'name': 'web:1.2', 'pull_policy': 'build', 'build': './web'} | peshev.docker.normalize_docker_image }}"
"""

RETURN = r"""
_value:
  description: Dictionary with the parsed reference under C(image), the normalized policy under C(pull), and C(build) when the build options are nonempty.
  type: dict
"""

from ansible_collections.peshev.docker.plugins.module_utils.docker_images import normalize_docker_image


class FilterModule:
    def filters(self):
        return {'normalize_docker_image': normalize_docker_image}
