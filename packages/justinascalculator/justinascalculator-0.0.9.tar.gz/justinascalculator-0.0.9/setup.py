from setuptools import setup, find_packages

with open("README.txt", "r") as fh:
    long_description = fh.read()

setup(
    name="justinascalculator",
    version="0.0.9",
    author="Justinas Klevinskas",
    author_email="justinas@klevinskas.lt",
    description="Simple calculator",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=['pytest', 'typing'],
    python_requires='>=3.6',
)