import setuptools


def get_version():
    with open('src/flake8_escaping_style.py') as f:
        lines = [line.strip() for line in f if line.startswith('__version__')]

    for line in lines:
        _, versionstr = line.split('=', 1)
        return versionstr.strip(' "\'')

    raise Exception("__version__ not found in src/flake8_escaping_style.py")


with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()


setuptools.setup(
    name="flake8-escaping-style",
    license="MIT",
    version=get_version(),
    description="A flake8 plugin to use consistent escaping style in string or bytes literals",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Baptiste Mispelon",
    author_email="bmispelon@gmail.com",
    url="https://github.com/bmispelon/flake8-escaping-style",
    project_urls={
        "Bug Tracker": "https://github.com/bmispelon/flake8-escaping-style/issues",
    },
    package_dir = {'': 'src'},
    py_modules=["flake8_escaping_style"],
    python_requires='>=3.7',
    install_requires=[
        "flake8 > 3.0.0",
    ],
    entry_points={
        'flake8.extension': [
            'ESC = flake8_escaping_style:Plugin',
        ],
    },
    classifiers=[
        "Framework :: Flake8",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Software Development :: Quality Assurance",
    ],
)
