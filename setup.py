
from setuptools import setup, find_packages


def load_requirements(path: str = "requirements.txt"):
    with open(path, encoding="utf-8") as f:
        return [ln.strip() for ln in f if ln.strip() and not ln.strip().startswith("#")]


if __name__ == "__main__":
    setup(
        name="marketflow",
        version="0.1.0",
        packages=find_packages(exclude=["tests*"]),
        install_requires=load_requirements(),
        entry_points={
            "console_scripts": [
                "marketflow=marketflow.__main__:main",
            ]
        },
        author="Your Name",
        author_email="joaoboscojbm@gmail.com",
        license="MIT",
        description="A modular, extensible Python framework for advanced Volume-Price Analysis (VPA) and Wyckoff Method analytics.",
        long_description_content_type="text/markdown",
        url="https://github.com/Martinolli/marketflow",
        classifiers=[
            "Programming Language :: Python :: 3",
            "Operating System :: OS Independent",
        ],
        python_requires=">=3.8",
    )
