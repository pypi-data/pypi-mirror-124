from setuptools import setup, find_packages

with open("README.md") as f:
    long_description = f.read()


if __name__ == "__main__":
    setup(
        name="colabshell",
        entry_points={"console_scripts": ["colabshell=colabshell.cli:main"]},
        version="0.1.0",
        description="ColabShell - Run shell on Colab/Kaggle notebook!",
        long_description=long_description,
        long_description_content_type="text/markdown",
        author="Sandip Dey",
        author_email="sandip.dey1988@yahoo.com",
        url="https://github.com/sandyz1000/colabshell",
        license="MIT License",
        packages=find_packages(include=['colabshell']),
        include_package_data=True,
        install_requires=[
            "pyngrok",
            "pgrok @ git+https://github.com/sandyz1000/pgrok-py.git#egg=pgrok-0.1.0",
            "kafka_logging_handler @ git+https://github.com/sandyz1000/kafka-logging-handler.git#egg=kafka_logging_handler",
            "gdrivefs @ git+https://github.com/sandyz1000/GDriveFS.git#egg=gdrivefs",
        ],
        platforms=["linux", "unix"],
        python_requires=">=3.5",
    )
