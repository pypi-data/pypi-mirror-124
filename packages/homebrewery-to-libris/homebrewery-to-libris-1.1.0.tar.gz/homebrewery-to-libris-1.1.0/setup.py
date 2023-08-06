from setuptools import setup
setup(
    name='homebrewery-to-libris',
    version='1.1.0',
    description='Converter between homebrewery and libris markdown formats.',
    url='https://github.com/lazy-scrivener-games/homebrewery-to-libris',
    download_url='https://github.com/lazy-scrivener-games/homebrewery-to-libris/archive/refs/tags/v1.1.tar.gz',
    author='Chris Muller',
    author_email='chris@lazyscrivenergames.com',
    keywords=[
        'utility',
        'pdf',
        'html',
        'markdown',
        'conversion',
        'book',
        'roleplaying',
        'game',
        'homebrewery',
        'libris'
    ],
    license='MIT',
    packages=[
        'homebrewery_to_libris'
    ],
    scripts=[
        'scripts/homebrewery-to-libris'
    ],
    install_requires=[
        'markdown2 == 2.4.1'
    ],
        classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: End Users/Desktop',
        'Topic :: Text Processing :: Markup :: Markdown',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9'
    ]
)
