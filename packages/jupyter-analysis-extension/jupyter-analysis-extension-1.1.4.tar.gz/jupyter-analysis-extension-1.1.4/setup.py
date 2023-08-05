# Optional file
# Dynamic metadata: possibly non-deterministic. Any items that are dynamic or determined at install-time,
# as well as extension modules or extensions to setuptools, need to go into setup.py.
# Static metadata should be preferred and dynamic metadata should be used only as an escape hatch when absolutely necessary.

import setuptools

setuptools.setup()

"""
import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="jupyter-analysis-extension",
    version="0.0.1",
    author="Kyoungjun Park",
    author_email="parkkjun525@gmail.com",
    description="A Jupyter Extension for Data Analysis",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/KyoungjunPark/ipywidget_statistics",
    project_urls={
        "Bug Tracker": "https://github.com/KyoungjunPark/ipywidget_statistics/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GPL-3.0",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
)
"""