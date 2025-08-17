
from setuptools import setup, find_packages


def load_requirements(path: str = "requirements.txt"):
    try:
        with open(path, encoding="utf-8") as f:
            lines = [ln.strip() for ln in f if ln.strip() and not ln.strip().startswith("#")]
        return lines
    except Exception:
        # Fallback to a minimal core set if requirements.txt is unavailable
        return [
            "pandas",
            "numpy",
            "requests",
            "python-dotenv",
            "polygon-api-client==1.14.6",
        ]


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
    description="A modular, extensible Python framework for advanced Volume-Price Analysis (VPA) and Wyckoff Method analytics.",
    long_description_content_type="text/markdown",
    url="https://github.com/Martinolli/marketflow",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
)
