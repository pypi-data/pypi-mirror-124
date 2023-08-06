""" setup.py : Script for FindSim """
__author__      = "HarshaRani"
__copyright__   = "Copyright 2021 HillTau, NCBS"
__maintainer__  = "HarshaRani"
__email__       = "hrani@ncbs.res.in"

import os
import sys
import setuptools
from setuptools import setup, Extension
from setuptools.command.build_ext import build_ext
import subprocess

DIR = os.path.abspath(os.path.dirname(__file__))

class git_clone_external(build_ext):
	def run(self):
		pybindDir = DIR+'/extern/pybind11/'
		subprocess.check_call(['git', 'clone', 'https://github.com/pybind/pybind11',pybindDir])
		build_ext.run(self)


setuptools.setup(
		name="HillTau",
		description="A fast, compact abstraction for model reduction in biochemical signaling networks",
		version="1.0",
		author= "Upinder S. Bhalla",
		author_email="bhalla@ncbs.res.in",
		maintainer= "HarshaRani",
		email= "hrani@ncbs.res.in",
		long_description = open('README.md', encoding='utf-8').read(),
		long_description_content_type='text/markdown',
		packages=["HillTau","HillTau.CppCode"],
		package_dir={'HillTau': "."},
		cmdclass = {'build_ext': git_clone_external},    
		ext_modules=[Extension('ht', ['CppCode/htbind.cpp','CppCode/ht.cpp'], include_dirs=['extern/pybind11/include','extern/exprtk'])],
		install_requires = ['numpy','matplotlib','simpleSBML','scipy'],
		# Make sure to include the `#egg` portion so the `install_requires` recognizes the package
		#'git+ssh://git@github.com/pybind/pybind11.git#egg=ExampleRepo-0.1'],
		url ="http://github.com/Bhallalab/HillTau",
		#headers = ['extern/pybind11/include/pybind11/'],
		package_data = {"HillTau" : ['CppCode/*','extern/exprtk/*','Examples/*/*']},
		license="GPLv3",
		entry_points = {
		'console_scripts' : [ 'HillTau = HillTau.__main__:run',
					   'Hilltau = HillTau.__main__:run',
					   'hillTau = HillTau.__main__:run',
					   'hilltau = HillTau.__main__:run',
					   'htgraph = HillTau.__main__:run_htgraph',
					   'ht2sbml = HillTau.__main__:run_ht2sbml',
					   'mash    = HillTau.__main__:run_mash',
				   ]
			},
		)

