from setuptools import setup, find_packages
from os import path

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name="tenor.py",
    version="0.0.1",
    description="Gif 검색 라이브러리",
    license="GPLv3",
    author="Jung Ji-Hyo",
    author_email="cord0318@gmail.com",
    long_description=long_description,
    long_description_content_type='text/markdown',
    url="https://github.com/cord0318/tenor",
    install_requires=["asyncio", "aiohttp", "aiofiles"],
    packages=find_packages(),
    keywords=["korea", "gif", "tenor", "움짤", "tenor.py"],
    python_requires=">=3",
    classifiers=[
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        #'Development Status :: 3 - Alpha',
        "Development Status :: 5 - Production/Stable",
    ],
)