from setuptools import setup, find_packages

setup(
    name="spreadsheet_intelligence",  # パッケージ名
    version="0.1.0",  # バージョン
    author="Shue Shiinoki, Galirage, Inc.",
    author_email="shue.shiinoki@galirage.com",
    description="A package for spreadsheet data loader to process with LLM",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/galirage/gg-knowledge-base",  # GitHubリポジトリなど
    packages=find_packages(exclude=["tests*", "tests"]),
    include_package_data=True,
    install_requires=["toml"],
    python_requires=">=3.10",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
