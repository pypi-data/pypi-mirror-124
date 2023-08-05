import setuptools

with open("./README.md", "r") as fh:
    long_description = fh.read()

with open("./requirements.txt") as f:
    required = list(f.read().splitlines())

setuptools.setup(
    name="omdenalore",
    version="0.2.10",
    author="Omdena Collaborators",
    author_email="kaushal@omdena.com",
    description="AI for Good library",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://omdena.com/omdenalore/",
    install_requires=required,
    project_urls={
        "Documentation": "https://omdenaai.github.io/",
        "OmdenaLore Article": "https://omdena.com/blog/worlds-largest-ai4good-python-library-omdenalore/",  # noqa: E501
        "Apply to be a contributor": "https://airtable.com/shrue8xCVpjPvDD1g",
        "Become a partner": "https://bit.ly/omdenalore_company",
        "Join discord": "https://discord.gg/s9h7JvJzUx",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=setuptools.find_packages(),
)
