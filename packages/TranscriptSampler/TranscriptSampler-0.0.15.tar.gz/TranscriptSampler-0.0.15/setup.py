from setuptools import setup, find_packages

setup(
    name='TranscriptSampler',
    url='https://gitlab.com/noepozzan/programming-life-sciences.git',
    author='Noè Pozzan',
    author_email='noe.pozzan@stud.unibas.ch',
    description='sample transcripts',
    entry_points = {
        'console_scripts': ['TranscriptSampler=TranscriptSampler.cli:write_sample'],
    },
    license='MIT',
    version='0.0.15',
    #packages=find_packages(),
    packages=["TranscriptSampler"],
    package_dir={
        "": ".",
        "TranscriptSampler": "./TranscriptSampler",
    },
    install_requires=[
        "click"
    ]
)