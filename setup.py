from setuptools import setup, find_packages

setup(
    name="matools",
    version="0.0.1",
    packages=find_packages(),
    url="https://github.com/rafikurnia/matools",
    license="Apache License 2.0",
    author="Rafi Kurnia Putra",
    author_email="rafi.putra@traveloka.com",
    description="tools to automate scaffolding resources setup processes.",
    install_requires=[
        "boto3",
        "pyyaml",
    ],
    package_data={
        "matools": ["templates/*.yml"],
    },
    include_package_data=True,
    python_requires=">=2.7,<3",
    entry_points={
        "console_scripts": [
            "matools=matools.main:main"
        ],
    }
)
