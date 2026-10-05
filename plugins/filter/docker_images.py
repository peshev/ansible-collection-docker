import re
from typing import Optional
from urllib.parse import urlparse

from jinja2 import Undefined


class FilterModule(object):
    def filters(self):
        return {
            'parse_docker_image_name': parse_docker_image_name,
            'format_docker_image_name': format_docker_image_name,
            'normalize_docker_image': normalize_docker_image,
            'registry_netloc': registry_netloc
        }


# https://docs.docker.com/reference/cli/docker/image/tag/
# [HOST[:PORT]/]NAMESPACE/REPOSITORY[:TAG]
ip_address_pattern = r"(([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.){3}([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])"
hostname_pattern = r"(([a-zA-Z0-9]|[a-zA-Z0-9][a-zA-Z0-9\-]*[a-zA-Z0-9])\.)*([A-Za-z0-9]|[A-Za-z0-9][A-Za-z0-9\-]*[A-Za-z0-9])"
port_pattern = r"(6553[0-5]|655[0-2][0-9]|65[0-4][0-9]{2}|6[0-4][0-9]{3}|[1-5][0-9]{4}|[1-9][0-9]{0,3})"
docker_image_regex = re.compile(
    fr"(?:(?P<registry>(?:{hostname_pattern}|{ip_address_pattern})(?::{port_pattern})?)/)?((?P<namespace>.+)/)?(?P<repository>[^/:]*)(:(?P<tag>.*))?")

pull_policy_mapping = {
    "Always": "always",  # k8s imagePullPolicy
    "IfNotPresent": "not_present",  # k8s imagePullPolicy
    "Never": None,  # k8s imagePullPolicy
    "always": "always",  # docker compose pull_policy
    "not_present": "not_present",  # default
    "if_not_present": "not_present",  # docker compose pull_policy
    "missing": "not_present",  # docker compose pull_policy
    "never": None,  # docker compose pull_policy
    "build": "build",  # docker compose pull_policy
}


def registry_netloc(url, specify_default_port=False):
    if isinstance(url, str) and not (url.startswith('http://') or url.startswith('https://')):
        return url
    parsed_url = urlparse(url) if isinstance(url, str) else url
    port = None
    if parsed_url.port:
        port = str(parsed_url.port)
    elif specify_default_port:
        if parsed_url.scheme == "https":
            port = "443"
        else:
            port = "80"
    result = parsed_url.hostname
    if port:
        result += ":" + port
    return result


class RequiredValueException(Exception):
    pass


class InvalidValueException(Exception):
    pass


def to_mapping(obj, separators="="):
    if isinstance(obj, dict):
        return obj
    elif isinstance(obj, list):
        result = {}
        for i in obj:
            for s in separators:
                parts = str(i).split(s, maxsplit=1)
                if len(parts) == 2:
                    result[parts[0]] = parts[1]
                    break
        return result
    else:
        raise InvalidValueException(f"Unexpected value {obj}")


def to_list(lst, element_type):
    if lst is None:
        return lst
    else:
        try:
            _ = iter(lst)
        except TypeError:
            lst = [lst]

        return [element_type(i) for i in lst]


def to_scalar(s, _type):
    if s is None:
        return None
    else:
        return _type(s)


def required(o):
    if o is None:
        raise RequiredValueException()
    else:
        return o


def validate_enum(o, options):
    if o is not None and o not in options:
        raise InvalidValueException(f"Value is not one of {options}")
    return o


def validate_regex(o, regex):
    if o is not None and not regex.match(o):
        raise InvalidValueException(f"Value does not match {regex.pattern}")
    return o


byte_value_regex = re.compile(r"\d+([bkmg]b?)?", re.I)


def validate_byte_value(o):
    if o is not None:
        if isinstance(o, int):
            return o
        else:
            return validate_regex(str(o), byte_value_regex)
    return o


platform_regex = re.compile(r"([^/]+/)?([^/]+/)?[^/]+")

build_schema = {
    "args": lambda x: to_mapping(x, "="),
    "cache_from": lambda x: to_list(x, lambda i: to_scalar(i, str)),
    "context": lambda x: required(to_scalar(x, str)),
    "dockerfile": lambda x: to_scalar(x, str),
    "extra_hosts": lambda x: to_mapping(x, "=:"),
    "labels": lambda x: to_mapping(x, "="),
    "network": lambda x: validate_enum(to_scalar(x, str), ["default", "none", "host"]),
    "no_cache": lambda x: to_scalar(x, bool),
    "platforms": lambda x: to_list(x, lambda i: validate_regex(str(i), platform_regex)),
    "pull": lambda x: to_scalar(x, bool),
    "shm_size": lambda x: validate_byte_value(x),

    # The following properties from the docker compose build schema are not supported:

    # "additional_contexts", # No support in community.docker.docker_build
    # "cache_to", # No support in community.docker.docker_build
    # "dockerfile_inline", # No support in community.docker.docker_build
    # "entitlements", # No support in community.docker.docker_build
    # "isolation", # No support in community.docker.docker_build
    # "privileged", # No support in community.docker.docker_build
    # "provenance", # No support in community.docker.docker_build
    # "sbom", # No support in community.docker.docker_build
    # "secrets", # Can't support it, since we need the secrets from the docker-compose.yml file, which we don't have here
    # "ssh", # No support in community.docker.docker_build
    # "tags", # No support in community.docker.docker_build, also doesn't make sense for this filter's use-case
    # "targets", # Doesn't make sense for this filter's use-case
    # "ulimits" # No support in community.docker.docker_build

}


def normalize_dict(d, schema):
    result = {}
    for k, v in d.items():
        if k not in schema:
            raise Exception(f"Unexpected property: {k}")
        try:
            v = schema[k](v)
        except RequiredValueException:
            raise Exception(f"{k} is required, but missing")
        except InvalidValueException as e:
            raise Exception(f"Value for {k} is invalid: {e.args[0]}")
        if v is None:
            v = Undefined()
        result[k] = v
    return result


def parse_docker_image_name(name):
    return docker_image_regex.match(name).groupdict()


def format_docker_image_name(image):
    name = ""
    if image.get("registry"):
        name += image['registry'] + "/"
    if image.get("namespace"):
        name += image['namespace'] + "/"
    name += image['repository']
    if image.get("tag"):
        name += ":" + image['tag']
    return name


def normalize_docker_image(image, default_pull_policy="not_present", default_build: Optional[dict] = None):
    build = default_build or {}
    pull_policy = default_pull_policy
    if isinstance(image, str):
        name = image
    else:
        if 'name' in image:
            name = image['name']
        elif 'image' in image:
            name = image['image']
        else:
            raise Exception(f"No image name found in {image}")

        if 'pull' in image:
            pull_policy = image['pull']
        elif 'pull_policy' in image:
            pull_policy = image['pull_policy']
        elif 'imagePullPolicy' in image:
            pull_policy = image['imagePullPolicy']

        if pull_policy == "build":
            if 'build' in image:
                if isinstance(image['build'], str):
                    build.update({'context': image['build']})
                elif isinstance(image['build'], dict):
                    build.update(normalize_dict(image['build'], build_schema))
                elif image['build'] is not None:
                    raise Exception(f"Unexpected value for build property: {build}")
            else:
                raise Exception(f"{name} has a pull_policy of 'build' but no build property")

    result = {
        "image": parse_docker_image_name(name),
        "pull": pull_policy_mapping[pull_policy],
    }
    if build:
        result['build'] = build
    return result
