import distutils.cmd
import json
import os
from configparser import ConfigParser

import setuptools

config = ConfigParser()
config.read("setup.cfg")

# We provide extras_require parameter to setuptools.setup later which
# overwrites the extra_require section from setup.cfg. To support extra_require
# secion in setup.cfg, we load it here and merge it with the extra_require param.
extras_require = {}
if "options.extras_require" in config:
    for key, value in config["options.extras_require"].items():
        extras_require[key] = [v for v in value.split("\n") if v.strip()]

BASE_DIR = os.path.dirname(__file__)

PACKAGE_INFO = {}

VERSION_FILENAME = os.path.join(
    BASE_DIR, "src", "santolabs", "logging", "fastapi", "version.py"
)

with open(VERSION_FILENAME, encoding="utf-8") as f:
    exec(f.read(), PACKAGE_INFO)

PACKAGE_FILENAME = os.path.join(
    BASE_DIR, "src", "santolabs", "logging", "fastapi","package.py"
)

with open(PACKAGE_FILENAME, encoding="utf-8") as f:
    exec(f.read(), PACKAGE_INFO)


extras_require["framework"] = PACKAGE_INFO["_framework"]
test_deps = extras_require.get("test", [])
for dep in extras_require["framework"]:
    test_deps.append(dep)


class JSONMetadataCommand(distutils.cmd.Command):

    description = (
        "print out package metadata as JSON. This is used by OpenTelemetry dev scripts to ",
        "auto-generate code in other places",
    )
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        metadata = {
            "name": config["metadata"]["name"],
            "version": PACKAGE_INFO["__version__"],
            "framework": PACKAGE_INFO["_framework"],
        }
        print(json.dumps(metadata))

setuptools.setup(
    cmdclass={"meta": JSONMetadataCommand},
    version=PACKAGE_INFO["__version__"],
    extras_require=extras_require,
)