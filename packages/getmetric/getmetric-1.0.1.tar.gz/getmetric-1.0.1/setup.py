import setuptools


setuptools.setup(name='getmetric',
                 version='1.0.1',
                 description='Getmetric python package',
                 long_description=open('README.md').read().strip(),
                 long_description_content_type="text/markdown",
                 author='Alex Turkovskii',
                 author_email='darkertb@gmail.com',
                 url='https://github.com/getmetric/python',
                 py_modules=['getmetric'],
                 install_requires=[],
                 license='MIT License',
                 packages=['getmetric'],
                 zip_safe=False,
                 keywords='getmetric package',
                 classifiers=[
                     "Programming Language :: Python :: 2",
                     "Programming Language :: Python :: 3",
                     "License :: OSI Approved :: MIT License",
                     "Operating System :: OS Independent",
                 ])
