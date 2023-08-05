from distutils.core import setup

setup(
    name='gcm_common',
    packages=['gcm_common'],
    version='0.1.5',
    license='MIT',
    description='GCM common package',
    author='Batkhishig Dulamsurankhor',
    author_email='batkhishign55@gmail.com',
    url='https://github.com/batkhishign55/gcm_common',
    download_url='https://github.com/batkhishign55/gcm_common/archive/refs/tags/v_0.1.5.tar.gz',
    keywords=['gcm', 'common'],
    install_requires=[
        'flask',
        'PyYAML',
    ],
    classifiers=[  # Optional
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 3 - Alpha',

        # Indicate who your project is intended for
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',

        # Pick your license as you wish
        'License :: OSI Approved :: MIT License',

        'Programming Language :: Python :: 3.6',
    ],
)
