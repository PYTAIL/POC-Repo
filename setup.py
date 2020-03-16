from setuptools import setup

from poc_repo import __version__

setup(
    name="POC_Repo",
    version=__version__,
    author="PIQE Libraries Team",
    author_email="amacmurr@redhat.com",
    description="PIQE Libraries Proof of Concept.",
    url="https://github.com/piqe-test-libraries/POC-Repo.git",
    packages=setuptools.find_packages(),
    install_requires=[
        "openshift",
        "pytest-dependency",
        "pytest-xdist",
        "glusto@git+git://github.com/loadtheaccumulator/glusto.git"
        "@python3_port4#egg=glusto"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GPLv3 License",
    ],
)
