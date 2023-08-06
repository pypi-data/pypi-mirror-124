"""
Описание установки
"""
# pylint: disable=all
from setuptools import setup, find_packages

"""
python -m pip install --upgrade setuptools wheel twine
python setup.py sdist bdist_wheel

python -m twine upload --repository-url https://test.pypi.org/legacy/ dist/*
python -m twine upload dist/*
export CURL_CA_BUNDLE="" && python -m twine upload --repository-url https://nexus-ci.corp.dev.vtb/repository/puos-pypi-lib/ dist/*
"""

REQUIRED = [
    'vtb-http-interaction>=0.1.3',
    'django>=3.0.0',
    'djangorestframework>=3.12.2',
    'mozilla-django-oidc==1.2.4',
    'django-lifecycle==0.8.0',
]

setup(
    name='vtb-django-utils',
    version='1.0.12',
    packages=find_packages(exclude=['tests']),
    url='https://bitbucket.region.vtb.ru/projects/PUOS/repos/vtb-django-utils',
    license='',
    author='VTB',
    author_email='',
    description='django utils for VTB projects',
    install_requires=REQUIRED,
    classifiers=[
        "Programming Language :: Python :: 3.8",
        "Framework :: Django :: 3.0",
        "Operating System :: OS Independent",
    ],
    extras_require={
        'test': [
            'pytest',
            'pytest-env',
            'pylint',
            'pytest-asyncio'
        ]
    }
)
