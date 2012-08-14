from distutils.core import setup

version = '0.0.2'

setup(
    name = 'gchart',
    url = 'https://github.com/KrzysiekJ/gchart',
    py_modules = ['gchart'],
    download_url = 'https://github.com/KrzysiekJ/gchart/tarball/{}'.format(version),
    version = version,
    author = 'Krzysztof Jurewicz',
    author_email = 'krzysztof.jurewicz@gmail.com',
    description = 'A flexible Google Chart API wrapper'
    )
