from setuptools import setup, find_packages

setup(
    name='pygments-ket',
    version='0.1.r1',
    description='Pygments lexer for Ket.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    keywords='pygments ket lexer',
    license='Apache-2.0',

    author='Evandro Chagas Ribeiro da Rosa',
    author_email='evandro.crr@posgrad.ufsc.br',

    url='https://gitlab.com/quantum-ket/pygments-ket',

    packages=find_packages(),
    install_requires=['pygments >= 2.3.1', 'ket-lang'],

    entry_points='''[pygments.lexers]
                    ket=pygments_ket:KetLexer''',
)