import setuptools

with open("README.md", "r") as fh:
  long_description = fh.read()

setuptools.setup(
  name="amd_pyutils",
  version="0.1.0",
  description="General Python utils.",

  author="Aaron",
  author_email="adrenberg@gmail.com",
  classifiers=[
    "Development Status :: 4 - Beta",
    "Intended Audience :: Developers",
    "License :: OSI Approved :: MIT License",
    "Natural Language :: English",
    "Operating System :: OS Independent",
    "Programming Language :: Python",
    "Topic :: Software Development :: Libraries :: Python Modules"
  ],
  include_package_data=True,
  install_requires=["flatten-json>=0.1.6"],
  license="MIT",
  long_description=long_description,
  long_description_content_type="text/markdown",
  packages=setuptools.find_packages(),
  url="https://bitbucket.org/adrenberg/amd-pyutils",
  tests_require=["pytest"]
)
