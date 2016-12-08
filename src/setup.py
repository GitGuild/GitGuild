from setuptools import setup

setup(
    name='gitguild-cli',
    version='0.0.2.2.2',
    url='https://github.com/gitguild/gitguild',
    license='MIT',
    author='Ira Miller',
    author_email='ira@gitguild.com',
    description='A helper for git project standards and governance.',
    packages=['gitguild'],
    install_requires=['python-gnupg',
                      'gitpython',
                      'pygithub'],
    entry_points={
        'console_scripts': [
            'gitguild = gitguild.command:cli',
        ],
    },
    classifiers=[
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ]
)
