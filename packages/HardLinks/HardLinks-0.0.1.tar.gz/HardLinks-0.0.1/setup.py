from setuptools import setup, find_packages
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()
with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = fh.read()
setup(
    name = 'HardLinks',
    version = '0.0.1',
    author = 'Coreman14',
    author_email = '',
    license = 'Apache License 2.0',
    description = 'Make hard links for specific file types for programs that don\'t search subdirectories.',
    long_description = long_description,
    long_description_content_type = "text/markdown",
    url = 'https://gitlab.com/coreman14/hardlinks',
    py_modules = ['hard_links'],
    packages = find_packages(),
    install_requires = [requirements],
    python_requires='>=3.5',
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Operating System :: OS Independent",
    ],
    entry_points = '''
        [console_scripts]
        hardlinks=HardLinks.hard_links:main
    '''
)
