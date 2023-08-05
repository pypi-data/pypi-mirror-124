from setuptools import setup, find_packages

def readme() -> str:
    with open(r'README.md') as f:
        README = f.read()
    return README

classifiers = [
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Education',
    'Operating System :: OS Independent',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3'
]

setup(
    name='kalkulatorsd',
    version='0.0.1',
    description='ini adalah kalkulator sederhana untuk anak sd',
    long_description=readme(),
    long_description_content_type="text/markdown",
    url='',
    author='Zaafir',
    author_email='zfrhmnn@gmail.com',
    license='MIT',
    classifiers=classifiers,
    keywords=['calculator'],
    packages=find_packages(),
    install_requires=['']
)