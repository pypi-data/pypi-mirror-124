import os
from setuptools import setup, find_packages


def read(file_name):
    return open(os.path.join(os.path.dirname(__file__), file_name)).read()


setup(
    name='grebarss',
    version='1.0.2',
    author='Alexander Hreben',
    url='https://github.com/Greba3000/Homework',
    author_email='greba3000@gmail.com',
    description="CLI utility for reading news",
    keyword="CLI reader news",
    packages=find_packages(),  # packages=['rss_reader', 'tests']
    longdescription=read('README.md'),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Topic :: Utilities",
        'Environment :: Console',
    ],
    #install_requires=read('requirements.txt'),
    #package_dir={"": "rss_reader"},
    python_requires=">=3.9",
    entry_points={
        "console_scripts": ["grebarss=rss_reader.rss_reader:main"],
    },
)
