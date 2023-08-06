from setuptools import setup, find_packages

VERSION = '1.0.4'

setup(
    name='rsa_crypto',
    version=VERSION,

    description='Encrypt and decrypt data using RSA certificates.',
    url='https://github.com/Christophe-Gauge/rsa_crypto',

    long_description="""# rsa_crypto\n\nA Python 3 command-line tool and a library for encrypting and decrypting files and/or key/value pairs in a particular section of a configuration file (.ini file).\n\nThis library uses public/private RSA keys to perform the encryption.""",
    long_description_content_type='text/markdown',

    author='Christophe Gauge',
    author_email='chris@videre.us',
    license='GNU Lesser General Public License v3 (LGPLv3)',
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 4 - Beta',

        # Indicate who your project is intended for
        'Intended Audience :: Developers',
        'Topic :: Security :: Cryptography',

        # Pick your license as you wish (should match "license" above)
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
    # packages=[
    #     'rsa_crypto'
    #     ],
    py_modules=['rsa_crypto'],
    install_requires=['pycryptodome'],
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    python_requires=">=3",

    entry_points={
        'console_scripts': [
            'rsa_crypto = rsa_crypto:main'
        ]
    },

)