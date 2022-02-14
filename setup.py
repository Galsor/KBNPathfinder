from setuptools import setup, find_packages

setup(
  name="KBNPathfinder",
  version="0.0.1",
  long_description=open("README.md", "r", encoding="utf-8").read(),
  long_description_content_type="text/markdown",
  keywords="Knapsack problem graph geographical optimisation",
  license="MIT",
  package_dir={"": "KBNPathfinder"},
  packages=find_packages("KBNPathfinder"),
  python_requires=">=3.8.0",
)