import setuptools

with open("README.md", "r") as f:
    long_description = f.read()

INSTALL_REQUIRES = [
    'pandas',
    'dataclasses',
    'arrow',
    'xarray',
    'bs4',
    'tqdm',
    'pvlib'
]

setuptools.setup(
    name="pv60hz",
    version="0.0.4",
    author="JiHyeong Seo",
    author_email="it-admins@60hz.io",
    description="PV Forecast simulation",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/60hz-io/pv60hz",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Intended Audience :: Science/Research",
    ],
    python_requires=">=3.6",
    install_requires=INSTALL_REQUIRES
)
