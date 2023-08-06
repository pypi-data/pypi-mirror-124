import setuptools

setuptools.setup(
    name='amoapi',
    version="0.0.1",

    url='https://github.com/Raevsky-Team/amoapi',
    author='Mihail Granovskij',
    author_email='mihail.granovskij@gmail.com',

    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
    install_requires=['requests',
                      'PyJWT == 2.1.0',
                      'python-dotenv'],

)
