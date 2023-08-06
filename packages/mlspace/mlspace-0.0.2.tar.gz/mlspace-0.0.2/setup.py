from setuptools import find_packages, setup


with open("README.md") as f:
    long_description = f.read()


if __name__ == "__main__":
    setup(
        name="mlspace",
        version="0.0.2",
        description="mlspace",
        long_description=long_description,
        long_description_content_type="text/markdown",
        author="Abhishek Thakur",
        author_email="abhishek4@gmail.com",
        url="https://github.com/abhishekkrthakur/mlspace",
        license="Apache 2.0",
        package_dir={"": "src"},
        packages=find_packages("src"),
        entry_points={"console_scripts": ["mlspace=mlspace.cli.mlspace:main"]},
        include_package_data=True,
        install_requires=["torch>=1.6.0"],
        platforms=["linux", "unix"],
        python_requires=">3.5.2",
    )
