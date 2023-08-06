try:
    from setuptools import setup, find_packages
except ImportError:
    from distutils.core import setup


def get_requirements():
    """Parse all packages mentioned in the 'requirements.txt' file."""
    with open("requirements.txt") as file_stream:
        return file_stream.read().splitlines()


setup(
    name="container-ci-suite",
    description='A python3 container CI tool for testing images.',
    version="0.0.1",
    keywords='tool,containers,images,tests',
    packages=find_packages(exclude=["tests"]),
    url="https://github.com/phracek/container-ci-suite",
    license="MIT",
    author="Petr Hracek",
    author_email="phracek@redhat.com",
    install_requires=get_requirements(),
    scripts=[],
    setup_requires=[],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python',
        'Topic :: Software Development',
    ],
)
