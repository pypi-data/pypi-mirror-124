import json
import setuptools

kwargs = json.loads(
    """
{
    "name": "prowler-sdk-poc",
    "version": "0.0.1",
    "description": "prowler-sdk-poc",
    "license": "Apache-2.0",
    "url": "https://github.com/mmuller88/prowler-sdk-poc",
    "long_description_content_type": "text/markdown",
    "author": "Martin Mueller<damadden88@googlemail.com>",
    "bdist_wheel": {
        "universal": true
    },
    "project_urls": {
        "Source": "https://github.com/mmuller88/prowler-sdk-poc"
    },
    "package_dir": {
        "": "src"
    },
    "packages": [
        "prowler_sdk_poc",
        "prowler_sdk_poc._jsii"
    ],
    "package_data": {
        "prowler_sdk_poc._jsii": [
            "prowler-sdk-poc@0.0.1.jsii.tgz"
        ],
        "prowler_sdk_poc": [
            "py.typed"
        ]
    },
    "python_requires": ">=3.6",
    "install_requires": [
        "jsii>=1.40.0, <2.0.0",
        "publication>=0.0.3"
    ],
    "classifiers": [
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: JavaScript",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Typing :: Typed",
        "Development Status :: 5 - Production/Stable",
        "License :: OSI Approved"
    ],
    "scripts": []
}
"""
)

with open("README.md", encoding="utf8") as fp:
    kwargs["long_description"] = fp.read()


setuptools.setup(**kwargs)
