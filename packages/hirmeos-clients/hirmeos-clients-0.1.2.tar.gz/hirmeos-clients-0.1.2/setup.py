from setuptools import setup


with open('README.rst', 'r') as f:
    long_description = f.read()


setup(
    name='hirmeos-clients',
    version='0.1.2',
    author='Rowan Hatherley',
    author_email='rowan.hatherley@ubiquitypress.com',
    description='Python API clients for the HIRMEOS project.',
    install_requires=[
        'requests==2.25.1',
        'PyJWT==2.1.0',
    ],
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://gitlab.com/ubiquitypress/hirmeos-clients/',
    packages=['hirmeos_clients'],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
    ],
    python_requires='>=3.7'
)
