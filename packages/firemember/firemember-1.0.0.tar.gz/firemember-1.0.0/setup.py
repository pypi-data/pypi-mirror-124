from setuptools import find_packages, setup

setup(
    name='firemember',
    packages=find_packages(include=['firemember']),
    version='1.0.0',
    description='Lisensi aplikasi menggunakan realtime database dari firebase',
    author='santo',
    author_email='santo.lpu@gmail.com',
    url='https://github.com/snja/firemember',
    license='MIT',
    install_requires=['pycryptodome', 'requests'],
    setup_requires=['pytest-runner'],
    tests_require=['pytest'],
    test_suite='test',
)
