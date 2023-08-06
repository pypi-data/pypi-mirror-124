from distutils.core import setup

setup(
    name = 'pygendata',
    packages = ['pygendata'],
    version = '0.1.0',
    license = 'MIT',
    description = 'data generation library supports multiple input/output file types',
    author = 'Lucas Padden',
    author_email='lucaspadden@gmail.com',
    url = 'https://github.com/Dynee/pygendata',
    download_url = 'https://github.com/Dynee/pygendata/archive/refs/tags/v0.0.1.tar.gz',
    keywords=['python', 'data generation'],
    install_requires=[
        'faker'
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8'
    ]
)