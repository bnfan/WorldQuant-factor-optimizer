"""
WorldQuant Factor Optimizer 项目设置文件
"""

from setuptools import setup, find_packages

# 读取 README 文件
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

# 读取 requirements.txt
with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="worldquant-factor-optimizer",
    version="1.0.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="一个基于GPT-5的WorldQuant量化因子优化工具",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/your-username/worldquant-factor-optimizer",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Financial and Insurance Industry",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Office/Business :: Financial :: Investment",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "pytest-mock>=3.10.0",
            "black>=23.0.0",
            "flake8>=6.0.0",
            "isort>=5.12.0",
            "mypy>=1.0.0",
            "pre-commit>=3.0.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "worldquant-optimizer=gpt_optimizer:main",
        ],
    },
    include_package_data=True,
    package_data={
        "": ["*.txt", "*.md"],
    },
    keywords="quantitative finance, factor optimization, worldquant, gpt-5, ai, machine learning",
    project_urls={
        "Bug Reports": "https://github.com/your-username/worldquant-factor-optimizer/issues",
        "Source": "https://github.com/your-username/worldquant-factor-optimizer",
        "Documentation": "https://github.com/your-username/worldquant-factor-optimizer#readme",
    },
)
