"""Setup script for HorizonNet."""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="horizonnet",
    version="1.0.0",
    author="Development Team",
    author_email="dev@horizonnet.ai",
    description="Graph Attention Network for Credit Entity Risk Assessment",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/HorizonNet",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
    ],
    python_requires=">=3.8",
    install_requires=[
        "numpy>=1.20.0",
        "pandas>=1.2.0",
        "scikit-learn>=0.24.0",
        "scipy>=1.6.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=3.0.0",
            "coverage>=6.0",
            "black>=22.0.0",
            "pylint>=2.13.0",
            "flake8>=4.0.0",
            "mypy>=0.950",
        ],
    },
)
