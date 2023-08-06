"""The setup script."""

from setuptools import find_packages, setup

with open('README.rst') as readme_file:
    readme = readme_file.read()

requirements = [
    'Click>=8.0',
    'pandas>=1.3.1',
    'tqdm>=4.62.0',
    'sqlalchemy>=1.4.22',
    'sqlalchemy_utils>=0.37.8',
    'pymysql==1.0.2',
    'requests==2.26.0',
    'xmltodict',
    'cryptography',
]

setup_requirements = ['pytest-runner']

test_requirements = ['pytest>=3']

setup(
    author="Bruce Schultz",
    author_email='bruce.schultz@scai.fraunhofer.de',
    python_requires='>=3.7',
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
    description="Package for generating a relational database of GEO derived information.",
    entry_points={
        'console_scripts': [
            'aop2db=aop2db.cli:main',
        ],
    },
    install_requires=requirements,
    license="MIT license",
    include_package_data=True,
    keywords='aop2db',
    name='aop2db',
    packages=find_packages(include=['aop2db', 'aop2db.*']),
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/brucetony/aop2db',
    version='0.1.1',
    zip_safe=False,
)
