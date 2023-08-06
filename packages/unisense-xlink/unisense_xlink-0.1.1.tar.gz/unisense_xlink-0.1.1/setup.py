#!/usr/bin/env python3

import os
import re
import shutil
import sys

from setuptools import find_packages, setup


def read(f):
    return open(f, "r", encoding="utf-8").read()


def get_version(package):
    """
    Retuen package version as listed in `__version__` in `init.py`.
    """
    init_py = open(os.path.join(package, "__init__.py")).read()
    return re.search("__version__ = ['\"]([^'\"]+)['\"]", init_py).group(1)


version = get_version("unisense_xlink")

if sys.argv[-1] == "publish":
    if os.system("pip freeze | grep twine"):
        print("Twine is not installed.\nUse `pip install twine`.\nExiting.")
        sys.exit()
    if os.system("pip list | grep wheel"):
        print("Wheel is not installed.\nUse `pip install wheel`.\nExiting.")
        sys.exit()
    os.system("python setup.py sdist bdist_wheel")
    print("You probably want to also tag the version now:")
    print("  git tag -a v%s -m 'version %s'" % (version, version))
    print("  git push --tags")
    shutil.rmtree("dist")
    shutil.rmtree("build")
    shutil.rmtree("unisense_xlink.egg-info")
    sys.exit()

if sys.argv[-1] == "git":
    cmd = "git tag -a v%s -m 'version %s'" % (version, version)
    os.system(cmd)
    os.system("git push --tags")
    x = input("Push new version to Github? (y/n)")
    if x == "y":
        os.system("git add .")
        cmd = "git commit -m 'version %s'" % (version)
        os.system(cmd)
        b = input("which branch to push? (default: master)")
        g_cmd = f"git branch | grep {b}"
        g = os.system(g_cmd)
        if b == "":
            os.system("git push origin master")
        elif g is not None:
            cmd = f"git push origin {b}"
            os.system(cmd)
    sys.exit()

# 'setup.py publish' shortcut.
if sys.argv[-1] == 'upload':
    os.system('python setup.py sdist')
    os.system('twine upload dist/*')
    os.system('rm -rf dist')
    os.system('rm -rf *.egg-info')
    sys.exit()

setup(
    name="unisense_xlink",
    version=version,
    url="https://github.com/AzatAI/unisense_xlink",
    license="AzatAI Licence",
    description="Connect and setup AzatAI django projects, made easy.",
    long_description=read("README.md"),
    author="AzatAI",
    author_email="info@azat.ai",
    packages=find_packages(exclude=["tests*"]),
    include_package_data=True,
    install_requires=[
        'Adafruit-Blinka',
        'adafruit-circuitpython-bno055',
        'adafruit-circuitpython-busdevice',
        'adafruit-circuitpython-register',
        'Adafruit-GPIO',
        'Adafruit-PlatformDetect',
        'Adafruit-PureIO',
        'bme680',
        'pyusb',
        'PyYAML',
        'regex',
        'rpi-ws281x',
        'RPi.GPIO',
        'shellingham',
        'smbus',
        'smbus2',
        'typing-extensions',
        'Werkzeug',
        'zipp',
        'SI1145'
    ],
    python_requires=">=3.6",
    zip_safe=False,
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3 :: Only",
        "Topic :: Internet :: WWW/HTTP",
    ],
    project_urls={
        "Official": "https://azat.ai",
        "Source": "https://github.com/AzatAI/unisense_xlink",
    },
)
