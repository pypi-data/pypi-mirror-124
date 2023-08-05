from os import system, rename
from os.path import basename
from shutil import rmtree
from pathlib import Path
from glob import glob
from setuptools import setup, find_packages
from distutils.cmd import Command


with open('README', 'r', encoding='utf-8') as fh:
    long_description = fh.read()


class DocsCmd(Command):
    '''Command for building the docs.'''
    user_options = []

    def initialize_options(self):  # must override
        pass

    def finalize_options(self):  # must override
        pass

    def run(self):
        '''Builds the docs.'''
        system('cd src/p3d_flatpak; python -m pydoc -w ./ ; cd ../..')
        rmtree('docs', ignore_errors=True)
        Path('docs').mkdir(exist_ok=True)
        [rename(fname, 'docs/' + basename(fname))
         for fname in glob('src/p3d_flatpak/*.html')]


if __name__ == '__main__':
    setup(
        name='panda3d-flatpak',
        version='0.1.0',
        author='Flavio Calva',
        author_email='f.calva@gmail.com',
        description='Flatpak support for Panda3D',
        long_description=long_description,
        long_description_content_type='text/plain',
        url='http://www.ya2tech.it/pages/panda3d-flatpak.html',
        project_urls={
            'Repository': 'http://git.ya2tech.it/?p=panda3d-flatpak.git',
            'Docs': 'http://docs.ya2tech.it/p3d_flatpak/p3d_flatpak.html',
            'Issues': 'http://www.ya2tech.it/issues',
            'Patches': 'http://lists.ya2tech.it/p3d-flatpak/listinfo.html',
            'Mailing list': 'http://lists.ya2tech.it/p3d-flatpak/listinfo.html'},
        classifiers=[
            'Programming Language :: Python :: 3',
            'License :: OSI Approved :: BSD License',
            'Operating System :: POSIX :: Linux'],
        package_dir={'': 'src'},
        packages=find_packages(where='src'),
        python_requires='>=3.8',
        cmdclass={'docs': DocsCmd})
