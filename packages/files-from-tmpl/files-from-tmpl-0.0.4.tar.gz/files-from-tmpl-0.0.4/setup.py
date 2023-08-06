from setuptools import setup


with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()


setup(
    name="files-from-tmpl",
    version="0.0.4",
    author="inerject",
    author_email="kumbalup@gmail.com",
    description="Generating files from template",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url=" https://github.com/inerject/files-from-tmpl",
    install_requires=[
        "Jinja2==3.0.2",
    ],
    license="GNU GPLv3",
    classifiers=[
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
    ],
    packages=["files_from_tmpl"],
)
