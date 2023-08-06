import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="namu",
    version="0.0.1",
    author="prnm789",
    author_email="prnm789@gmail.com",
    description="한글 프로그래밍 언어 '나무'를 실행할 수 있는 패키지입니다.",
    long_description=long_description, # don't touch this, this is your README.md
    long_description_content_type="text/markdown",
    url="https://repl.it/@prnm789/namupackage",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)