import os

import relman
import setuptools


BASEPATH = os.path.abspath(os.path.dirname(__file__))


def load_requirements(filename):
    """load requirements from a pip requirements file."""
    lineiter = (line.strip()
                for line in open(os.path.join(BASEPATH, filename)))
    return [line for line in lineiter if line and not line.startswith("#")]


setuptools.setup(
    name="relmanager",
    version=relman.__version__,
    description="Release manager",
    long_description='Release manager - Automation Toolkit',
    classifiers=[
        "Topic :: Software Development :: Build Tools",
        "Topic :: Software Development :: Documentation",
        "Development Status :: 4 - Beta",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python",
        "License :: Public Domain",
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators"
    ],
    keywords="jira confluence python",
    author="David Lapsley, Alex Chan",
    author_email="dlapsley@cisco.com, alexc2@cisco.com",
    url="http://www.cisco.com",
    license="ASL",
    packages=setuptools.find_packages(exclude=["tests"]),
    include_package_data=True,
    data_files=[
        ('etc', ['etc/sample.cfg']),
    ],
    zip_safe=False,
    install_requires=load_requirements("requirements.txt"),
    test_suite="tests",
    entry_points={
        "console_scripts": [
            "relman = relman.main:run"
        ]
    }
)
