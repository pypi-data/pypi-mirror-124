from distutils.core import setup
setup(
    name = 'RawCord',
    packages = ['RawCord'],
    version = '0.1',
    license='MIT',
    description = 'Discord API Wrapper',
    author = 'FishballNoodles',
    author_email = 'joelkhorxw@gmail.com',
    url = 'https://github.com/TheReaper62/RawCord',
    download_url = 'https://github.com/TheReaper62/RawCord/archive/refs/tags/v0.1.tar.gz',
    keywords = ['discord','discord api','discord api wrapper','discord wrapper','discord bot','discord gateway'],
    install_requires= [
        'requests',
        'websocket_client'
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    long_description = "Main purpose is to make my own bots but free to use if you want to use it. No guranteed quality."
)
