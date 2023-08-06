from pathlib import Path

import setuptools

import django_admin_object_button

package = django_admin_object_button
name = 'django-admin-object-button'
description = "Add button to django admin rows."
readme_file = Path('.').parent / 'README.md'
if not readme_file.exists():
    long_description = ''
else:
    with open("README.md", "r", encoding="utf-8") as file:
        long_description = file.read()

setuptools.setup(
    name=name,
    version=package.__version__,
    author=package.__author__,
    author_email=package.__email__,
    description=description,
    long_description=long_description,
    long_description_content_type="text/markdown",
    url=f"https://github.com/panhaoyu/{name}",
    project_urls={
        "Bug Tracker": f"https://github.com/panhaoyu/{name}/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=setuptools.find_packages(exclude=['demo*']),
    python_requires=">=3.8",
)
