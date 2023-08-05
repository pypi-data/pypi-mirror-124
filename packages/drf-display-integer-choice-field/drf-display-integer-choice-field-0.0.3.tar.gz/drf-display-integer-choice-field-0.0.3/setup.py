from pathlib import Path

import setuptools

import drf_display_integer_choice_field

readme_file = Path('.').parent / 'README.md'
if not readme_file.exists():
    long_description = ''
else:
    with open("README.md", "r", encoding="utf-8") as file:
        long_description = file.read()

setuptools.setup(
    name="drf-display-integer-choice-field",
    version=drf_display_integer_choice_field.__version__,
    author=drf_display_integer_choice_field.__author__,
    author_email=drf_display_integer_choice_field.__email__,
    description="django rest framework choice field, which display label, instead of value",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/panhaoyu/drf-display-integer-choice-field",
    project_urls={
        "Bug Tracker": "https://github.com/panhaoyu/drf-display-integer-choice-field/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=setuptools.find_packages(exclude=['demo*']),
    python_requires=">=3.8",
)
