from setuptools import setup, find_packages

setup(
    name='google_flights_scraper',
    version='0.1.0',
    author='Hugo Gonçalves',
    author_email='hugoglvs@icloud.com',
    description='A Python package to scrape flight data from Google Flights.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/yourusername/google_flights_scraper',
    packages=find_packages(),
    keywords=['google flights scraper', 'google flights', 'flights scraper', 'flights'],
    include_package_data=True,
    install_requires=[
        'playwright==1.17.0',
        'selectolax==0.2.12',
        'click==7.1.2'
    ],
    entry_points={
        'console_scripts': [
            'google-flights=flights_cli:main',
        ],
    },
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.8',
)
