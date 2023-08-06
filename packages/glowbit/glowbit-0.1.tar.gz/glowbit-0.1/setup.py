from distutils.core import setup

with open('README.md', 'r') as fh:
    long_description = fh.read()

setup (
    name = 'glowbit',
    packages = ['glowbit'],
    version = '0.1',
    license='MIT',
    description = 'Raspberry Pi (Python 3.x) and Raspberry Pi Pico (MicroPython) driver for GlowBit devices',
    long_description = 'Raspberry Pi (Python 3.x) and Raspberry Pi Pico (MicroPython) driver for GlowBit devices',
    url = 'https://github.com/CoreElectronics/CE-GlowBit-Python',
    author = 'Core Electronics',
    author_email = 'production.inbox@coreelectronics.com.au',
    classifiers = [
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: Implementation :: MicroPython',
        'License :: OSI Approved :: MIT License',
        ],        
)
