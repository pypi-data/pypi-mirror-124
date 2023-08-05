# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

if __name__ == "__main__":
  setup(
    name="save-text",
    version="1.3.1",
    description='You can save and retrieve text.',
    author='YahiroRyo',  
    author_email='YahiroRyo@users.noreply.github.com',
    url="https://github.com/YahiroRyo",
    license='MIT',
    packages=find_packages(),
    classifiers=[
      "Programming Language :: Python :: 3",
      "License :: OSI Approved :: MIT License",
      "Operating System :: OS Independent",
    ],
    entry_points={
      "console_scripts":[
        "st = save.main:main"
      ]
    }
  )