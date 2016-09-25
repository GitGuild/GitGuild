from setuptools import setup

setup(
    name='gitguild',
    version='0.0.2',
    url='https://github.com/deginner/gitguild',
    license='MIT',
    author='Ira Miller',
    author_email='ira@gitguild.com',
    description='',
    packages=['gitguild'],
    install_requires=['python-gnupg',
                      'gitpython',
                      'pygithub'],
    entry_points={
        'console_scripts': [
            'gg = gitguild.gg:cli',
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
