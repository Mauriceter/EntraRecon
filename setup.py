from setuptools import setup, find_packages

setup(
    name="entrarecon",
    version="0.1.0",
    description="Entra ID / Azure reconnaissance utilities",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    author="Mauricebis",
    packages=find_packages(),
    python_requires=">=3.8",
    install_requires=[
        "requests"
    ],
    entry_points={
        "console_scripts": [
            "entrarecon=entrarecon.entrarecon:main"
        ]
    },
)