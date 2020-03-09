import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="amd-util",
    version="0.1.0",
    description="A Python utility library.",
    author="Aaron",
    author_email="adrenberg@gmail.com",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3 :: Only",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    include_package_data=True,
    install_requires=[
        "flask>=1.0.2",
        "flatten-json>=0.1.6",
        "jsonschema[format]>=3.0.1",
        "prometheus_client>=0.6.0",
        "prometheus_flask_exporter>=0.7.3",
        "pytz>=2019.1",
    ],
    license="MIT",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_namespace_packages(exclude=["test"]),
    url="https://github.com/no-decaf/amd-pyutils",
    tests_require=["pytest>=4.4.1", "pytest-cov>=2.7.1"],
)
