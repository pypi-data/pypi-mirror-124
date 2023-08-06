import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

packages = [ 
  "covidstats"
]

setuptools.setup(
    name="covid-stats",
    version="0.0.1",
    author="Bruce",
    packages=packages,
    author_email="brucealt69@gmail.com",
    description="A way to get covid-19 stats using worldometers.info",
    long_description=long_description,
    long_description_content_type="text/markdown",
    project_urls={
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requres= [
      "BeautifulSoup4",
      "requests"
    ]
)