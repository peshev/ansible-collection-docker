from urllib.parse import urlparse


class FilterModule(object):
    def filters(self):
        return {
            'add_registry_mirrors': add_registry_mirrors,
            'add_private_registries': add_private_registries,
        }


def append_or_relace(d, k, lst, replace):
    if lst:
        if replace:
            d[k] = lst
        else:
            current_lst = d.setdefault(k, [])
            for registry_url in lst:
                if registry_url not in current_lst:
                    current_lst.append(registry_url)
    return d


def add_registry_mirrors(docker_json, registry_mirrors, replace=False):
    return append_or_relace(
        add_insecure_registries(docker_json, registry_mirrors),
        'registry-mirrors',
        [
            registry_mirror['url']
            for registry_mirror in
            registry_mirrors
        ],
        replace)


def add_private_registries(docker_json, private_registries, replace=False):
    return add_insecure_registries(docker_json, private_registries, replace)


def add_insecure_registries(docker_json, insecure_registries, replace=False):
    return append_or_relace(
        docker_json,
        'insecure-registries',
        [
            registry_netloc(registry_url)
            for insecure_registry, registry_url in
            [
                (insecure_registry, urlparse(insecure_registry['url']))
                for insecure_registry in
                insecure_registries
            ]
            if registry_url.scheme == "http" or not insecure_registry.get("ca")
        ],
        replace)
