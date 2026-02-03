"""
Setup configuration for Sentiment Portfolio Optimization System.

This script enables installation of the package using:
    pip install -e .
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="sentiment-portfolio-optimizer",
    version="1.0.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="A sentiment-driven portfolio optimization system integrating NLP and quantitative finance",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/sentiport",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Financial and Insurance Industry",
        "Intended Audience :: Developers",
        "Topic :: Office/Business :: Financial :: Investment",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    install_requires=[
        "pandas>=2.0.0",
        "numpy>=1.24.0",
        "scipy>=1.10.0",
        "scikit-learn>=1.3.0",
        "yfinance>=0.2.30",
        "nltk>=3.8",
        "textblob>=0.17.0",
        "matplotlib>=3.7.0",
        "seaborn>=0.12.0",
        "plotly>=5.0.0",
        "pyyaml>=6.0",
        "tqdm>=4.65.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0",
            "pytest-cov>=4.0",
            "black>=23.0",
            "flake8>=6.0",
            "pylint>=3.0",
            "sphinx>=7.0",
        ],
        "notebook": [
            "jupyter>=1.0",
            "jupyterlab>=4.0",
            "ipython>=8.0",
        ],
        "dashboard": [
            "streamlit>=1.28",
            "dash>=2.14",
        ],
    },
    entry_points={
        "console_scripts": [
            "sentiport=src.utils.config_loader:setup_config",
        ],
    },
    include_package_data=True,
    zip_safe=False,
)
