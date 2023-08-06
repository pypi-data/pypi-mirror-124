import setuptools

long_description = open("README.md").read()
required = [""] # Comma seperated dependent libraries name

setuptools.setup(
    name="moonauth_sdk",
    version="1.0.1alpha",
    author="Dominik Gralka",
    author_email="dominik@gralka.info",
    license="Do No Harm",
    description="A Python wrapper for the Moonauth RESTful API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/moonauth/SDK-NodeJS",
    #packages = ['moonauth-sdk'],
    # project_urls is optional
    project_urls={
        "Bug Tracker": "https://github.com/moonauth/SDK-Python/issues",
    },
    key_words="moonauth, api, wrapper, moon, authentication, passwordless",
    install_requires=required,
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
)