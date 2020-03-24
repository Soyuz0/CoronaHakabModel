import setuptools

from src.corona_hakab_model_data.__data__ import (
    __author__,
    __author_email__,
    __license__,
    __url__,
    __version__,
)

setuptools.setup(
    name="corona_hakab_model",
    version=__version__,
    author=__author__,
    author_email=__author_email__,
    license=__license__,
    url=__url__,
    description="a simple gdal translate/warp/addo python wrapper for raster batch processing",
    package_dir={"": "src"},
    packages=["corona_hakab_model", "corona_hakab_model_data"],
    install_requires=["numpy", "scipy", "scikit-learn"],
    extras_require={"profiling": ["yappi"],
                    "pretty graphs": ["pyside2", "matplotlib"]
                    },
    python_requires=">=3.7.0",
    include_package_data=True,
    data_files=[("", ["README.md", "LICENSE"])],
)
