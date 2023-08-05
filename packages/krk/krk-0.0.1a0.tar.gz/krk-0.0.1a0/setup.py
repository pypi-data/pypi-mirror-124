from setuptools import setup, find_packages
import os

here = os.path.abspath(os.path.dirname(__file__))

with open("README.md") as f:
    readme = f.read()

with open("LICENSE") as f:
    license = f.read()

DESCRIPTION = "A command-line utility for all krk projects"
LONG_DESCRIPTION = "A command-line utility for all krk projects."
URL = "https://github.com/krakakai/krk"
PROJECT_URLS = {
    "Bug Tracker": "https://github.com/krakakai/krk/issues",
}


def local_scheme(version):
    return ""


# Setting up
setup(
    name="krk",
    author="Stan Verschuuren",
    author_email="delangstenerdopaarde@gmail.com",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    url=URL,
    project_urls=PROJECT_URLS,
    install_requires=[],
    keywords=["krk", "robotics"],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ],
    entry_points={
        "console_scripts": [
            "krk=krk.cli:main",
        ],
    },
    zip_safe=False,
    package_dir={"": "krakakai"},
    packages=find_packages(where="krakakai", exclude=["docs", "tests*"]),
    extras_require={
        "test": ["coverage", "pytest", "pytest-cov"],
    },
    use_scm_version={"local_scheme": local_scheme},
    setup_requires=["setuptools_scm"],
    python_requires=">=3.6",
    include_package_data=True,
)
