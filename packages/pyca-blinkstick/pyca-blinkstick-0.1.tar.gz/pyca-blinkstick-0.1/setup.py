from setuptools import setup, find_packages
import os

path = os.path.abspath(os.path.dirname(__file__))


def read(filename):
    with open(os.path.join(path, filename), encoding='utf-8') as f:
        return f.read()


setup(
    name="pyca-blinkstick",
    version="0.1",
    description="Blinkstick recording light integration with opencast pyca capture agent",
    author="Kristof Keppens",
    author_email='kristof.keppens@ugent.be',
    license="MIT",
    url="https://github.com/mm-dict/pyca-blinkstick",
    long_description=read('README.rst'),
    long_description_content_type='text/x-rst',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "BlinkStick==1.2.0",
        "certifi==2021.10.8",
        "charset-normalizer==2.0.7",
        "configobj==5.0.6",
        "idna==3.3",
        "nose==1.3.7",
        "pyusb==1.2.1",
        "requests==2.26.0",
        "sdnotify==0.3.2",
        "six==1.16.0",
        "urllib3==1.26.7"
    ],
    entry_points={
        'console_scripts': [
            'pyca_blinkstick = pyca_blinkstick.__main__:main'
        ]
    },
    test_suite="tests",
)
