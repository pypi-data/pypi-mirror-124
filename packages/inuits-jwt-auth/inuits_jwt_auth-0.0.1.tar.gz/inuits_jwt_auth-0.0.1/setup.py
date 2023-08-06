from distutils.core import setup

setup(
    name='inuits_jwt_auth',
    version='0.0.1',
    description="Job helper to use with the job api",
    classifiers=[
        'License :: OSI Approved :: GNU General Public License v2 (GPLv2)',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3'
    ],
    author='Matthias Dillen',
    author_email='matthias.dillen@inuits.eu',
    license='GPLv2',
    packages=[
        'inuits_jwt_auth'
    ],
    provides=['inuits_jwt_auth']
)
