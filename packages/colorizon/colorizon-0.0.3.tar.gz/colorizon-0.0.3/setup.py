from setuptools import setup
import re

version = '0.0.3'

readme = ''
with open('README.rst') as f:
    readme = f.read()

packages = [
    'colorizon',
]

setup(name='colorizon',
      author='Felipe Savazi',
      author_email="dev@felipesavazi.com",
      url='https://github.com/FelipeSavazii/Colorizon',
      project_urls={
        "Documentation": "https://github.com/FelipeSavazii/Colorizon#documentation",
        "Issue tracker": "https://github.com/FelipeSavazii/Colorizon/issues",
      },
      version=version,
      packages=packages,
      license='MIT',
      description='A small library to make it easy to use colors in Python',
      long_description=readme,
      long_description_content_type="text/x-rst",
      include_package_data=True,
      python_requires='>=3.8.0',
      classifiers=[
        'Development Status :: 5 - Production/Stable',
        'License :: OSI Approved :: MIT License',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
      ]
)
