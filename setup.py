from setuptools import setup, find_packages

setup(
    name="someone-ai",
    version="1.0.0",
    description="Someone AI - Your Personal Assistant",
    author="Your Name",
    packages=find_packages(),
    install_requires=[
        "requests>=2.31.0",
        "python-dotenv>=1.0.0"
    ],
    entry_points={
        "console_scripts": [
            "someone=someone.cli:main",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
)
