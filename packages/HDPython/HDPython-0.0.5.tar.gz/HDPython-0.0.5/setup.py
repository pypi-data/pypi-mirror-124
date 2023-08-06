import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="HDPython", # Replace with your own username
    version="0.0.5",
    author="Richard Peschke",
    author_email="rp40@hawaii.edu",
    description="High Level Object Oriented Hardware Description Library",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/HardwareDesignWithPython/HDPython",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
          'pyvcd',
    ],
    python_requires='>=3.8',
)
