import pathlib

from setuptools import setup, find_packages

# Setting up
setup(
    name="zipmanager",
    version='0.2.1',
    license="MIT",
    author="SimplePythonCoder",
    author_email="",
    url='https://github.com/SimplePythonCoder/zipmanager',
    description='Allows you to manage zip folders as data',
    long_description=pathlib.Path('README.md').read_text(),
    long_description_content_type="text/markdown",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[],
    keywords=['zip'],
    python_requires='>=3.11',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3.11',
        'Operating System :: Microsoft :: Windows',
        'Topic :: Utilities',
    ],
    project_urls={
        'Source': 'https://github.com/SimplePythonCoder/zipmanager',
        'Issues': 'https://github.com/SimplePythonCoder/zipmanager/issues'
    }
)