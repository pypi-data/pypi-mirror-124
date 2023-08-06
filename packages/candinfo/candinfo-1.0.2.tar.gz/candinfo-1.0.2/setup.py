import setuptools

setuptools.setup(
    name="candinfo",
    packages = ['candinfo'],
    version="1.0.2",
    license='MIT',
    author="kangyoolee",
    author_email="me@kangyoo.kr",
    description="Korea Candidate Unofficial API Wrapper",
    url="https://github.com/kangyoolee/candinfo",
    download_url = 'https://github.com/kangyoolee/candinfo/blob/main/dist/candinfo-1.0.1.tar.gz',
    long_description=open('README.md').read(), 
    install_requires=['requests','xmltodict'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
    ]
)