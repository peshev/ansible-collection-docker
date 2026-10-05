import pytest
from jinja2 import Undefined

from plugins.filter.docker_images import (
    normalize_docker_image,
)

@pytest.mark.parametrize(
    "image, default_pull_policy, expected",
    [
        (
            "nginx:latest",
            "not_present",
            {
                "image": {
                    "registry": None,
                    "namespace": None,
                    "repository": "nginx",
                    "tag": "latest",
                },
                "pull": "not_present",
            },
        ),
        (
            "docker.io/library/nginx:1.27",
            "always",
            {
                "image": {
                    "registry": "docker.io",
                    "namespace": "library",
                    "repository": "nginx",
                    "tag": "1.27",
                },
                "pull": "always",
            },
        ),
        (
            "registry.example.com:5000/foo/bar:latest",
            "not_present",
            {
                "image": {
                    "registry": "registry.example.com:5000",
                    "namespace": "foo",
                    "repository": "bar",
                    "tag": "latest",
                },
                "pull": "not_present",
            },
        ),
    ],
)
def test_normalize_docker_image_string(
    image,
    default_pull_policy,
    expected,
):
    assert normalize_docker_image(image, default_pull_policy) == expected


@pytest.mark.parametrize(
    "image",
    [
        {"name": "nginx:latest"},
        {"image": "nginx:latest"},
    ],
)
def test_normalize_docker_image_accepts_name_or_image(image):
    result = normalize_docker_image(image)

    assert result == {
        "image": {
            "registry": None,
            "namespace": None,
            "repository": "nginx",
            "tag": "latest",
        },
        "pull": "not_present",
    }


@pytest.mark.parametrize(
    "property_name, value, expected",
    [
        ("pull", "always", "always"),
        ("pull_policy", "always", "always"),
        ("imagePullPolicy", "Always", "always"),
        ("pull_policy", "not_present", "not_present"),
        ("pull_policy", "if_not_present", "not_present"),
        ("pull_policy", "missing", "not_present"),
        ("imagePullPolicy", "IfNotPresent", "not_present"),
        ("pull_policy", "never", None),
        ("imagePullPolicy", "Never", None),
    ],
)
def test_normalize_docker_image_pull_policy(
    property_name,
    value,
    expected,
):
    result = normalize_docker_image({
        "name": "nginx",
        property_name: value,
    })

    assert result["pull"] == expected


def test_normalize_docker_image_pull_takes_precedence_over_pull_policy():
    result = normalize_docker_image({
        "name": "nginx",
        "pull": "always",
        "pull_policy": "never",
        "imagePullPolicy": "Never",
    })

    assert result["pull"] == "always"


def test_normalize_docker_image_pull_policy_takes_precedence_over_image_pull_policy():
    result = normalize_docker_image({
        "name": "nginx",
        "pull_policy": "always",
        "imagePullPolicy": "Never",
    })

    assert result["pull"] == "always"


def test_normalize_docker_image_name_takes_precedence_over_image():
    result = normalize_docker_image({
        "name": "nginx:1",
        "image": "nginx:2",
    })

    assert result["image"]["tag"] == "1"


def test_normalize_docker_image_build_string():
    result = normalize_docker_image({
        "name": "example:latest",
        "pull_policy": "build",
        "build": "./src",
    })

    assert result == {
        "image": {
            "registry": None,
            "namespace": None,
            "repository": "example",
            "tag": "latest",
        },
        "pull": "build",
        "build": {
            "context": "./src",
        },
    }


def test_normalize_docker_image_build_dict():
    result = normalize_docker_image({
        "name": "example:latest",
        "pull_policy": "build",
        "build": {
            "context": "./src",
            "dockerfile": "Dockerfile.custom",
            "args": [
                "FOO=bar",
                "BAZ=qux",
            ],
            "labels": {
                "com.example.foo": "bar",
            },
            "pull": True,
        },
    })

    assert result["pull"] == "build"
    assert result["build"] == {
        "context": "./src",
        "dockerfile": "Dockerfile.custom",
        "args": {
            "FOO": "bar",
            "BAZ": "qux",
        },
        "labels": {
            "com.example.foo": "bar",
        },
        "pull": True,
    }


def test_normalize_docker_image_build_none_values_become_undefined():
    result = normalize_docker_image({
        "name": "example",
        "pull_policy": "build",
        "build": {
            "context": ".",
            "dockerfile": None,
        },
    })

    assert result["build"]["context"] == "."
    assert isinstance(result["build"]["dockerfile"], Undefined)


def test_normalize_docker_image_missing_name():
    image = {
        "pull_policy": "always",
    }

    with pytest.raises(
        Exception,
        match=r"No image name found",
    ):
        normalize_docker_image(image)


def test_normalize_docker_image_build_policy_requires_build():
    with pytest.raises(
        Exception,
        match=r"nginx has a pull_policy of 'build' but no build property",
    ):
        normalize_docker_image({
            "name": "nginx",
            "pull_policy": "build",
        })


def test_normalize_docker_image_invalid_pull_policy():
    with pytest.raises(KeyError):
        normalize_docker_image({
            "name": "nginx",
            "pull_policy": "sometimes",
        })


def test_normalize_docker_image_invalid_build_type():
    with pytest.raises(
        Exception,
        match=r"Unexpected value for build property: 123",
    ):
        normalize_docker_image({
            "name": "example",
            "pull_policy": "build",
            "build": 123,
        })


def test_normalize_docker_image_unknown_build_property():
    with pytest.raises(
        Exception,
        match=r"Unexpected property: unsupported",
    ):
        normalize_docker_image({
            "name": "example",
            "pull_policy": "build",
            "build": {
                "context": ".",
                "unsupported": "foo",
            },
        })


def test_normalize_docker_image_build_context_is_required():
    with pytest.raises(
        Exception,
        match=r"context is required, but missing",
    ):
        normalize_docker_image({
            "name": "example",
            "pull_policy": "build",
            "build": {
                "context": None,
            },
        })


def test_normalize_docker_image_invalid_build_network():
    with pytest.raises(
        Exception,
        match=r"Value for network is invalid",
    ):
        normalize_docker_image({
            "name": "example",
            "pull_policy": "build",
            "build": {
                "context": ".",
                "network": "invalid",
            },
        })