import setuptools

with open("README.md", "r") as fh:
  long_description = fh.read()

setuptools.setup(
  name="slightwind",
  version="0.0.1",
  author="Slightwind",
  author_email="am473ur@gmail.com",
  description="Some commonly used functions.",
  long_description=long_description,
  long_description_content_type="text/markdown",
  url="",
  packages=setuptools.find_packages(),
  classifiers=[
  "Programming Language :: Python :: 3",
  ],
)