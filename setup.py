from setuptools import setup, find_packages

with open('README.md') as f:
    readme = f.read()

setup(
    name='awesomely_complex_machines',
    version='0.0',
    description='Implementation of a profit maximizer for a ficticious company ACM.',
    long_description=readme,
    author='QLR',
    author_email='quentin.leroux@edhec.com',
    url='',
    packages=find_packages(exclude=('tests', 'docs')),
    setup_requires=[],
    license='None',
    classifiers=[
        'Intended Audience :: Recruiters',
        'Programming Language :: Python',
        'Operating System :: Linux',
        'Topic :: Assignment'
    ],
)
