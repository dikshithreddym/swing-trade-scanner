from setuptools import setup, find_packages

setup(
    name="swing-trade-scanner",
    version="1.0.0",
    author="Dikshith Reddy",
    author_email="dikshithreddymacherla@gmail.com",
    description="Intelligent swing trading opportunity scanner for S&P 500 stocks",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/dikshithreddym/swing-trade-scanner",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Financial and Insurance Industry",
        "Topic :: Office/Business :: Financial :: Investment",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: MIT License",
    ],
    python_requires=">=3.8",
    install_requires=[
        "yfinance>=0.2.28",
        "pandas>=2.0.0",
        "numpy>=1.24.0",
        "ta>=0.11.0",
        "requests>=2.31.0",
        "schedule>=1.2.0",
        "tqdm>=4.66.0",
        "python-dotenv>=1.0.0",
        "click>=8.1.0",
        "colorama>=0.4.6",
    ],
    entry_points={
        "console_scripts": [
            "swing-scanner=swing_scanner.cli:cli",
        ],
    },
)