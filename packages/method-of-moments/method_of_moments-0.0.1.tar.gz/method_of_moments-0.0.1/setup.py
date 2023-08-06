import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

requirements = [
    "math_round_af==1.0.2",
    "pretty-repr==1.0.1",
    "pylint-af==1.0.1",
    "scipy==1.7.1",
]

setuptools.setup(
    name="method_of_moments",
    version="0.0.1",
    author="Albert Farkhutdinov",
    author_email="albertfarhutdinov@gmail.com",
    description=(
        "The package that allows you to work with probability distributions "
        "with a specified mean values and variances."
    ),
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/AlbertFarkhutdinov/method_of_moments",
    packages=setuptools.find_packages(),
    install_requires=requirements,
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Programming Language :: Python :: 3.9",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
