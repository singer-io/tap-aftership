
from setuptools import setup, find_packages


setup(name="tap-aftership",
      version="0.0.1",
      description="Singer.io tap for extracting data from aftership API",
      author="Stitch",
      url="http://singer.io",
      classifiers=["Programming Language :: Python :: 3 :: Only"],
      py_modules=["tap_aftership"],
      install_requires=[
        "singer-python==6.1.1",
        "requests==2.32.4",
        "backoff==2.2.1",
      ],
      extras_require={
        "dev": [
          "parameterized",
        ],
      },
      entry_points="""
          [console_scripts]
          tap-aftership=tap_aftership:main
      """,
      packages=find_packages(),
      package_data = {
          "tap_aftership": ["schemas/*.json"],
      },
      include_package_data=True,
)
