from setuptools import find_packages, setup

with open("README.md") as f:
    long_description = f.read()

INSTALL_REQUIRES = [
    "optuna>=2.10.0",
    "xgboost>=1.5.0",
]

if __name__ == "__main__":
    setup(
        name="autoxgb",
        version="0.0.2",
        description="autoxgb: tune xgboost with optuna",
        long_description=long_description,
        long_description_content_type="text/markdown",
        author="Abhishek Thakur",
        author_email="abhishek4@gmail.com",
        url="https://github.com/abhishekkrthakur/autoxgb",
        license="Apache License",
        packages=find_packages(),
        install_requires=INSTALL_REQUIRES,
        platforms=["linux", "unix"],
        python_requires=">3.5.2",
    )
