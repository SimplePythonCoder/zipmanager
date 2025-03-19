import pathlib

from setuptools import setup, find_packages

# Setting up
setup(
    name="zipmanager",
    version='0.5.2',
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
    keywords=['zip', 'zipfile'],
    python_requires='>=3.11',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3.11',
        'Operating System :: Microsoft :: Windows :: Windows 10',
        'Topic :: Utilities',
    ],
    project_urls={
        'Source': 'https://github.com/SimplePythonCoder/zipmanager',
        'Changelog': 'https://github.com/SimplePythonCoder/zipmanager/blob/main/CHANGELOG.md',
        'Documentation': 'https://github.com/SimplePythonCoder/zipmanager/wiki',
        'Issues': 'https://github.com/SimplePythonCoder/zipmanager/issues'
    }
)
