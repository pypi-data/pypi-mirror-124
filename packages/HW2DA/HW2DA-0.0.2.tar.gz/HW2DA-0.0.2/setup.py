import setuptools
from setuptools import setup

setup(
    name='HW2DA',
    version='0.0.2',
    description='Package for HW 2',
    author='Eugene Gusarov',
    author_email='gen05@yandex-team.ru',
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
    install_requires=[
        'numpy>=1.16',
        'matplotlib',
    ]
)
