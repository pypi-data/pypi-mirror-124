from setuptools import find_packages, setup

classifiers = [
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Education',
    'Operating System :: Microsoft :: Windows :: Windows 10',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3'
]

setup(
    name='zeroone-ai',
    version='0.0.3',
    description='With this package you can make an simple AI that can predict a zero or a one.',
    long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
    url='https://github.com/MathijsTak/ZeroOneAi',
    author='MathijsTak',
    author_email='mathijs.tak@outlook.com',
    license='MIT',
    classifiers=classifiers,
    keywords='zeroone zero one ai zerooneai zeroai oneai zeroone-ai',
    packages=find_packages(),
    install_requires=[
        'numpy',
        'pandas',
        'matplotlib',
        'sklearn'
    ]
)