from setuptools import setup, find_packages

setup(
    name="midiff",
    version="1.0.0",
    setup_requires=['setuptools_scm'],
    use_scm_version=True,
    packages=find_packages(),
    include_package_data=True,
    entry_points={'console_scripts': ['midiff=midiff.__main__:main']}
)