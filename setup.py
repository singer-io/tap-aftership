
from setuptools import setup, find_packages


setup(name="tap-aftership",
      version="0.0.2",
      description="Singer.io tap for extracting data from aftership API",
      author="Stitch",
      url="http://singer.io",
      classifiers=["Programming Language :: Python :: 3 :: Only"],
      py_modules=["tap_aftership"],
      install_requires=[
        "singer-python==6.1.1",
        "requests==2.33.0",
        "backoff==2.2.1",
        "parameterized"
      ],
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
