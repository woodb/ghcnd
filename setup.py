from setuptools import setup, find_packages

setup(
    name="ghcnd",
    version="0.1.0",
    description="Global Historical Climatology Network (GHCN) daily parser",
    url="https://github.com/woodb/ghcnd",
    author="Brandon Wood",
    author_email="btwood@geometeor.com",
    license="BSD",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
    ],
    keywords="global historical climatology network",
    packages=find_packages(exclude=["contrib", "docs", "tests*"]),
    install_requires=["pandas>=0.11.0"],
)
