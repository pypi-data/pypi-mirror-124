import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="work-os-ipython-magic",
    version="0.0.5",
    author="dyzfromyt",
    author_email="dyzfromyt@gmail.com",
    description="Work OS IPython Custom Magic",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/dyzfromyt/work_os_ipython_magic",
    project_urls={
        "Bug Tracker": "https://github.com/dyzfromyt/work_os_ipython_magic/issues",
    },
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Framework :: IPython",
        "Framework :: Jupyter",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
    install_requires=[
        'pyyaml',
    ],
)