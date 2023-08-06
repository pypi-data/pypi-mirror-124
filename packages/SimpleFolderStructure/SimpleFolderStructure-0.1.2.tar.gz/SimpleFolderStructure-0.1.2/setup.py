from setuptools import setup, find_packages
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()
with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = fh.read()
setup(
    name = 'SimpleFolderStructure',
    version = '0.1.2',
    author = 'Coreman14',
    author_email = '',
    license = 'Apache License 2.0',
    description = 'Create folder structures from files',
    long_description = long_description,
    long_description_content_type = "text/markdown",
    url = 'https://gitlab.com/coreman14/folder-generation-python',
    py_modules = ['folder_structure', 'generate_folder_structure', 'create_folder_structure'],
    packages = find_packages(),
    install_requires = [requirements],
    python_requires='>=3.10',
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.10",
        "Operating System :: OS Independent",
    ],
    entry_points = '''
        [console_scripts]
        folderstructure=FolderStructure.folder_structure:main
    '''
)
