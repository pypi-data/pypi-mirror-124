import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="smpl2", # Replace with your own username
    setup_requires=['setuptools-git-versioning'],
    version="0.0.1",
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
    version_config={
        "template": "{tag}",
        "dev_template": "{tag}.{ccount}",
        "dirty_template": "{tag}.{ccount}+dirty",
        "starting_version": "0.0.0",
        "version_callback": None,
        "version_file": None,
        "count_commits_from_version_file": False
    },
    python_requires='>=3.6',
)
