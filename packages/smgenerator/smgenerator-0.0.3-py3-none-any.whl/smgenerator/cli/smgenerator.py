"""
 * Copyright (C) 2021 - Simone G. Riva
 * Distributed under the terms of the GNU General Public License (GPL)
 * This file is part of SMGen.

 * SMGen is a free software; you can redistribute it and/or modify
 * it under the terms of the GNU General Public License v3.0 as published by
 * the Free Software Foundation.
  
 * SMGen is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
 * See the GNU General Public License for more details.
"""

import warnings
warnings.simplefilter(action='ignore')

import argparse
import sys
from subprocess import *
import os


def getArgs():
	parser = argparse.ArgumentParser(add_help=False)
	parser.add_argument('--n_process', help='Number of processes', nargs='?', default=1, type=int)
	args = vars(parser.parse_args())
	return args

def check_parameters(x):
	if x <= 0:
		print("n_process must be a positive integer")
		exit(-1)
	elif x == 2:
		print("n_process should be ==1 or >=3")
		exit(-2)
	elif x >= 3:
		try:
			import mpi4py
			mpy_v = mpi4py.__version__
			if mpy_v < '3.1.0':
				print("mpi4py must be greater then '3.1.0'")
				exit(-3)
		except:
			print("Please install mpi4py greater then '3.1.0'")
			exit(-4)

def main():
	path = os.path.join(os.path.dirname(__file__)).split(os.sep+'cli')[0]
	f = open(path+os.sep+"_version.py", "r")
	v = f.readline().split('"')[-2]
	print("* SMGen (v.%s): Synthetic Models of biological systems Generator"%v)
	
	args = getArgs()
	check_parameters(args["n_process"])

	if args['n_process'] == 1:
		command = ["python3",  path+os.sep+"SMGen_one.py"]
	else:
		command = ["mpiexec", "-np", str(args['n_process']), "python3", path+os.sep+"SMGen_multi.py"]
	call(command) 

if __name__ == '__main__':
	main()
