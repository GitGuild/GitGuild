from setuptools import setup

setup(
    name='gitguild',
    version='0.0.0',
    url='https://github.com/deginner/gitguild',
    license='MIT',
    author='Ira Miller',
    author_email='ira@deginner.com',
    description='',
    packages=['gitguild'],
    package_data={'gitguild': ['template/medieval/charter.md',
                               'template/medieval/contracts/*.md',
                               'template/software/charter.md',
                               'template/software/contracts/*.md',
                               ]},
    install_requires=['click', 'python-gnupg'],
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

