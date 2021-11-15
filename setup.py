from setuptools import setup, find_packages

setup(
    name='teether',
    version='0.1.9',
    packages=find_packages(),
    install_requires=[
        'z3-solver==4.8.5.0',
        'pysha3>=1.0.2',
        'web3==5.23.1'
    ],
    scripts=[
        'bin/asm.py',
        'bin/extract_contract_code.py',
        'bin/gen_exploit.py',
        'bin/plot_cfg.py',
        'bin/replay_exploit.py',
    ],
    url='https://github.com/nescio007/teether',
    python_requires='>=3.7',
    license='Apache 2.0',
    author='Johannes Krupp',
    author_email='johannes.krupp@cispa.saarland',
    description='Analysis and automatic exploitation framework for Ethereum smart contracts'
)
