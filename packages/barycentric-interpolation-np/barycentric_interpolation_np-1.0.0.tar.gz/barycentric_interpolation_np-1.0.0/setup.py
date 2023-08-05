from setuptools import setup

setup(
    name='barycentric_interpolation_np',
    version='1.0.0',
    description='A example Python package',
    url='https://3vilwind.com',
    author='Nikolai Rakov',
    author_email='thrash@3vilwind.com',
    license='MIT',
    packages=['barycentric_interpolation_np'],
    install_requires=['numpy==1.21.2'],

    classifiers=[
        'Development Status :: 1 - Planning',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
)