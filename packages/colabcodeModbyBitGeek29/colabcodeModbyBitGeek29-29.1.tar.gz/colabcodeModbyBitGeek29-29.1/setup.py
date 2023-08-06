from setuptools import Extension, find_packages, setup


with open("README.md") as f:
    long_description = f.read()


if __name__ == "__main__":
    setup(
        name="colabcodeModbyBitGeek29",
        scripts=["scripts/colabcode"],
        version="29.1",
        description="Mod version of ColabCode",
        long_description=long_description,
        long_description_content_type="text/markdown",
        author="Lufi Porndre",
        author_email="porndrelufi@gmail.com",
        license="MIT License",
        packages=find_packages(),
        include_package_data=True,
        install_requires=[
            "pyngrok>=5.0.0",
            "nest_asyncio==1.4.3",
            "uvicorn==0.13.1",
            "jupyterlab==3.0.7",
        ],
        platforms=["linux", "unix"],
        python_requires=">3.5.2",
    )
