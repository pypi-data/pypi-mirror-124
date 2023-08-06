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
warnings.filterwarnings("ignore")

from PyQt5 import QtCore, QtGui, QtWidgets, uic
from PyQt5.QtWidgets import QWidget, QMessageBox, QFileDialog
from PyQt5.QtGui import QCursor
from PyQt5.QtCore import Qt
from PyQt5.QtGui import *
from pylab import *
from numpy import *
from math import *
from libsbml import *
import random
import networkx as nx
import matplotlib.pyplot as plt
import math
import numpy as np
import os
import os.path
import time
import sys
import csv
import xml
import shutil
import configparser
import string
from os.path import expanduser

WORKTAG = 0
DIETAG = 1
REACTIVATE = 2

global g
g = []
global f
f = []
global h
h = []

class MyWindow(QtWidgets.QMainWindow):
	
	def __init__(self):
		super(MyWindow, self).__init__()
		path = os.path.join(os.path.dirname(__file__)).split('/smgenerator')[0]
		uic.loadUi(path+os.sep+'smgenerator/data/gui.ui', self)		
		self.show()

	def __disable_boxes(self):
		self.n_species.setEnabled(False)
		self.n_reaction.setEnabled(False)
		self.maximum_order_reactions.setEnabled(False)
		self.maximum_number_products.setEnabled(False)
		self.initial_amounts_distribution.setEnabled(False)
		self.initial_min.setEnabled(False)
		self.initial_max.setEnabled(False)
		self.mu_initial.setEnabled(False)
		self.sigma_initial.setEnabled(False)
		self.mu_initial.setEnabled(False)
		self.sigma_initial.setEnabled(False)
		self.kinetic_parameters_distribution.setEnabled(False)
		self.kinetic_min.setEnabled(False)
		self.kinetic_max.setEnabled(False)
		self.mu_kinetic.setEnabled(False)
		self.sigma_kinetic.setEnabled(False)
		self.mu_kinetic.setEnabled(False)
		self.sigma_kinetic.setEnabled(False)
		self.quantity.setEnabled(False)
		self.concentration.setEnabled(False)
		self.generateBioSimWare.setEnabled(False)
		self.generateSBML.setEnabled(False)
		self.n_networks.setEnabled(False)
		self.generate_networks.setEnabled(False)

	def __enable_boxes(self, activation=True):
		self.n_species.setEnabled(activation)
		self.n_reaction.setEnabled(activation)
		self.maximum_order_reactions.setEnabled(activation)
		self.maximum_number_products.setEnabled(activation)
		self.initial_amounts_distribution.setEnabled(activation)
		self.initial_min.setEnabled(activation)
		self.initial_max.setEnabled(activation)
		self.mu_initial.setEnabled(activation)
		self.sigma_initial.setEnabled(activation)
		self.mu_initial.setEnabled(activation)
		self.sigma_initial.setEnabled(activation)
		self.kinetic_parameters_distribution.setEnabled(activation)
		self.kinetic_min.setEnabled(activation)
		self.kinetic_max.setEnabled(activation)
		self.mu_kinetic.setEnabled(activation)
		self.sigma_kinetic.setEnabled(activation)
		self.mu_kinetic.setEnabled(activation)
		self.sigma_kinetic.setEnabled(activation)
		self.quantity.setEnabled(activation)
		self.concentration.setEnabled(activation)
		self.generateBioSimWare.setEnabled(activation)
		self.generateSBML.setEnabled(activation)
		self.n_networks.setEnabled(activation)
		self.generate_networks.setEnabled(activation)

	def actNew(self):

		w = QWidget()
		result = QMessageBox.question(w, 'Message', "Create new model?", QMessageBox.No | QMessageBox.Yes)
		if result == QMessageBox.Yes:
			self.n_species.setValue(2)
			self.n_reaction.setValue(1) 
			self.maximum_order_reactions.setValue(2) 
			self.maximum_number_products.setValue(2) 
			self.initial_amounts_distribution.setCurrentIndex(0) 
			self.initial_min.setText('0') 
			self.initial_max.setText('0')
			self.mu_initial.setText('0')
			self.sigma_initial.setText('0')
			self.mu_initial.setEnabled(False)
			self.sigma_initial.setEnabled(False)
			self.kinetic_parameters_distribution.setCurrentIndex(0)
			self.kinetic_min.setText('0')
			self.kinetic_max.setText('0')
			self.mu_kinetic.setText('0')
			self.sigma_kinetic.setText('0')
			self.mu_kinetic.setEnabled(False)
			self.sigma_kinetic.setEnabled(False)	
			self.quantity.setChecked(False)
			self.concentration.setChecked(True) 
			self.generateBioSimWare.setChecked(False)
			self.generateSBML.setChecked(False)
			self.n_networks.setValue(1)
			self.generate_networks.setEnabled(False)
		else:
			pass
		QWidget.setWindowTitle(self, 'SMGen')

	def actLoad(self):
		check = False
		try:
			if QWidget.windowTitle(self) == 'SMGen':
				w = QWidget()
				result = QMessageBox.question(w, 'Warning', "Do you want to upload without saving?", QMessageBox.No | QMessageBox.Yes)
				if result == QMessageBox.No:
					raise Exception('quit')
			if h == []:
				loadFile = QFileDialog.getOpenFileName(None, 'Select File', expanduser("~"), '*.ini')[0]
				if loadFile == '':
					raise Exception('quit')
				h.append(loadFile)
			else:
				loadFile = QFileDialog.getOpenFileName(None, 'Select File', expanduser(str(h[0])), '*.ini')[0]
				if loadFile == '':
					raise Exception('quit')
		except Exception as err:
				if err == 'quit': pass
				else: pass

		try:
			config = configparser.ConfigParser()
			config.read(str(loadFile))

			config.get('Model', 'Nspecies')
			config.get('Model', 'Nreactions')
			config.get('Model', 'MaxOrderReactions')
			config.get('Model', 'MaxNumberOfProducts')

			config.get('Model', 'InitialAmountDistribution')
			config.get('Model', 'MinIAD')
			config.get('Model', 'MaxIAD')
			config.get('Model', 'muIAD')
			config.get('Model', 'sigmaIAD')

			config.get('Model', 'KineticParametersDistribution')
			config.get('Model', 'MinKPD')
			config.get('Model', 'MaxKPD')
			config.get('Model', 'muKPD')
			config.get('Model', 'sigmaKPD')

			config.get('Model', 'ConcentrationIAD*')
			config.get('Model', 'QuantityIAD*')

			config.get('Model', 'GenerateSBML*')
			config.get('Model', 'Nnetworks')
			
			self.n_species.setValue(int(config.get('Model', 'Nspecies')))
			self.n_reaction.setValue(int(config.get('Model', 'Nreactions'))) 
			self.maximum_order_reactions.setValue(int(config.get('Model', 'MaxOrderReactions'))) 
			self.maximum_number_products.setValue(int(config.get('Model', 'MaxNumberOfProducts'))) 

			self.initial_amounts_distribution.setCurrentIndex(int(config.get('Model', 'InitialAmountDistribution')))
			self.initial_min.setText(config.get('Model', 'MinIAD')) 
			self.initial_max.setText(config.get('Model', 'MaxIAD'))
			self.mu_initial.setText(config.get('Model', 'muIAD'))
			self.sigma_initial.setText(config.get('Model', 'sigmaIAD'))
			
			if int(config.get('Model', 'InitialAmountDistribution')) == 1 or int(config.get('Model', 'InitialAmountDistribution')) == 3:
				self.mu_initial.setEnabled(True)
				self.sigma_initial.setEnabled(True)
			else:
				self.mu_initial.setEnabled(False)
				self.sigma_initial.setEnabled(False)
			
			self.kinetic_parameters_distribution.setCurrentIndex(int(config.get('Model', 'KineticParametersDistribution')))
			self.kinetic_min.setText(config.get('Model', 'MinKPD'))
			self.kinetic_max.setText(config.get('Model', 'MaxKPD'))
			self.mu_kinetic.setText(config.get('Model', 'muKPD'))
			self.sigma_kinetic.setText(config.get('Model', 'sigmaKPD'))
			
			if int(config.get('Model', 'KineticParametersDistribution')) == 1 or int(config.get('Model', 'KineticParametersDistribution')) == 3:
				self.mu_kinetic.setEnabled(True)
				self.sigma_kinetic.setEnabled(True)
			else:
				self.mu_kinetic.setEnabled(False)
				self.sigma_kinetic.setEnabled(False)
			
			if config.get('Model', 'ConcentrationIAD*') == 'True':
				self.concentration.setChecked(bool(config.get('Model', 'ConcentrationIAD*')))
			if config.get('Model', 'QuantityIAD*') == 'True':
				self.quantity.setChecked(bool(config.get('Model', 'QuantityIAD*')))
			
			self.generateSBML.setChecked(bool(config.get('Model', 'GenerateBioSimWare*')))
			self.generateSBML.setChecked(bool(config.get('Model', 'GenerateSBML*')))
			self.n_networks.setValue(int(config.get('Model', 'Nnetworks')))
			check = True

		except: 
			if check == True:
				w = QWidget()
				result = QMessageBox.question(w, 'Warning', "Incompatible model", QMessageBox.Ok)
			pass
		QWidget.setWindowTitle(self, 'SMGen')

	def actSave(self):
		w = QWidget()
		result = QMessageBox.question(w, 'Message', "Do you want save this model?", QMessageBox.No | QMessageBox.Yes)
		if result == QMessageBox.Yes:

			try:
				if f == []:
					saveFile = QFileDialog.getSaveFileName(None, 'Select Directory', expanduser("~"))[0]
					if saveFile == '':
						raise Exception('quit')
					f.append(saveFile)
				else:
					saveFile = QFileDialog.getSaveFileName(None, 'Select Directory', expanduser(str(f[0])))[0]
					if saveFile == '':
						raise Exception('quit')	
			
				if os.path.exists(saveFile+'.ini') == True:
					w = QWidget()
					result = QMessageBox.question(w, 'Warning', "Existing file, overwrite?", QMessageBox.No | QMessageBox.Yes)
					if result == QMessageBox.No:
						raise Exception('quit')
			except Exception as err:
				if err == 'quit': pass
				else: pass
				
			Config = configparser.ConfigParser()
			cfgfile = open(saveFile+'.ini','w')
						
			section = 'Model'
			Config.add_section(section)
			Config.set(section, 'Nspecies', str(self.n_species.value()))
			Config.set(section, 'Nreactions', str(self.n_reaction.value()))
			Config.set(section, 'MaxOrderReactions', str(self.maximum_order_reactions.value()))
			Config.set(section, 'MaxNumberOfProducts', str(self.maximum_number_products.value()))
			
			Config.set(section, 'InitialAmountDistribution', str(self.initial_amounts_distribution.currentIndex()))
			Config.set(section, 'MinIAD', str(self.initial_min.text()))
			Config.set(section, 'MaxIAD', str(self.initial_max.text()))
			Config.set(section, 'muIAD', str(self.mu_initial.text()))
			Config.set(section, 'sigmaIAD', str(self.sigma_initial.text()))
			Config.set(section, 'muIAD*', str(self.mu_initial.isEnabled()))
			Config.set(section, 'sigmaIAD*', str(self.sigma_initial.isEnabled()))
			
			Config.set(section, 'KineticParametersDistribution', str(self.kinetic_parameters_distribution.currentIndex()))
			Config.set(section, 'MinKPD', str(self.kinetic_min.text()))
			Config.set(section, 'MaxKPD', str(self.kinetic_max.text()))
			Config.set(section, 'muKPD', str(self.mu_kinetic.text()))
			Config.set(section, 'sigmaKPD', str(self.sigma_kinetic.text()))
			Config.set(section, 'muKPD*', str(self.mu_initial.isEnabled()))
			Config.set(section, 'sigmaKPD*', str(self.sigma_initial.isEnabled()))
			
			Config.set(section, 'QuantityIAD*', str(self.quantity.isChecked()))
			Config.set(section, 'ConcentrationIAD*', str(self.concentration.isChecked()))
			Config.set(section, 'GenerateBioSimWare*', str(self.generateBioSimWare.isChecked()))
			Config.set(section, 'GenerateSBML*', str(self.generateSBML.isChecked()))
			Config.set(section, 'Nnetworks', str(self.n_networks.value()))

			Config.write(cfgfile)
			cfgfile.close()

			QWidget.setWindowTitle(self, 'SMGen')

	def actExit(self):
		w = QWidget()
		result = QMessageBox.question(w, 'Message', "Sure to close the window?", QMessageBox.No | QMessageBox.Yes)
		if result == QMessageBox.Yes:
			self.close()
		else: pass

	def change_n_species(self): 
		QWidget.setWindowTitle(self, 'SMGen *')

	def change_n_reaction(self):
		QWidget.setWindowTitle(self, 'SMGen *')

	def change_maximum_order_reactions(self):
		QWidget.setWindowTitle(self, 'SMGen *')

	def change_maximum_number_products(self):
		QWidget.setWindowTitle(self, 'SMGen *')
	
	def select_initial_amounts_distribution(self):
		if self.initial_amounts_distribution.currentText() == "Normal" or self.initial_amounts_distribution.currentText() == "Log normal":
			self.mu_initial.setEnabled(True)
			self.sigma_initial.setEnabled(True)
		else:
			self.mu_initial.setEnabled(False)
			self.sigma_initial.setEnabled(False)
		QWidget.setWindowTitle(self, 'SMGen *')
	
	def change_mu_initial(self):
		QWidget.setWindowTitle(self, 'SMGen *')

	def change_sigma_initial(self):
		QWidget.setWindowTitle(self, 'SMGen *')

	def check_concentration(self):
		QWidget.setWindowTitle(self, 'SMGen *')
		
	def check_quantity(self):
		QWidget.setWindowTitle(self, 'SMGen *')
	
	def change_initial_min(self):
		QWidget.setWindowTitle(self, 'SMGen *')

	def change_initial_max(self):
		QWidget.setWindowTitle(self, 'SMGen *')

	def select_kinetic_parameters_distribution(self):
		if self.kinetic_parameters_distribution.currentText() == "Normal" or self.kinetic_parameters_distribution.currentText() == "Log normal":
			self.mu_kinetic.setEnabled(True)
			self.sigma_kinetic.setEnabled(True)
		else:
			self.mu_kinetic.setEnabled(False)
			self.sigma_kinetic.setEnabled(False)
		QWidget.setWindowTitle(self, 'SMGen *')

	def change_mu_kinetic(self):
		QWidget.setWindowTitle(self, 'SMGen *')

	def change_sigma_kinetic(self):
		QWidget.setWindowTitle(self, 'SMGen *')
	
	def change_kinetic_min(self):
		QWidget.setWindowTitle(self, 'SMGen *')

	def change_kinetic_max(self):
		QWidget.setWindowTitle(self, 'SMGen *')

	def generate_BioSimWare(self):
		if self.generateSBML.isChecked() == True or self.generateBioSimWare.isChecked() == True:
			self.generate_networks.setEnabled(True)
		else:
			self.generate_networks.setEnabled(False)
		# QWidget.setWindowTitle(self, 'SMGen *')

	def generate_SBML(self):
		if self.generateSBML.isChecked() == True or self.generateBioSimWare.isChecked() == True:
			self.generate_networks.setEnabled(True)
		else:
			self.generate_networks.setEnabled(False)
		# QWidget.setWindowTitle(self, 'SMGen *')

	def select_n_networks(self):
		# QWidget.setWindowTitle(self, 'SMGen *')
		pass

	def click_generator_networks(self):
	
		try:

			titl = QWidget.windowTitle(self)

			QWidget.setWindowTitle(self, titl+' ~ Processing...')

			if self.initial_min.text() == '' or self.initial_max.text() == '' or self.kinetic_min.text() == '' or self.kinetic_max.text() == '':
				raise Exception('miss value')
			 
			if self.initial_amounts_distribution.currentText() == 'Normal' or self.initial_amounts_distribution.currentText() == 'Log normal':
				if self.mu_initial.text() == '' or self.sigma_initial.text() == '':
					raise Exception('miss value')
			 
			if self.kinetic_parameters_distribution.currentText() == 'Normal' or self.kinetic_parameters_distribution.currentText() == 'Log normal':
				if self.mu_kinetic.text() == '' or self.sigma_kinetic.text() == '':
					raise Exception('miss value')
			 
			if self.initial_amounts_distribution.currentText() == "Uniform" or self.initial_amounts_distribution.currentText() == "Logarithmic":
				if float(self.initial_min.text()) < 0 or float(self.initial_max.text()) < 0:
					raise Exception("major")
			elif self.initial_amounts_distribution.currentText() == "Normal" or self.initial_amounts_distribution.currentText() == "Log normal":
				if float(self.mu_initial.text()) < 0 or float(self.sigma_initial.text()) < 0 or float(self.initial_min.text()) < 0 or float(self.initial_max.text()) < 0:
					raise Exception("major")
			 
			if self.kinetic_parameters_distribution.currentText() == "Uniform" or self.kinetic_parameters_distribution.currentText() == "Logarithmic":
				if float(self.kinetic_min.text()) < 0 or float(self.kinetic_max.text()) < 0:
					raise Exception("major")
			elif self.kinetic_parameters_distribution.currentText() == "Normal" or self.kinetic_parameters_distribution.currentText() == "Log normal":
				if float(self.mu_kinetic.text()) < 0 or float(self.sigma_kinetic.text()) < 0 or float(self.kinetic_min.text()) < 0 or float(self.kinetic_max.text()) < 0:
					raise Exception("major")
			 
			if (self.maximum_order_reactions.value() + self.maximum_number_products.value()) * self.n_reaction.value() <= self.n_species.value():
				raise Exception("n_species value")
			 					
			if float(self.initial_min.text()) > float(self.initial_max.text()):
				raise Exception("interval initial")
			 	
			if float(self.kinetic_min.text()) > float(self.kinetic_max.text()):
				raise Exception("interval kinetic")
			 	
			if self.initial_amounts_distribution.currentText() == "Normal" or self.initial_amounts_distribution.currentText() == "Log normal":	
				if (float(self.mu_initial.text()) <= float(self.initial_min.text()) or float(self.mu_initial.text()) >= float(self.initial_max.text())):
					raise Exception("mu initial")
			if self.kinetic_parameters_distribution.currentText() == "Normal" or self.kinetic_parameters_distribution.currentText() == "Log normal":	
				if (float(self.mu_kinetic.text()) <= float(self.kinetic_min.text()) or float(self.mu_kinetic.text()) >= float(self.kinetic_max.text())):
					raise Exception("mu kinetic")
			if self.initial_amounts_distribution.currentText() == "Logarithmic":
				if (float(self.initial_min.text()) == 0) or (float(self.initial_max.text()) == 0):
					raise Exception("interval initial")
			if self.kinetic_parameters_distribution.currentText() == "Logarithmic":
				if (float(self.kinetic_min.text()) == 0) or (float(self.kinetic_max.text() == 0)):
					raise Exception("interval kinetic")
			 
			if self.initial_amounts_distribution.currentText() == "Normal" or self.initial_amounts_distribution.currentText() == "Log normal":
				if float(self.sigma_initial.text()) == 0:
					raise Exception("sigma initial")
				elif ((float(self.mu_initial.text()) + 3*float(self.sigma_initial.text())) < float(self.initial_min.text())) or ((float(self.mu_initial.text()) - 3*float(self.sigma_initial.text())) > float(self.initial_max.text())):
					raise Exception("sigma initial")
			 
			if self.kinetic_parameters_distribution.currentText() == "Normal" or self.kinetic_parameters_distribution.currentText() == "Log normal":	
				if float(self.sigma_kinetic.text()) == 0:
					raise Exception("sigma kinetic")
				if ((float(self.mu_kinetic.text()) + 3*float(self.sigma_kinetic.text())) < float(self.kinetic_min.text())) or ((float(self.mu_kinetic.text()) - 3*float(self.sigma_kinetic.text())) > float(self.kinetic_max.text())):
					raise Exception("sigma kinetic")

			if g == []:
				file = str(QFileDialog.getExistingDirectory(None, 'Select Directory', expanduser("~")))
				#file = str(QFileDialog.getExistingDirectory(None, 'Select Directory'))
				if file == '':
					raise Exception('not')
				g.append(file)
			else:
				file = str(QFileDialog.getExistingDirectory(None, 'Select Directory', expanduser(str(g[0]))))
				#file = str(QFileDialog.getExistingDirectory(None, 'Select Directory', str(g[0])))
				if file == '':
					raise Exception('not')
				
			folder_empty = True
			for i in range(int(self.n_networks.value())+1):
				if os.path.exists(file + os.sep + str(i+1)) == True:
					folder_empty = False
					break
				else:
					folder_empty = True

			overwrite = True		
			if folder_empty == False:
				# The QWidget widget is the base class of all user interface objects in PyQt4.
				w = QWidget()
			
				# Show a message box
				result = QMessageBox.question(w, 'Message', "Existing folders. Do you want to overwrite them?", QMessageBox.Cancel | QMessageBox.No | QMessageBox.Yes)
				if result == QMessageBox.Yes:
					overwrite = True
				elif result == QMessageBox.No:
					overwrite = False
				else:
					raise Exception('not')

			if overwrite == False:
				NNETS = []
				w = 1
				for i in range(int(self.n_networks.value())):	
					while os.path.exists(file + os.sep + str(w)) == True:	
						w += 1 
					NNETS.append(w)
					w += 1 
				NNETS.reverse()
			else:
				NNETS = list(range(int(self.n_networks.value()), 0, -1))
			
			if self.initial_amounts_distribution.currentText() == 'Uniform':
				initial_amounts_distribution = 'Uniform'
			elif self.initial_amounts_distribution.currentText() == 'Normal':
				initial_amounts_distribution = 'Normal'
			elif self.initial_amounts_distribution.currentText() == 'Logarithmic':
				initial_amounts_distribution = 'Logarithmic'
			else:
				initial_amounts_distribution = 'Log normal'
			 
			if self.kinetic_parameters_distribution.currentText() == 'Uniform':
				kinetic_parameters_distribution = 'Uniform'
			elif self.kinetic_parameters_distribution.currentText() == 'Normal':
				kinetic_parameters_distribution = 'Normal'
			elif self.kinetic_parameters_distribution.currentText() == 'Logarithmic':
				kinetic_parameters_distribution = 'Logarithmic'
			else:
				kinetic_parameters_distribution = 'Log normal'
			
			self.__disable_boxes()

			parameters = ([
				int(self.n_species.value()), 
				int(self.n_reaction.value()), 
				int(self.maximum_order_reactions.value()), 
				int(self.maximum_number_products.value()), 
				initial_amounts_distribution,
				# self.initial_amounts_distribution.currentText(), 
				float(self.initial_min.text()), 
				float(self.initial_max.text()), 
				float(self.mu_initial.text()), 
				float(self.sigma_initial.text()), 
				kinetic_parameters_distribution,
				# self.kinetic_parameters_distribution.currentText(), 
				float(self.kinetic_min.text()), 
				float(self.kinetic_max.text()), 
				float(self.mu_kinetic.text()), 
				float(self.sigma_kinetic.text()),  
				self.quantity.isChecked(), 
				self.concentration.isChecked(), 
				self.generateBioSimWare.isChecked(),
				self.generateSBML.isChecked(),
				file
				])

			for i in NNETS:
				gen = Generator(parameters)
				gen.generateModel(i)

			activation = True
			QWidget.setWindowTitle(self, titl)
			w = QWidget()
			QMessageBox.information(w, "Information", "Generation finished... If the generated models are big, wait all files have been saved.", QMessageBox.Ok)
			self.__enable_boxes(activation)

		except Exception as err:

			QWidget.setWindowTitle(self, titl)

			if str(err) == "miss value":
				w = QWidget()
				result = QMessageBox.warning(w, 'Warning', "Insert missing values", QMessageBox.Ok)
			elif str(err) == "mu initial":
				w = QWidget()
				result = QMessageBox.warning(w, 'Warning', "Check mu of initial amounts distribution, mu should be strictly included between Min and Max", QMessageBox.Ok)
			elif str(err) == "mu kinetic":
				w = QWidget()
				result = QMessageBox.warning(w, 'Warning', "Check mu of kinetic parameters distribution, mu should be strictly ncluded between Min and Max", QMessageBox.Ok)
			elif str(err) == "sigma initial":
				w = QWidget()
				result = QMessageBox.warning(w, 'Warning', "Check sigma of initial amounts distribution", QMessageBox.Ok)
			elif str(err) == "sigma kinetic":
				w = QWidget()
				result = QMessageBox.warning(w, 'Warning', "Check sigma of kinetic parameters distribution", QMessageBox.Ok)
			elif str(err) == "major":
				w = QWidget()
				result = QMessageBox.warning(w, 'Warning', "Check Numeric Features, they should be positive", QMessageBox.Ok)
			elif str(err) == "interval initial":
				w = QWidget()
				result = QMessageBox.warning(w, 'Warning', "Check min and max of initial amounts distribution", QMessageBox.Ok)
			elif str(err) == "interval kinetic":
				w = QWidget()
				result = QMessageBox.warning(w, 'Warning', "Check min and max of kinetic parameters distribution", QMessageBox.Ok)
			elif str(err) == "n_species value":
				w = QWidget()
				result = QMessageBox.warning(w, 'Warning', "Check General Characteristics' input", QMessageBox.Ok)
			elif str(err) == 'not':
				pass
			else:
				w = QWidget()
				result = QMessageBox.warning(w, 'Warning', "Something went wrong with the current configuration", QMessageBox.Ok)




class Generator:

	def __create_matrix_adj(self, nspec):
		adj = zeros((nspec, nspec))
		value_nodes = np.array([])
		for a in range(nspec):	
			value_nodes = np.append(value_nodes, a)
		i = random.randint(0, np.size(value_nodes)-1)
		x = value_nodes[i]
		value_nodes = np.delete(value_nodes, i)
		j = random.randint(0, np.size(value_nodes)-1)
		y = value_nodes[j]
		value_nodes = np.delete(value_nodes, j)
		adj[int(x)][int(y)] = 1
		while np.array_equal(value_nodes, np.array([])) == False:
			coin = random.randint(0, 1)
			if coin == 1: # modify x
				i = random.randint(0, np.size(value_nodes)-1)
				x = value_nodes[i]
				value_nodes = np.delete(value_nodes, i)
				adj[int(x)][int(y)] = 1
			else: # modify y
				j = random.randint(0, np.size(value_nodes)-1)
				y = value_nodes[j]
				value_nodes = np.delete(value_nodes, j)
				adj[int(x)][int(y)] = 1
		return adj


	def __set_first_value(self, nspec, nreac, adj):
		reagents = zeros((nreac, nspec))
		products = zeros((nreac, nspec))
		xy = np.nonzero(adj)
		x = xy[0]
		y = xy[1]
		if nreac >= nspec:	
			for count in range(np.size(x)):
				reagents[count][x[count]] = 1
				products[count][y[count]] = 1
		else:
			check = 0
			while check <= np.size(x) - 1:
				for count in range(nreac):
					reagents[count][x[check]] = 1
					products[count][y[check]] = 1
					check += 1
					if check > np.size(x) - 1:
						break
		return reagents, products


	def __set_random_value(self, reagents, products, nspec, nreac, maxordreac, maxnumprod, x1, y1, x2, y2):
		for count in range(nreac):
			for count2 in range(maxordreac):
				value = random.randint(0, maxordreac+1)
				col = random.randint(0, nspec-1)
				if (count < np.size(x1)) and value > 0 and count in x1 and col in y1:
					if np.sum(reagents[count]) - reagents[count][col] + value <= maxordreac:
						reagents[count][col] = value
				elif (count < np.size(x1)) and count not in x1 or col not in y1:
					if reagents[count][col] == 0 and np.sum(reagents[count]) + value <= maxordreac:
						reagents[count][col] = value
					elif reagents[count][col] != 0 and np.sum(reagents[count]) - reagents[count][col] + value <= maxordreac:
						reagents[count][col] = value
				elif count >= np.size(x1):
					if reagents[count][col] == 0 and np.sum(reagents[count]) + value <= maxordreac:
						reagents[count][col] = value
					elif reagents[count][col] != 0 and np.sum(reagents[count]) - reagents[count][col] + value <= maxordreac:
						reagents[count][col] = value
		## set random products
		for count in range(nreac):
			for count2 in range(maxnumprod):
				value = random.randint(0, maxnumprod+1)
				col = random.randint(0, nspec-1)
				if (count < np.size(x2)) and value > 0 and count in x2 and col in y2:
					if np.sum(products[count]) - products[count][col] + value <= maxnumprod:
						products[count][col] = value
				elif (count < np.size(x2)) and count not in x2 or col not in y2:
					if products[count][col] == 0 and np.sum(products[count]) + value <= maxordreac:
						products[count][col] = value
					elif products[count][col] != 0 and np.sum(products[count]) - products[count][col] + value <= maxordreac:
						products[count][col] = value
				elif count >= np.size(x2):
					if products[count][col] == 0 and np.sum(products[count]) + value <= maxordreac:
						products[count][col] = value
					elif products[count][col] != 0 and np.sum(products[count]) - products[count][col] + value <= maxordreac:
						products[count][col] = value
		return reagents, products


	def __check_vector_reagents_products_lindep(self, reagents, products, nreac):
		rows_error_lindep = np.array([])
		for count in range(nreac):
			if np.sum(reagents[count]) == 0 and np.sum(products[count]) == 0:
				rows_error_lindep = np.append(rows_error_lindep, count)
			elif np.sum(reagents[count]) != 0 and np.sum(products[count]) != 0 and np.linalg.matrix_rank([reagents[count], products[count]]) < 2:
				rows_error_lindep = np.append(rows_error_lindep, count)
		return rows_error_lindep


	def __check_vector_reagents_products_reactions_equals(self, reagents, products, nspec, nreac):
		rows_error_equals_reactions = np.array([])
		matrix_support = np.array([])
		matrix_support = np.concatenate((reagents, products), axis = 1)
		matrix_support2 = set()		
		for count in range(nreac):
			if tuple(matrix_support[count]) in matrix_support2:
				rows_error_equals_reactions = np.append(rows_error_equals_reactions, count)
			else:
				matrix_support2.add(tuple(matrix_support[count]))
		return rows_error_equals_reactions


	def __rows_correction(self, rows_which_must_be_corrected, reagents, products, nspec, nreac, maxordreac, maxnumprod, x1, y1, x2, y2):

		for count in range(np.size(rows_which_must_be_corrected)):
			reagents[int(rows_which_must_be_corrected[count])] = np.zeros(np.size(reagents[int(rows_which_must_be_corrected[count])]))
			products[int(rows_which_must_be_corrected[count])] = np.zeros(np.size(products[int(rows_which_must_be_corrected[count])]))

			if int(rows_which_must_be_corrected[count]) in x1:
				for u in range(np.size(x1)):
					if int(rows_which_must_be_corrected[count]) == x1[u]:
						reagents[x1[u]][y1[u]] = 1
				for count2 in range(maxordreac):
					value = random.randint(0, maxordreac+1)
					col = random.randint(0, nspec-1)
					if reagents[int(rows_which_must_be_corrected[count])][col] == 0 and np.sum(reagents[int(rows_which_must_be_corrected[count])]) + value <= maxordreac:
						reagents[int(rows_which_must_be_corrected[count])][col] = value
					elif reagents[int(rows_which_must_be_corrected[count])][col] > 0 and np.sum(reagents[int(rows_which_must_be_corrected[count])]) - reagents[int(rows_which_must_be_corrected[count])][col] + value <= maxordreac and value > 0:
						reagents[int(rows_which_must_be_corrected[count])][col] = value
			else:
				for count2 in range(maxordreac):
					value = random.randint(0, maxordreac+1)
					col = random.randint(0, nspec-1)
					if reagents[int(rows_which_must_be_corrected[count])][col] == 0 and np.sum(reagents[int(rows_which_must_be_corrected[count])]) + value <= maxordreac:
						reagents[int(rows_which_must_be_corrected[count])][col] = value
					elif reagents[int(rows_which_must_be_corrected[count])][col] > 0 and np.sum(reagents[int(rows_which_must_be_corrected[count])]) - reagents[int(rows_which_must_be_corrected[count])][col] + value <= maxordreac:
						reagents[int(rows_which_must_be_corrected[count])][col] = value
			if int(rows_which_must_be_corrected[count]) in x2:
				for u in range(np.size(x2)):
					if int(rows_which_must_be_corrected[count]) == x2[u]:
						products[x2[u]][y2[u]] = 1
				for count2 in range(maxnumprod):
					value = random.randint(0, maxnumprod+1)
					col = random.randint(0, nspec-1)
					if products[int(rows_which_must_be_corrected[count])][col] == 0 and np.sum(products[int(rows_which_must_be_corrected[count])]) + value <= maxordreac:
						products[int(rows_which_must_be_corrected[count])][col] = value
					elif products[int(rows_which_must_be_corrected[count])][col] > 0 and np.sum(products[int(rows_which_must_be_corrected[count])]) - products[int(rows_which_must_be_corrected[count])][col] + value <= maxnumprod and value > 0:
						products[int(rows_which_must_be_corrected[count])][col] = value
			else:
				for count2 in range(maxordreac):
					value = random.randint(0, maxordreac+1)
					col = random.randint(0, nspec-1)
					if products[int(rows_which_must_be_corrected[count])][col] == 0 and np.sum(products[int(rows_which_must_be_corrected[count])]) + value <= maxnumprod:
						products[int(rows_which_must_be_corrected[count])][col] = value
					elif products[int(rows_which_must_be_corrected[count])][col] > 0 and np.sum(products[int(rows_which_must_be_corrected[count])]) - products[int(rows_which_must_be_corrected[count])][col] + value <= maxordreac:
						products[int(rows_which_must_be_corrected[count])][col] = value
		return reagents, products


	def __second_check_vector_reagents_products_lindep(self, rows_which_must_be_corrected, reagents, products):
		rows_error_lindep = np.array([])
		for count in range(int(np.size(rows_which_must_be_corrected))):
			if np.sum(reagents[int(rows_which_must_be_corrected[count])]) == 0 and np.sum(products[int(rows_which_must_be_corrected[count])]) == 0:
				rows_error_lindep = np.append(rows_error_lindep, int(rows_which_must_be_corrected[count]))
			elif np.sum(reagents[int(rows_which_must_be_corrected[count])]) != 0 and np.sum(products[int(rows_which_must_be_corrected[count])]) != 0 and np.linalg.matrix_rank([reagents[int(rows_which_must_be_corrected[count])], products[int(rows_which_must_be_corrected[count])]]) < 2:
				rows_error_lindep = np.append(rows_error_lindep, int(rows_which_must_be_corrected[count]))
		return rows_error_lindep


	def __second_check_vector_reagents_products_reactions_equals(self, reagents, products, nspec, nreac):
		rows_error_equals_reactions = np.array([])
		matrix_support = np.array([])
		matrix_support = np.concatenate((reagents, products), axis = 1)
		matrix_support2 = set()		
		for count in range(nreac):
			if tuple(matrix_support[count]) in matrix_support2:
				rows_error_equals_reactions = np.append(rows_error_equals_reactions, count)
			else:
				matrix_support2.add(tuple(matrix_support[count]))
		return rows_error_equals_reactions


	def __set_concentration(self, initialdistr, min_initial, max_initial, nspec, mu_initial, sigma_initial):
		init_constants = np.array([])
		if initialdistr == "Uniform":
			for count in range(nspec):
				num = np.random.uniform(min_initial, max_initial)
				init_constants = np.append(init_constants, num)
		elif initialdistr == "Normal":
			i = 0
			y = 1
			for count in range(nspec):
				num = np.random.normal(mu_initial, sigma_initial)
				while num < min_initial or num > max_initial:
					if i == 1000*nspec:
						if num < min_initial:
							num = min_initial
						elif num > max_initial:
							num = max_initial
						break
					else:
						i = i + 1
						num = np.random.normal(mu_initial, sigma_initial)
				init_constants = np.append(init_constants, num)
		elif initialdistr == "Logarithmic":
			for count in range(nspec):	
				minimo = math.log(min_initial)
				massimo = math.log(max_initial)
				num = math.exp(minimo+(massimo-minimo)*random.random())
				while num < min_initial or num > max_initial:
					num = math.exp(minimo+(massimo-minimo)*random.random())
				init_constants = np.append(init_constants, num)
		elif initialdistr == "Log normal":
			i = 0
			for count in range(nspec):
				num = np.random.lognormal(mu_initial, sigma_initial)
				while num < min_initial or num > max_initial:
					if i == 1000*nspec:
						if num < min_initial:
							num = min_initial
						elif num > max_initial:
							num = max_initial
						break
					else:
						i = i + 1
						num = np.random.lognormal(mu_initial, sigma_initial)
				init_constants = np.append(init_constants, num)
		return init_constants


	def __set_quantity(self, initialdistr, min_initial, max_initial, nspec, mu_initial, sigma_initial):
		init_constants = np.array([])
		if initialdistr == "Uniform":
			for count in range(nspec):
				num = int(np.random.uniform(min_initial, max_initial))
				init_constants = np.append(init_constants, num)
		elif initialdistr == "Normal":
			i = 0
			for count in range(nspec):
				num = int(np.random.normal(mu_initial, sigma_initial))
				while num < min_initial or num > max_initial:
					if i == 1000*nspec:
						if num < min_initial:
							num = min_initial
						elif num > max_initial:
							num = max_initial
						break
					else:
						i = i + 1	
						num = int(np.random.normal(mu_initial, sigma_initial))
				init_constants = np.append(init_constants, num)
		elif initialdistr == "Logarithmic":
			for count in range(nspec):	
				minimo = math.log(min_initial)
				massimo = math.log(max_initial)
				num = int(math.exp(minimo+(massimo-minimo)*random.random()))
				while num < min_initial or num > max_initial:
					num = int(math.exp(minimo+(massimo-minimo)*random.random()))
				init_constants = np.append(init_constants, num)
		elif initialdistr == "Log normal":
			i = 0
			for count in range(nspec):
				num = int(np.random.lognormal(mu_initial, sigma_initial))
				while num < min_initial or num > max_initial:
					if i == 1000*nspec:
						if num < min_initial:
							num = min_initial
						elif num > max_initial:
							num = max_initial
						break
					else:
						i = i + 1
						num = int(np.random.lognormal(mu_initial, sigma_initial))
				init_constants = np.append(init_constants, num)
		return init_constants


	def __set_kinetic(self, kineticdistr, min_kinetic, max_kinetic, nreac, mu_kinetic, sigma_kinetic):
		kinetic_constants_vector = np.array([])
		if kineticdistr == "Uniform":
			for count in range(nreac):
				num = np.random.uniform(min_kinetic, max_kinetic)
				kinetic_constants_vector = np.append(kinetic_constants_vector, num)
		elif kineticdistr == "Normal":
			i = 0
			for count in range(nreac):
				num = np.random.normal(mu_kinetic, sigma_kinetic)
				while num < min_kinetic or num > max_kinetic:
					if i == 1000*nreac:
						if num < min_kinetic:
							num = min_kinetic
						elif num > max_kinetic:
							num = max_kinetic
						break
					else:
						i = i + 1
						num = np.random.normal(mu_kinetic, sigma_kinetic)
				kinetic_constants_vector = np.append(kinetic_constants_vector, num)
		elif kineticdistr == "Logarithmic":
			for count in range(nreac):	
				minimo = math.log(min_kinetic)
				massimo = math.log(max_kinetic)
				num = math.exp(minimo+(massimo-minimo)*random.random())
				while num < min_kinetic or num > max_kinetic:
					num = math.exp(minimo+(massimo-minimo)*random.random())
				kinetic_constants_vector = np.append(kinetic_constants_vector, num)
		elif kineticdistr == "Log normal":
			i = 0
			for count in range(nreac):
				num = np.random.lognormal(mu_kinetic, sigma_kinetic)
				while num < min_kinetic or num > max_kinetic:
					if i == 1000*nreac:
						if num < min_kinetic:
							num = min_kinetic
						elif num > max_kinetic:
							num = max_kinetic
						break
					else:
						i = i + 1
						num = np.random.lognormal(mu_kinetic, sigma_kinetic)
				kinetic_constants_vector = np.append(kinetic_constants_vector, num)
		return kinetic_constants_vector


	def __set_feed(self, nspec):
		vector_feed = np.zeros(nspec)
		return vector_feed

	# binarising m_feed
	def __set_feed2(self, nspec, reac, prod):
		pos = []
		for c in range(prod.shape[1]):
			if np.sum(prod[:,c]) == 0:
				pos.append(c)

		vector_feed = np.zeros(nspec)
		for c in pos:
			vector_feed[c] = 1
			
		return vector_feed


	def __saveModel(self, n_networks, out, quantity, concentration, file, reagents, products, vector_initial, vector_kinetic, vector_feed, nspec, nreac):
		if os.path.exists(file + os.sep + str(n_networks)) == False:
			os.makedirs(file + os.sep + str(n_networks))

		np.savetxt(file + os.sep + str(n_networks) + os.sep + 'left_side', reagents, fmt='%1.0f', delimiter="\t")
		np.savetxt(file + os.sep + str(n_networks) + os.sep + 'right_side', products, fmt='%1.0f', delimiter="\t")
		if concentration == True:
			np.savetxt(file + os.sep + str(n_networks) + os.sep + 'M_0', vector_initial, delimiter="\t", newline="\t")
		elif quantity == True:
			np.savetxt(file + os.sep + str(n_networks) + os.sep + 'M_0', vector_initial, fmt='%1.0f', delimiter="\t", newline="\t")
		np.savetxt(file + os.sep + str(n_networks) + os.sep + 'c_vector', vector_kinetic, delimiter="\n")
		np.savetxt(file + os.sep + str(n_networks) + os.sep + 'M_feed', vector_feed, fmt='%1.0f', delimiter="\t", newline="\t")

		## creating file reactions
		with open(file + os.sep + str(n_networks) + os.sep + '_reactions', 'w') as fo:
			for count in range(nreac):
				add = np.array([])
				if int(np.sum(reagents[count])) == 0:
					add = np.append(add, 'LAMBDA')
				else:
					tmp = np.nonzero(reagents[count])
					for count2 in range(np.size(tmp[0])):
						if reagents[count][tmp[0][count2]] != 1:
							add = np.append(add, str(int(reagents[count][tmp[0][count2]])) + 'S' + str(tmp[0][count2]))
							add = np.append(add, '+')
						else:
							add = np.append(add, 'S' + str(tmp[0][count2]))
							add = np.append(add, '+')
					canc = np.size(add)
					add = np.delete(add, canc-1)
				add = np.append(add, '->')
				if int(np.sum(products[count])) == 0:
					add = np.append(add, 'LAMBDA')
				else:
					tmp = np.nonzero(products[count])
					for count2 in range(np.size(tmp[0])):
						if products[count][tmp[0][count2]] != 1:
							add = np.append(add, str(int(products[count][tmp[0][count2]])) + 'S' + str(tmp[0][count2]))
							add = np.append(add, '+')
						else:
							add = np.append(add, 'S' + str(tmp[0][count2]))
							add = np.append(add, '+')
					canc = np.size(add)
					add = np.delete(add, canc-1)
				for count2 in range(np.size(add)):
					fo.write(str(add[count2]))
				if count != nreac-1:
					fo.write('\n')
		## delete last \t or \n M_0
		file_M_0 = file + os.sep + str(n_networks) + os.sep + 'M_0'
		with open(file_M_0, 'rb+') as filehandle:
			filehandle.seek(-1, os.SEEK_END)
			filehandle.truncate()
		## delete last \t or \n c_vector
		file_c_vector = file + os.sep + str(n_networks) + os.sep + 'c_vector'
		with open(file_c_vector, 'rb+') as filehandle:
			filehandle.seek(-1, os.SEEK_END)
			filehandle.truncate()
		## delete last \t or \n left_side
		file_left_side = file + os.sep + str(n_networks) + os.sep + 'left_side'
		with open(file_left_side, 'rb+') as filehandle:
			filehandle.seek(-1, os.SEEK_END)
			filehandle.truncate()
		## delete last \t or \n right_side
		file_right_side = file + os.sep + str(n_networks) + os.sep + 'right_side'
		with open(file_right_side, 'rb+') as filehandle:
			filehandle.seek(-1, os.SEEK_END)
			filehandle.truncate()
		## delete last \t or \n M_feed
		file_M_feed = file + os.sep + str(n_networks) + os.sep + 'M_feed'
		with open(file_M_feed, 'rb+') as filehandle:
			filehandle.seek(-1, os.SEEK_END)
			filehandle.truncate()
		## delete last \t or \n M_feed
		file_reactions = file + os.sep + str(n_networks) + os.sep + '_reactions'
		with open(file_M_feed, 'rb+') as filehandle:
			filehandle.seek(0, os.SEEK_END)
			filehandle.truncate()  


	def __init__(self, _pars):
		self.pars = _pars
		
		self.nspec = _pars[0]
		self.nreac = _pars[1]
		self.maxordreac = _pars[2]
		self.maxnumprod = _pars[3]
		self.initialdistr = _pars[4]
		self.min_initial = _pars[5]
		self.max_initial = _pars[6]
		self.mu_initial = _pars[7]
		self.sigma_initial = _pars[8]
		self.kineticdistr = _pars[9]
		self.min_kinetic = _pars[10]
		self.max_kinetic = _pars[11]
		self.mu_kinetic = _pars[12]
		self.sigma_kinetic = _pars[13]
		self.quantity = _pars[14]
		self.concentration = _pars[15]
		self.generateBioSimWare = _pars[16]
		self.generateSBML = _pars[17]
		self.file = _pars[18]
		
		
	def generateModel(self, _inp):
		
		self.n_networks = _inp

		## create adj matrix
		adj = self.__create_matrix_adj(self.nspec)

		## convertion from adj to stoichiometric matrix
		reagents, products = self.__set_first_value(self.nspec, self.nreac, adj)
		
		## set random value in stoichiometric matrix
		xy1 = np.nonzero(reagents)
		x1 = xy1[0]
		y1 = xy1[1]
		xy2 = np.nonzero(products)
		x2 = xy2[0]
		y2 = xy2[1]
		reagents, products = self.__set_random_value(reagents, products, self.nspec, self.nreac, self.maxordreac, self.maxnumprod, x1, y1, x2, y2)
		
		## first, linear independence
		rows_error_lindep = self.__check_vector_reagents_products_lindep(reagents, products, self.nreac)
		
		## first, unique reactions
		rows_error_equals_reactions = self.__check_vector_reagents_products_reactions_equals(reagents, products, self.nspec, self.nreac)
		
		## if possible --> correction errors
		loop = 0
		out = False
		while np.size(rows_error_lindep) != 0 or np.size(rows_error_equals_reactions) != 0:
			try:
				if loop > 99:
					out = True
					raise Exception('not possible')
			except Exception as err:
				if str(err) == 'not possible':
					w = QWidget()
					result = QMessageBox.critical(w, 'Warning', "Generation not possible", QMessageBox.Ok)
					break
			if out == True:
				break
			rows_which_must_be_corrected = np.array([])
			rows_which_must_be_corrected = np.append(rows_which_must_be_corrected, rows_error_lindep)
			rows_which_must_be_corrected = np.append(rows_which_must_be_corrected, rows_error_equals_reactions)
			rows_which_must_be_corrected = np.unique(rows_which_must_be_corrected)
			rows_which_must_be_corrected = np.sort(rows_which_must_be_corrected)
			
			## correction
			reagents, products = self.__rows_correction(rows_which_must_be_corrected, reagents, products, self.nspec, self.nreac, self.maxordreac, self.maxnumprod, x1, y1, x2, y2)
			
			## second, linear independence	
			rows_error_lindep = self.__second_check_vector_reagents_products_lindep(rows_which_must_be_corrected, reagents, products)
			
			## second, unique reactions
			rows_error_equals_reactions = self.__second_check_vector_reagents_products_reactions_equals(reagents, products, self.nspec, self.nreac)
				
			loop = loop + 1
		
		
		## generation initial amounts and kinetic parameters
		if self.concentration == True:
			vector_initial = self.__set_concentration(self.initialdistr, self.min_initial, self.max_initial, self.nspec, self.mu_initial, self.sigma_initial)
		elif self.quantity == True:
			vector_initial = self.__set_quantity(self.initialdistr, self.min_initial, self.max_initial, self.nspec, self.mu_initial, self.sigma_initial)
		vector_kinetic = self.__set_kinetic(self.kineticdistr, self.min_kinetic, self.max_kinetic, self.nreac, self.mu_kinetic, self.sigma_kinetic)
		# vector_feed = self.__set_feed(self.nspec)
		vector_feed = self.__set_feed2(self.nspec, reagents, products)


		## save model
		if self.generateBioSimWare == True:
			
			self.__saveModel(self.n_networks, out, self.quantity, self.concentration, self.file, reagents, products, vector_initial, vector_kinetic, vector_feed, self.nspec, self.nreac)

		## save SBML
		if self.generateSBML == True:
			
			if self.quantity == True:
				initial_quantity_or_concentration = 'quantity'
			else:
				initial_quantity_or_concentration = 'concentration'
			file_SBML = SBML(self.n_networks, reagents, products, vector_initial, vector_kinetic, self.nspec, self.nreac, initial_quantity_or_concentration, self.file)
			file_SBML.createSBML()



class SBML:
			

	def __init__(self, _n_networks, _reagents, _products, _vector_initial, _vector_kinetic, _nspec, _nreac, _initial_quantity_or_concentration, _file):
		self.n_networks = _n_networks
		self.reagents = _reagents
		self.products  = _products
		self.vector_initial =  _vector_initial
		self.vector_kinetic  = _vector_kinetic
		self.nspec = _nspec
		self.nreac  = _nreac
		self.initial_quantity_or_concentration = _initial_quantity_or_concentration
		self.file = _file


	def createSBML(self):

		if os.path.exists(self.file + os.sep + str(self.n_networks)) == False:
			os.makedirs(self.file + os.sep + str(self.n_networks))

		## Create Model
		document = SBMLDocument(2, 4) # SBML level and version
		model = document.createModel()
		
		## Create Compartment
		c = model.createCompartment()
		c.setName('Compartment')
		c.setId('C')
		c.setVolume(1)

		## Create Species
		if self.initial_quantity_or_concentration == 'quantity':
			for i in range(int(self.nspec)):
				s = 'S'+str(i)			
				s = model.createSpecies()
				s.setName('S'+str(i))
				s.setId('S'+str(i))
				s.setCompartment('C')
				s.setInitialAmount(self.vector_initial[i])
			for i in range(int(self.nreac)):
				if np.sum(self.reagents[i]) == 0 or np.sum(self.products[i]) == 0:
					s = 'null'		
					s = model.createSpecies()
					s.setName('null')
					s.setId('null')
					s.setCompartment('C')
					s.setInitialAmount(0)
					break
		else:
			for i in range(int(self.nspec)):
				s = 'S'+str(i)			
				s = model.createSpecies()
				s.setName('S'+str(i))
				s.setId('S'+str(i))
				s.setCompartment('C')
				s.setInitialConcentration(self.vector_initial[i])
			for i in range(int(self.nreac)):
				if np.sum(self.reagents[i]) == 0 or np.sum(self.products[i]) == 0:
					s = 'null'		
					s = model.createSpecies()
					s.setName('null')
					s.setId('null')
					s.setCompartment('C')
					s.setInitialConcentration(0)
					break

		## Create Parameters
		for i in range(int(self.nreac)):
			k = 'K'+str(i)
			k = model.createParameter()
			k.setId('K'+str(i))
			k.setConstant(True)
			k.setValue(self.vector_kinetic[i])
		
		## Create Reaction
		for i in range(int(self.nreac)):
			r = 'R'+str(i)	
			r = model.createReaction()
			r.setReversible(False)
			r.setName('R'+str(i))
			r.setId('R'+str(i))
			
			## Create Reactants and Products
			reac = 'reac'+str(i)
			prod = 'prod'+str(i)
			s = []
			for m in range(int(self.nspec)):
				if np.sum(self.reagents[i]) == 0:
					reac = r.createReactant()
					reac.setSpecies('null')
					#reac.setStoichiometry(0)
					break
				if self.reagents[i][m] > 0:
					reac = r.createReactant()
					reac.setSpecies('S'+str(m))
					reac.setStoichiometry(int(self.reagents[i][m]))
					s.append('S'+str(m))
			for m in range(int(self.nspec)):		
				if np.sum(self.products[i]) == 0:
					prod = r.createProduct()
					prod.setSpecies('null')
					#reac.setStoichiometry(0)
					break
				if self.products[i][m] > 0:
					prod = r.createProduct()
					prod.setSpecies('S'+str(m))
					prod.setStoichiometry(int(self.products[i][m]))
			
			re = ' * '

			for i in range(len(s)):
				re = re+s[i]+' * '

			math_ast = parseL3Formula('K'+str(i)+re+'C')
			kinetic_law = r.createKineticLaw()
			kinetic_law.setMath(math_ast)
			
		## Add model in to the document
		document.setModel(model)
		
		## Add optional information
		model.setName('Model')
		model.setId('Model')
		
		## Save to file
		writeSBMLToFile(document, self.file + os.sep + str(self.n_networks) + os.sep + 'modelSBML.xml')

	
def interface():
	app = QtWidgets.QApplication(sys.argv)
	window = MyWindow()
	window.show()
	app.exec_()
	sys.exit()
	

## main
if __name__ == '__main__':
	interface()
