import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="smpl2", # Replace with your own username
    version="0.1.0",
    author="dfb159",
    author_email="jSigrist@web.de",
    description="simple plotting and fitting and simulation",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/dfb159/smpl2",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    install_requires = [
        "uncertainties",
        "numpy",
        "matplotlib",
        "scipy",
        "sympy"
        #"requests",
        #"tqdm",
        #"pandas",
    ],
    python_requires='>=3.6',
)
