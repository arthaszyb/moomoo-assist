from setuptools import setup, find_packages

setup(
    name="moomoo-assist",
    version="0.1",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    install_requires=[
        "futu-api>=7.1.3308",
        "PyYAML>=5.4.1",
        "requests>=2.26.0",
        "TA-Lib>=0.4.24",
    ],
    extras_require={
        "dev": [
            "pytest>=6.2.0",
            "pytest-cov>=2.12.0",
        ],
    },
    python_requires=">=3.8",
) 