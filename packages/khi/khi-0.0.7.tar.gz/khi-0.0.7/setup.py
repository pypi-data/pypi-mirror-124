from setuptools import setup

setup(
        name='khi',
        version='0.0.7',
        description='Furnish information about the great Karachi city, Pakistan.',
        url='https://www.techtum.dev',
        author='siphr',
        author_email='python@techtum.dev',
        license='MIT',
        packages=['khi'],
        install_requires=['BeautifulSoup4',
                          ],

        classifiers=[
            'Development Status :: 1 - Planning',
            'Intended Audience :: Science/Research',
            'License :: OSI Approved :: MIT License',  
            'Operating System :: OS Independent',
        ],
)

