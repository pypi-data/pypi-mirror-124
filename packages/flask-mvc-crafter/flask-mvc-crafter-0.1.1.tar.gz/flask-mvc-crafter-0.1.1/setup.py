from setuptools import setup, find_packages
with open('README.md') as f:
    long_description = f.read()

setup(
    name = 'flask-mvc-crafter',
    version = '0.1.1',
    url = 'https://github.com/rdp-jr/crafter',
    download_url = 'https://github.com/rdp-jr/crafter/archive/refs/tags/0.1.1.tar.gz',
    author = 'Obee Principio',
    author_email = 'rdprincipio.jr@gmail.com',
    description = 'A CLI tool for the FlaskMVC Starter Kit',
    long_description=long_description,
    long_description_content_type='text/markdown',
    py_modules = ['main', 'crafter'],
    packages=find_packages(),
    install_requires = ['Click',
        'inflect'],
    classifiers=[
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    entry_points={
        'console_scripts': [
            'crafter = main:cli'
        ]
    },
    include_package_data=True,
    package_data={'': ['templates/*.tpl']},
    

)