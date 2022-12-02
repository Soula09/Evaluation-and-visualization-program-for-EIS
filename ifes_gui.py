import sys
import os
from pathlib import Path
import logging
import warnings
warnings.filterwarnings("ignore", "(?s).*MATPLOTLIBDATA.*", category=UserWarning)
logging.getLogger('matplotlib.font_manager').disabled = True
import numpy as np
import pandas as pd
import datums
import matplotlib.pyplot as plt


import visuals
import utils
import model
import impedance as imp
from impedance.models.circuits import CustomCircuit, BaseCircuit
from impedance.models.circuits.fitting import rmse
from scipy.stats import chisquare

from impedance.visualization import plot_nyquist, plot_residuals,plot_bode , plot_bode_amp, plot_bode_phase,plot_nyquistlinkk


from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar

import ctypes
from model import Datum

# import emn_sdk
# from emn_sdk.io.ckan import CKAN

from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtWidgets import QScrollArea
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QDesktopServices, QFont, QPalette, QColor
from PyQt5.QtCore import Qt
from PyQt5.QtCore import qVersion
# from matplotlib.backends.backend_qt5agg import (FigureCanvas, NavigationToolbar2QT as NavigationToolbar)

import matplotlib
from matplotlib.figure import Figure
from matplotlib.lines import Line2D
import matplotlib



class DataHandler():
	def __init__(self):
		self.folder = IfesUI.homedir
		self.files = None
		self.data = []
		self.data_linkk = []
		self.expt_type = 'cp'
		self.colone = 2
		self.coltwo = 3
		self.colthree = 4 #f
		self.colfour = 5 # re(Z)
		self.colfive= 6 # im(Z)
		self.colsix = 1 #time 
		self.area = 22.68
		self.maxfreq = 100000
		self.current_factor = 1
		self.voltage_factor  = 1
		self.negative_imaginary = 1
		self.refelec = 0
		self.rxn = 0
		self.mu = 0
		self.rmse = 0
		self.randle = 0
		self.pyr = False
		self.pts_to_avg = 300
		self.export_data = False
		self.saveloc = ''

	### actions ###
	def load_raw_data(self):
		all_data = datums.load_data(filename=self.files, folder=self.folder, expt_type=self.expt_type)
		current_names = [d.get_name() for d in self.data]
		new_data = [d for d in all_data if d.get_name() not in current_names]
		self.data.extend(new_data)

	def process_data(self):
		self.load_raw_data()
		if self.expt_type == 'cv':
			datums.cv_process(data=self.data, potential_column=self.colone, current_column=self.coltwo, area=self.area, reference=self.refelec, export_data=self.export_data, save_dir=self.saveloc)
		elif self.expt_type == 'lsv':
			datums.lsv_process(data=self.data, potential_column=self.colone, current_column=self.coltwo, area=self.area, reference=self.refelec, thermo_potential=self.rxn, export_data=self.export_data, save_dir=self.saveloc)
		elif self.expt_type == 'cp':
			datums.cp_process(data=self.data, potential_column=self.colone, current_column=self.coltwo, area=self.area, reference=self.refelec, thermo_potential=self.rxn, export_data=self.export_data, save_dir=self.saveloc, pts_to_avg=self.pts_to_avg, pyramic=self.pyr)
		elif self.expt_type == 'ca':
			datums.ca_process(data=self.data, potential_column=self.colone, current_column=self.coltwo, area=self.area, reference=self.refelec, thermo_potential=self.rxn, export_data=self.export_data, save_dir=self.saveloc, pts_to_avg=self.pts_to_avg, pyramic=self.pyr)
		elif self.expt_type == 'eis':
			new_data = datums.eis_process(self.data,time_column= self.colsix, voltage_column= self.colone,current_column=self.coltwo,freq_column= self.colthree, real_column=self.colfour, imag_column=self.colfive, area=self.area, maxfreq = self.maxfreq ,current_factor= self.current_factor,voltage_factor=self.voltage_factor,negative_imaginary =self.negative_imaginary, export_data=self.export_data, save_dir=self.saveloc)
			# new_data = datums.eis_process(self.data, real_column=self.coltwo, imag_column=self.colthree, export_data=self.export_data, save_dir=self.saveloc)
			self.data = new_data


	### accessors ###
	def get_folder(self):
		return self.folder

	def get_files(self):
		return self.files

	def get_data(self):
		return self.data

	def get_data_linkk(self):
		return self.data_linkk

	def get_expt_type(self):
		return self.expt_type

	### modifiers ###
	def set_folder(self, new_folder):
		self.folder = new_folder

	def set_files(self, new_files):
		self.files = new_files

	def set_data(self, new_data):
		self.data = new_data

	def set_expt_type(self, new_type):
		self.expt_type = new_type

	def set_colone(self, new_col):
		self.colone = new_col

	def set_coltwo(self, new_col):
		self.coltwo = new_col

	def set_colthree(self, new_col):
		self.colthree = new_col

	def set_colfour(self, new_col):
		self.colfour = new_col

	def set_colfive(self, new_col):
		self.colfive = new_col

	def set_colsix(self, new_col):
		self.colsix = new_col

	def set_area(self, new_area):
		self.area = new_area

	def set_maxfreq(self, new_maxfreq):
		self.maxfreq = new_maxfreq

	def set_refelec(self, new_val):
		self.refelec = newval

	def set_rxn(self, new_val):
		self.rxn = new_val

	def set_pyr(self, new_state):
		self.pyr = new_state

	def set_mu(self, new_state):
		self.mu = new_state

	def set_rmse(self, new_state):
		self.rmse = new_state

	def set_mu(self, new_state):
		self.mu = new_state

	def set_voltage_factor(self, new_val):
		self.voltage_factor = new_val

	def set_negative_imaginary(self, new_val):
		self.negative_imaginary = new_val

	def set_current_factor(self, new_val):
		self.current_factor = new_val

	def set_pts_to_avg(self, new_val):
		self.pts_to_avg = new_val

	def set_export_data(self, new_state):
		self.export_data = new_state
		

	def set_saveloc(self, new_path):
		self.saveloc = new_path

class VisualHandler():
	def __init__(self):
		self.data = []
		self.plot_data = []
		self.eis_data = []
		self.linkk_data = []
		self.tafel_data = []
		self.bayes_data = []
		self.datafolder = None
		self.datafiles = None
		self.vis_code = 0
		self.use_raw = False
		self.xcol = 0
		self.ycol = 1
		self.ecol = 3
		self.drawline = True
		self.drawscatter = True
		self.drawerr = False

		self.expt_codes = {0:['ca', 'cp'], 1:['cv'], 2:['lsv'], 3:['eis']}

	### actions ###
	def load_data(self):
		new_data = datums.load_data(filename=self.datafiles, folder=self.datafolder)
		for this_data in new_data:
			if this_data.get_processed_data() is None:
				this_data.set_processed_data(this_data.get_raw_data())
		self.data.extend(new_data)

	def load_eis(self):
		new_data = datums.load_data(filename=self.datafiles, folder=self.datafolder)
		for this_data in new_data:
			this_data.set_expt_type('eis')
			if this_data.get_processed_data() is None:
				this_data.set_processed_data(this_data.get_raw_data())
		self.eis_data = datums.eis_process(new_data)
		self.linkk_data = this_data.get_processed_data_linkk()



	def load_tafel(self):
		new_data = datums.load_data(filename=self.datafiles, folder=self.datafolder)
		for this_data in new_data:
			this_data.set_expt_type('lsv')
			if this_data.get_processed_data() is None:
				this_data.set_processed_data(this_data.get_raw_data())
		self.tafel_data = datums.lsv_process(new_data)

	def load_bayes(self):
		new_data = datums.load_data(filename=self.datafiles, folder=self.datafolder)
		for this_data in new_data:
			this_data.set_expt_type('lsv')
			if this_data.get_processed_data() is None:
				this_data.set_processed_data(this_data.get_raw_data())
		self.bayes_data = datums.lsv_process(new_data)

	def draw_plot(self, ax):
		self.plot_data = [d for d in self.data if d.get_expt_type() in self.expt_codes[self.vis_code]]
		if self.vis_code == 0:
			plotfun = visuals.polcurve
			curr = self.xcol
			pot = self.ycol
		elif self.vis_code == 1:
			plotfun = visuals.plot_cv
			curr = self.ycol
			pot = self.xcol
		elif self.vis_code == 2:
			plotfun = visuals.plot_lsv
			curr = self.ycol
			pot = self.xcol
		elif self.vis_code == 3:
			plotfun = visuals.plot_eis
			curr = self.xcol
			pot = self.ycol
		else:
			return
		plotfun(data=self.plot_data, ax=ax, line=self.drawline, scatter=self.drawscatter, errs=self.drawerr, current_column=curr, potential_column=pot, err_column=self.ecol)

	### accessors ###
	def get_plot_data(self):
		return self.plot_data

	def get_eis_data(self):
		return self.eis_data

	def get_linkk_data(self):
		return self.linkk_data

	def get_tafel_data(self):
		return self.tafel_data

	def get_bayes_data(self):
		return self.bayes_data

	### modifiers ###
	def set_datafolder(self, new_folder):
		self.datafolder = new_folder

	def set_datafiles(self, new_files):
		self.datafiles = new_files

	def set_data(self, all_data, replace=False):
		if replace:
			self.data = all_data
			new_data = all_data
		else:
			current_names = [d.get_name() for d in self.data]
			new_data = [d for d in all_data if d.get_name() not in current_names]
		self.data.extend(new_data)
		self.eis_data.extend([d for d in all_data if d.get_expt_type() == 'eis'])
		self.linkk_data.extend([d for d in all_data if d.get_expt_type() == 'eis'])
		self.tafel_data.extend([d for d in all_data if d.get_expt_type() == 'lsv'])
		self.bayes_data.extend([d for d in all_data if d.get_expt_type() == 'lsv'])

	def set_vis_code(self, new_code):
		self.vis_code = new_code
		# expt_code = []
		# if new_code == 0:
		# 	expt_code.append('cp')
		# 	expt_code.append('ca')
		# elif new_code == 1:
		# 	expt_code.append('cv')
		# elif new_code == 2:
		# 	expt_code.append('lsv')
		# elif new_code == 3:
		# 	expt_code.append('eis')
		# else:
		# 	return
		new_data = [d for d in self.data if d.get_expt_type() in self.expt_codes[self.vis_code]]
		self.plot_data = new_data
		if new_code == 2:
			self.tafel_data = new_data
		if new_code == 3:
			self.eis_data = new_data
			self.linkk_data = new_data

	def set_xcol(self, new_col):
		self.xcol = new_col

	def set_ycol(self, new_col):
		self.ycol = new_col

	def set_ecol(self, new_col):
		self.ecol = new_col

	def set_drawline(self, new_state):
		self.drawline = new_state

	def set_drawscatter(self, new_state):
		self.drawscatter = new_state

	def set_drawerr(self, new_state):
		self.drawerr= new_state

class UploadHandler():
	def __init__(self):
		self.url = 'https://www.ifes.uni-hannover.de/en/ees/'
		self.apikey = '53596bad-6601-49c1-bf65-e02c7b379776'
		self.project = 'API Sandbox'
		self.institution = 'Electric Energy Storage System Section'
		self.package = 'foobar_sg'
		self.use_existing = True
		self.files = None
		self.records = None
		self.basedir = IfesUI.homedir

	# actions
	# def upload(self):
	# 	try:
	# 		ckan = CKAN(self.url, self.apikey)
	# 		ckan.set_dataset_info(self.project, self.institution)
	# 		ckan.upload(name=self.package, files=self.files, records=self.records, basedir=self.basedir, use_existing=self.use_existing)
	# 		return 'upload successful!'
	# 	except Exception as e:
	# 		return str(e)

	# accessors
	def get_url(self, new_url):
		return self.url

	def get_apikey(self, new_key):
		return self.apikey

	def get_project(self, new_proj):
		return self.project

	def get_institution(self, new_inst):
		return self.institution

	def get_package(self, new_pkg):
		return self.package

	def get_useexisting(self, newval):
		return self.useexisting

	def get_files(self, new_files):
		return self.files

	def get_records(self, new_records):
		return self.records

	def get_basedir(self, new_dir):
		return self.basedir

	# modifiers
	def set_url(self, new_url):
		self.url = new_url

	def set_apikey(self, new_key):
		self.apikey = new_key

	def set_project(self, new_proj):
		self.project = new_proj

	def set_institution(self, new_inst):
		self.institution = new_inst

	def set_package(self, new_pkg):
		self.package = new_pkg

	def set_useexisting(self, newval):
		self.useexisting = newval

	def set_files(self, new_files):
		self.files = new_files

	def set_records(self, new_records):
		self.records = new_records

	def set_basedir(self, new_dir):
		self.basedir = new_dir

class TableModel(QtCore.QAbstractTableModel):
	def __init__(self, data):
		super().__init__()
		self._data = data

	def data(self, index, role):
		if role == Qt.DisplayRole:
			value = self._data.iloc[index.row(), index.column()]
			if isinstance(value, float):
				value = "%.4f" % value
			return str(value)

	def rowCount(self, index):
		return self._data.shape[0]

	def columnCount(self, index):
		return self._data.shape[1]

	def headerData(self, section, orientation, role):
		# section is the index of the column/row.
		if role == Qt.DisplayRole:
			if orientation == Qt.Horizontal:
				return str(self._data.columns[section])
			if orientation == Qt.Vertical:
				return str(self._data.index[section])

class IfesWindow(QMainWindow):
	def __init__(self):
		super().__init__()
		self.setWindowTitle('IFES Tool')
		self.setStyleSheet("background-color: ghostwhite;")
		self.menubar = self.menuBar()
		self.statusbar = self.statusBar()
		self.statusbar.showMessage('GUI launched successfully', 5000)
		self.make_menubar()
		self.set_size(1, 1)

	def set_size(self, w, h):
		dw = QDesktopWidget()
		width = dw.availableGeometry(self).width()
		height = dw.availableGeometry(self).height()
		# hdelta = height+8
		# s = QScrollBar(self)
		# scrollbar_adjust = min(s.width(), s.height())
		# self.resize(width+scrollbar_adjust, height+scrollbar_adjust)
		# screen_height = dw.availableGeometry(self).height() - 25
		# height = min(screen_height, height+hdelta+scrollbar_adjust)
		# self.resize(width+scrollbar_adjust, height)
		self.resize(width * w, height * h)

	def make_menubar(self):
		# create menus
		file = self.menubar.addMenu('File')
		info = self.menubar.addMenu('Info')
		# create actions
		quit = QAction(' Exit', self)
		quit.triggered.connect(self.close)
		docs = QAction('Documentation', self)
		docs.triggered.connect(self.documentation_url)
		git = QAction('Github Page', self)
		git.triggered.connect(self.github_url)
		# add actions to menus
		file.addAction(quit)
		info.addAction(git)
		info.addAction(docs)

	def close(self):
		sys.exit()

	def documentation_url(self):
		url = QtCore.QUrl('https://Ifes.readthedocs.io/en/latest/')
		QtGui.QDesktopServices.openUrl(url)

	def github_url(self):
		url = QtCore.QUrl('https://github.com/samaygarg/Ifes')
		QtGui.QDesktopServices.openUrl(url)


class IfesUI(QTabWidget):

	tintin = ['blistering barnacles', 'thundering typhoon', 'my jewels!', 'woah!']
	refelecs = datums.ref_electrodes
	thermo_potentials = datums.thermo_potentials
	expt_types = { 'Chronopotentiometry':'cp', 'Chronoamperometry': 'ca', 'Cyclic voltammetry': 'cv', 'Linear sweep voltammetry': 'lsv', 'Electrochemical impedance spectroscopy':'eis'}
	vis_types = {'HFR and HFR Frequency vs. Current density':0, 'HFR vs. Current density':1, 'HFR Frequency vs. Current density':2, 'I–U curve':3}
	expt_types_rev = {y:x for x,y in expt_types.items()}
	markerstyles_rev = {Line2D.markers[m]:m for m in Line2D.filled_markers}
	# vis_types = {'Cyclic Voltammagram':'cv', 'Polarization Curve':'cp'}
	homedir = str(Path.home())
	default_figsize = (7,5)
	default_figsize1 = (6,4)
	default_figres = 300

	headerfont = QFont()
	default_size = headerfont.pointSize()
	headerfont.setPointSize(20)
	headerfont.setBold(True)

	headerfont1 = QFont()
	default_size1 = headerfont.pointSize()
	headerfont1.setPointSize(15)
	headerfont1.setBold(True)

	headerfont2 = QFont()
	default_size2 = headerfont.pointSize()
	headerfont2.setPointSize(12)
	headerfont2.setBold(True)

	valuefont = QFont()
	valuefont.setBold(True)

	notefont = QFont()
	notefont.setItalic(True)
	notefont.setBold(True)

	def __init__(self, main_window):
		super().__init__()
		# self.tintin = ['blistering barnacles', 'thundering typhoon', 'my jewels!', 'woah!']
		self.window = main_window
		self.window.setCentralWidget(self)
		self.datahandler = DataHandler()
		self.vishandler = VisualHandler()
		self.uploader = UploadHandler()


		self.data_tab = self.makeTab(self.datums_layout(), 'Data Processing')
		
		# self.tafel_tab = self.makeTab(self.tafel_layout(), 'Tafel Analysis')
		self.eis_tab = self.makeTab(self.eis_layout(), 'HFR Analysis')
		self.linkk_tab = self.makeTab(self.linkk_layout(), 'Kramers Kronig ')
		self.equivalentcircuit_tab = self.makeTab(self.EC_layout(), 'Equivalent circuit')
		# self.visuals_tab = self.makeTab(self.visuals_layout(), 'Visualization')
		# self.bayes_tab = self.makeTab(self.bayes_layout(), 'Bayesian Tafel Analysis')
		# self.datahub_tab = self.makeTab(self.datahub_layout(), 'Datahub Upload')

		self.data_dict = {}
		self.eis_dict = {}
		self.linkk_dict = {}
		self.ec_dict = {}
		self.tafel_dict = {}
		self.bayes_dict = {}

		self.line_dict_vis = {}
		self.line_dict_eis = {}
		self.line_dict_linkk = {}
		self.line_dict_tafel = {}

	def makeTab(self, layout, name):
		tab = QWidget()
		tab.setLayout(layout)
		self.addTab(tab, name)
		return tab

	def update_status(self, message):
		self.window.statusbar.showMessage(message, 10000)

	def close(self):
		sys.exit()

	### general use methods ###
	def set_max_width(self, widget, scale=1):
		size = widget.sizeHint()
		w = size.width()
		widget.setMaximumWidth(int(w*scale))

	def set_min_width(self, widget, scale=1):
		size = widget.sizeHint()
		w = size.width()
		widget.setMinimumWidth(int(w*scale))

	def set_max_height(self, widget, scale=1):
		size = widget.sizeHint()
		h = size.height()
		widget.setMaximumHeight(int(h*scale))

	def set_min_height(self, widget, scale=1):
		size = widget.sizeHint()
		h = size.height()
		widget.setMinimumHeight(int(h*scale))

	def get_all_files(self, dir, valid=None):
		allfiles = os.listdir(dir)
		files = []
		for f in allfiles:
			if os.path.isdir(os.path.join(dir, f)) or f.startswith('.'):
				continue
			elif valid:
				try:
					name, filetype = f.split('.')
				except Exception:
					continue
				if filetype.lower() not in valid:
					continue
			files.append(f)
		return files

	###################
	# Data Processing #
	###################
	### data processing layout ###
	def datums_layout(self):
		# file selection header
		self.header_data = QLabel('Select Data')
		self.header_data.setFont(IfesUI.headerfont)
		# folder selection widgets
		self.folder_lbl_data = QLabel('Data folder')
		self.folder_txtbx_data = QLineEdit(IfesUI.homedir)
		self.folder_btn_data = QPushButton('Choose folder...')
		# file selection widgets
		self.file_lbl_data = QLabel('Data files')
		self.file_txtbx_data = QLineEdit()
		self.file_btn_data = QPushButton('Choose files...')
		# experiment selection header
		self.header_expt = QLabel('Experiment Parameters')
		self.header_expt.setFont(IfesUI.headerfont)
		# experiment selection widgets
		self.protocol_lbl = QLabel('Data processing protocol')
		self.protocol_menu = QComboBox()
		for n in IfesUI.expt_types.keys():
			self.protocol_menu.addItem(n)
		self.applytoall_chkbx = QCheckBox('Apply to all files')
		self.applytoall_chkbx.setCheckState(Qt.Unchecked)
		self.applytoall_chkbx.setEnabled(False)
		# column selection layout
		self.colslayout_data = self.colselction_layout_data()
		# parameters layout
		self.paramslayout_data = self.param_layout_data()
		# data processing header
		self.header_process = QLabel('Process Data')
		self.header_process.setFont(IfesUI.headerfont)
		# processing button
		self.process_btn = QPushButton('Process Data')
		self.process_btn.setFont(IfesUI.notefont)
		self.process_btn.setFixedSize(120,60)
		self.process_btn.setStyleSheet("background-color: slateblue")
		# export data widgets
		self.save_chkbx_data = QCheckBox('Export processed data')
		self.save_chkbx_data.setLayoutDirection(Qt.RightToLeft)
		self.save_chkbx_data.setCheckState(Qt.Unchecked)
		self.saveloc_txtbx_data = QLineEdit(self.default_saveloc_data())
		self.saveloc_btn_data = QPushButton('Choose location...')
		# data table layout
		self.tbllayout = self.table_layout()
		# connect widgets
		self.folder_txtbx_data.textChanged.connect(self.folder_action_data)
		self.folder_btn_data.clicked.connect(self.choose_folder_data)
		self.file_txtbx_data.textChanged.connect(self.file_action_data)
		self.file_btn_data.clicked.connect(self.choose_files_data)
		self.protocol_menu.currentTextChanged.connect(self.protocol_action)
		self.process_btn.clicked.connect(self.process_action)
		self.save_chkbx_data.stateChanged.connect(self.savechkbx_action)
		self.saveloc_txtbx_data.textChanged.connect(self.saveloc_action_data)
		self.saveloc_btn_data.clicked.connect(self.choose_saveloc_data)
		# build layout
		layout = QGridLayout()
		row = 0
		layout.addWidget(self.header_data, row, 0, 1, -1, Qt.AlignHCenter)
		row += 1
		layout.addWidget(self.folder_lbl_data, row, 0, Qt.AlignRight)
		layout.addWidget(self.folder_txtbx_data, row, 1)
		layout.addWidget(self.folder_btn_data, row, 2)
		row += 1
		layout.addWidget(self.file_lbl_data, row, 0, Qt.AlignRight)
		layout.addWidget(self.file_txtbx_data, row, 1)
		layout.addWidget(self.file_btn_data, row, 2)
		row += 1
		layout.addWidget(self.header_expt, row, 0, 1, -1, Qt.AlignHCenter)
		row += 1
		layout.addWidget(self.protocol_lbl, row, 0, Qt.AlignRight)
		layout.addWidget(self.protocol_menu, row, 1,)
		layout.addWidget(self.applytoall_chkbx, row, 2)
		row += 1
		layout.addLayout(self.colslayout_data, row, 0, 1, -1, Qt.AlignLeft)
		row += 1
		layout.addLayout(self.paramslayout_data, row, 0, 1, -1, Qt.AlignLeft)
		row += 1
		layout.addWidget(self.header_process, row, 0, 1, -1, Qt.AlignHCenter)
		row += 1
		layout.addWidget(self.save_chkbx_data, row, 0, Qt.AlignRight)
		layout.addWidget(self.saveloc_txtbx_data, row, 1)
		layout.addWidget(self.saveloc_btn_data, row, 2)
		row += 1
		layout.addWidget(self.process_btn, row, 0, 1, -1, Qt.AlignHCenter)
		row += 1
		layout.addLayout(self.tbllayout, row, 0, 1, -1, Qt.AlignHCenter)
		return layout

	def colselction_layout_data(self):
		# column selection widgets
		self.colone_lbl = QLabel('Voltage column')
		self.colone_txtbx = QLineEdit('2')
		# self.colone_txtbx.setFixedWidth(60)
		self.coltwo_lbl = QLabel('Current column')
		self.coltwo_txtbx = QLineEdit('3')
		# self.coltwo_txtbx.setFixedWidth(60)
		self.colthree_lbl = QLabel('Frequency column')
		self.colthree_txtbx = QLineEdit('4')
		# self.colthree_txtbx.setFixedWidth(60)
		self.colfour_lbl = QLabel('Real column')
		self.colfour_txtbx = QLineEdit('5')
		# self.colfour_txtbx.setFixedWidth(60)
		self.colfive_lbl = QLabel('Imag column')
		self.colfive_txtbx = QLineEdit('6')
		# self.colfour_txtbx.setFixedWidth(60)
		self.colsix_lbl = QLabel('Time column')
		self.colsix_txtbx = QLineEdit('1')
		# self.colfive_txtbx.setFixedWidth(60)
		# Voltage factor
		self.voltage_factor_lbl = QLabel('Voltage factor')
		self.voltage_factor_txtbx = QLineEdit('1')
		# Current factor
		self.current_factor_lbl = QLabel('Current factor')
		self.current_factor_txtbx = QLineEdit('1')
		# sign imaginary part 
		self.negative_imaginary_lbl = QLabel('Sign of Im(Z)')
		self.negative_imaginary_txtbx = QLineEdit('1')
		# col id note
		self.colnote_lbl = QLabel('Note: Column indexing starts at 0 ')
		self.colnote_lbl.setFont(IfesUI.notefont)
		 # Factor and Prefix note 
		self.factornote_lbl = QLabel('Note: Voltage and current are specified in Volts and Amperes respectively   Example: For mV -> voltage factor = 1e3')
		self.factornote_lbl.setFont(IfesUI.notefont)
		# connect widgets
		self.colone_txtbx.textChanged.connect(self.colone_action)
		self.colthree_txtbx.textChanged.connect(self.colthree_action)
		self.coltwo_txtbx.textChanged.connect(self.coltwo_action)
		self.colfour_txtbx.textChanged.connect(self.colfour_action)
		self.colfive_txtbx.textChanged.connect(self.colfive_action)
		self.colsix_txtbx.textChanged.connect(self.colsix_action)
		# build layout
		layout = QGridLayout()
		layout.addWidget(self.colsix_lbl, 0, 0, Qt.AlignLeft)
		layout.addWidget(self.colsix_txtbx, 0, 1, Qt.AlignLeft)
		layout.addWidget(self.colone_lbl, 0, 2, Qt.AlignLeft)
		layout.addWidget(self.colone_txtbx, 0, 3, Qt.AlignLeft)
		layout.addWidget(self.coltwo_lbl, 0, 4, Qt.AlignLeft)
		layout.addWidget(self.coltwo_txtbx, 0, 5, Qt.AlignLeft)
		layout.addWidget(self.colthree_lbl, 0, 6, Qt.AlignLeft)
		layout.addWidget(self.colthree_txtbx, 0, 7, Qt.AlignLeft)
		layout.addWidget(self.colfour_lbl, 0,8, Qt.AlignLeft)
		layout.addWidget(self.colfour_txtbx, 0,9, Qt.AlignLeft)
		layout.addWidget(self.colfive_lbl, 0, 10, Qt.AlignLeft)
		layout.addWidget(self.colfive_txtbx, 0, 11, Qt.AlignLeft)
		layout.addWidget(self.colnote_lbl, 0, 12, Qt.AlignLeft)
		layout.addWidget(self.voltage_factor_lbl, 1, 0, Qt.AlignLeft)
		layout.addWidget(self.voltage_factor_txtbx, 1, 1, Qt.AlignLeft)
		layout.addWidget(self.current_factor_lbl, 1, 2, Qt.AlignLeft)
		layout.addWidget(self.current_factor_txtbx, 1, 3, Qt.AlignLeft)
		layout.addWidget(self.negative_imaginary_lbl, 1, 4, Qt.AlignRight)
		layout.addWidget(self.negative_imaginary_txtbx, 1, 5, Qt.AlignLeft)
		layout.addWidget(self.factornote_lbl, 1, 6,1,8, Qt.AlignLeft)
		# resize widgets
		for i in range(layout.count()):
			w = layout.itemAt(i).widget()
			if isinstance(w, QLineEdit):
				self.set_max_width(w, 0.5)
		return layout

	def param_layout_data(self):
		
		# mea area widgets
		self.area_lbl = QLabel(f'MEA area in cm<sup>2</sup>')
		self.area_txtbx = QLineEdit('22.68')
		#Maximal frequency
		self.maxfreq_lbl = QLabel('Maximum frequency in Hz')
		self.maxfreq_txtbx = QLineEdit('100000')
		# reference electrode widgets
		self.refelec_lbl = QLabel('Reference electrode')
		self.refelec_menu = QComboBox()
		for name, val in IfesUI.refelecs.items():
			thislabel = name.upper() + f' ({str(val)} V)'
			self.refelec_menu.addItem(thislabel)
		self.refelec_menu.addItem('custom')
		self.refelec_txtbx = QLineEdit(str(list(IfesUI.refelecs.values())[0]))
		self.refelec_txtbx.setEnabled(False)
		# reaction widgets
		self.rxn_lbl = QLabel('Reaction (thermodynamic potential)')
		self.rxn_menu = QComboBox()
		for name, val in IfesUI.thermo_potentials.items():
			thislabel = name.upper() + f' ({str(val)} V)'
			self.rxn_menu.addItem(thislabel)
		self.rxn_menu.addItem('custom')
		self.rxn_txtbx = QLineEdit(str(list(IfesUI.thermo_potentials.values())[0]))
		self.rxn_txtbx.setEnabled(False)
		# pyramid widgets
		self.pyr_lbl = QLabel('Pyramid')
		self.pyr_chkbx = QCheckBox()
		self.pyr_chkbx.setCheckState(Qt.Checked)
		# points to average
		self.ststpts_lbl = QLabel('Points to average')
		self.ststpts_txtbx = QLineEdit('300')
		# connect widgets
		self.area_txtbx.textChanged.connect(self.area_action)
		self.maxfreq_txtbx.textChanged.connect(self.maxfreq_action)
		self.voltage_factor_txtbx.textChanged.connect(self.voltage_factor_action)
		self.current_factor_txtbx.textChanged.connect(self.current_factor_action)
		self.negative_imaginary_txtbx.textChanged.connect(self.negative_imaginary_action)
		self.refelec_menu.currentTextChanged.connect(self.refelec_menu_action)
		self.refelec_txtbx.textChanged.connect(self.refelec_txtbx_action)
		self.rxn_menu.currentTextChanged.connect(self.rxn_menu_action)
		self.rxn_txtbx.textChanged.connect(self.rxn_txtbx_action)
		self.pyr_chkbx.stateChanged.connect(self.pyr_action)
		self.ststpts_txtbx.textChanged.connect(self.ststpts_action)
		# build layout
		layout = QGridLayout()
		row = 0
		layout.addWidget(self.area_lbl, row, 0, Qt.AlignLeft)
		layout.addWidget(self.area_txtbx, row, 1, Qt.AlignLeft)
		layout.addWidget(self.maxfreq_lbl, row, 2, Qt.AlignLeft)
		layout.addWidget(self.maxfreq_txtbx, row, 3, Qt.AlignLeft)
		# row += 1
		# layout.addWidget(self.refelec_lbl, row, 0, Qt.AlignLeft)
		# layout.addWidget(self.refelec_menu, row, 1, Qt.AlignLeft)
		# layout.addWidget(self.refelec_txtbx, row, 2, Qt.AlignLeft)
		# row += 1
		# layout.addWidget(self.rxn_lbl, row, 0, Qt.AlignLeft)
		# layout.addWidget(self.rxn_menu, row, 1, Qt.AlignLeft)
		# layout.addWidget(self.rxn_txtbx, row, 2, Qt.AlignLeft)
		# row += 1
		# layout.addWidget(self.pyr_lbl, row, 0, Qt.AlignLeft)
		# layout.addWidget(self.pyr_chkbx, row, 1, Qt.AlignLeft)
		# row += 1
		# layout.addWidget(self.ststpts_lbl, row, 0, Qt.AlignLeft)
		# layout.addWidget(self.ststpts_txtbx, row, 1, Qt.AlignLeft)
		# resize widgets
		for i in range(layout.count()):
			w = layout.itemAt(i).widget()
			if isinstance(w, QLineEdit):
				self.set_max_width(w, 0.5)
			elif isinstance(w, QComboBox):
				self.set_max_width(w)
		return layout

	def table_layout(self):
		# table widget
		self.datatable = QTableView()
		# data selector
		self.datatable_selector = QComboBox()
		self.datatable_selector.setEnabled(False)
		# connect widgets
		self.datatable_selector.currentTextChanged.connect(self.datatable_selector_action)
		# build layout
		layout = QGridLayout()
		layout.addWidget(self.datatable, 0, 0, Qt.AlignHCenter)
		layout.addWidget(self.datatable_selector, 0, 1, Qt.AlignHCenter)
		self.set_min_width(self.datatable, 2)
		self.set_min_width(self.datatable_selector, 3)
		return layout

	### data processing actions ###
	def choose_folder_data(self):
		fd = QFileDialog()
		filepath = fd.getExistingDirectory(self, 'Data Folder', IfesUI.homedir)
		if filepath:
			self.folder_txtbx_data.setText(filepath)
			self.file_txtbx_data.setText('')

	def choose_files_data(self):
		fd = QFileDialog()
		files, _ = fd.getOpenFileNames(self, 'Data Files', IfesUI.homedir)
		if files:
			names = [os.path.basename(f) for f in files]
			folder = os.path.dirname(files[0])
			self.file_txtbx_data.setText('; '.join(names))
			self.folder_txtbx_data.setText(folder)

	def folder_action_data(self):
		try:
			folder = self.folder_txtbx_data.text()
			self.datahandler.set_folder(folder)
			self.file_action_data()
		except Exception as e:
			self.update_status('ERROR: ' + str(e))

	def file_action_data(self):
		file_str = self.file_txtbx_data.text()
		folder = self.folder_txtbx_data.text()
		try:
			if not file_str:
				files = self.get_all_files(folder, valid=utils.valid_types)
				self.file_txtbx_data.setText('; '.join(files))
			else:
				files = file_str.split('; ')
			files = [os.path.join(folder, f) for f in files]
			self.datahandler.set_files(files)
		except Exception as e:
			self.update_status('ERROR: ' + str(e))

	def protocol_action(self):
		new_protocol = self.protocol_menu.currentText()
		protocol_code = IfesUI.expt_types[new_protocol]
		self.datahandler.expt_type = protocol_code
		if protocol_code == 'cv' or protocol_code == 'lsv':
			self.colone_lbl.setText('Potential column')
			self.colone_txtbx.setText('0')
			# self.colone_txtbx.setFixedWidth(60)
			self.coltwo_lbl.setText('Current column')
			self.coltwo_txtbx.setText('1')
			# self.coltwo_txtbx.setFixedWidth(60)
			self.colthree_lbl.setText('No Enter')
			self.colthree_txtbx.setText(' ')
			# self.colthree_txtbx.setFixedWidth(60)
			self.colfour_lbl.setText('No Enter')
			self.colfour_txtbx.setText(' ')
			# self.colfour_txtbx.setFixedWidth(60)
			self.colfive_lbl.setText('No Enter')
			self.colfive_txtbx.setText(' ')
			# self.colfive_txtbx.setFixedWidth(60)
			self.area_txtbx.setEnabled(True)
			self.refelec_menu.setEnabled(True)
			self.rxn_menu.setEnabled(True)
			self.pyr_chkbx.setEnabled(False)
			self.ststpts_txtbx.setEnabled(False)
		elif protocol_code == 'ca' or protocol_code == 'cp':
			self.colone_lbl.setText('Potential column')
			self.colone_txtbx.setText('1')
			# self.colone_txtbx.setFixedWidth(60)
			self.coltwo_lbl.setText('Current column')
			self.coltwo_txtbx.setText('2')
			# self.coltwo_txtbx.setFixedWidth(60)
			self.colthree_lbl.setText('No Enter')
			self.colthree_txtbx.setText(' ')
			# self.colthree_txtbx.setFixedWidth(60)
			self.colfour_lbl.setText('No Enter')
			self.colfour_txtbx.setText(' ')
			# self.colfour_txtbx.setFixedWidth(60)
			self.colfive_lbl.setText('No Enter')
			self.colfive_txtbx.setText(' ')
			# self.colfive_txtbx.setFixedWidth(60)
			self.area_txtbx.setEnabled(True)
			self.area_txtbx.setEnabled(True)
			self.refelec_menu.setEnabled(True)
			self.rxn_menu.setEnabled(True)
			self.pyr_chkbx.setEnabled(True)
			self.ststpts_txtbx.setEnabled(True)
		elif protocol_code=='eis':
			self.colone_lbl.setText('Voltage column in V')
			self.colone_txtbx.setText('2')
			# self.colone_txtbx.setFixedWidth(60)
			self.coltwo_lbl.setText('Current column in A')
			self.coltwo_txtbx.setText('3')
			# self.coltwo_txtbx.setFixedWidth(60)
			self.colthree_lbl.setText('Frequency column in Hz')
			self.colthree_txtbx.setText('4')
			# self.colthree_txtbx.setFixedWidth(60)
			self.colfour_lbl.setText('Real column in \u03A9')
			self.colfour_txtbx.setText('5')
			# self.colfour_txtbx.setFixedWidth(60)
			self.colfive_lbl.setText('Imaginary column in \u03A9')
			self.colfive_txtbx.setText('6')
			# self.colfive_txtbx.setFixedWidth(60)
			self.area_txtbx.setEnabled(True)
			self.refelec_menu.setEnabled(False)
			self.rxn_menu.setEnabled(False)
			self.pyr_chkbx.setEnabled(False)
			self.ststpts_txtbx.setEnabled(False)

	def colone_action(self):
		col = self.colone_txtbx.text()
		if col.isdigit():
			col = int(col)
		self.datahandler.set_colone(col)

	def coltwo_action(self):
		col = self.coltwo_txtbx.text()
		if col.isdigit():
			col = int(col)
		self.datahandler.set_coltwo(col)

	def colthree_action(self):
		col = self.colthree_txtbx.text()
		if col.isdigit():
			col = int(col)
		self.datahandler.set_colthree(col)

	def colfour_action(self):
		col = self.colfour_txtbx.text()
		if col.isdigit():
			col = int(col)
		self.datahandler.set_colfour(col)

	def colfive_action(self):
		col = self.colfive_txtbx.text()
		if col.isdigit():
			col = int(col)
		self.datahandler.set_colfive(col)

	def colsix_action(self):
		col = self.colsix_txtbx.text()
		if col.isdigit():
			col = int(col)
		self.datahandler.set_colsix(col)


	def area_action(self):
		area = self.area_txtbx.text()
		try:
			area = float(area)
			self.datahandler.set_area(area)
		except ValueError as e:
			self.update_status('MEA area must be a number')

	def maxfreq_action(self):
		maxfreq = self.maxfreq_txtbx.text()
		try:
			maxfreq = float(maxfreq)
			self.datahandler.set_maxfreq(maxfreq)
		except ValueError as e:
			self.update_status('Max frequency must be a number')

	def voltage_factor_action(self):
		voltage_factor = self.voltage_factor_txtbx.text()
		try:
			voltage_factor = float(voltage_factor)
			self.datahandler.set_voltage_factor(voltage_factor)
		except ValueError as e:
			self.update_status('Factor must be a number')

	def current_factor_action(self):
		current_factor = self.current_factor_txtbx.text()
		try:
			current_factor = float(current_factor)
			self.datahandler.set_current_factor(current_factor)
		except ValueError as e:
			self.update_status('Factor must be a number')

	def negative_imaginary_action(self):
		negative_imaginary = self.negative_imaginary_txtbx.text()
		try:
			negative_imaginary = float(negative_imaginary)
			self.datahandler.set_negative_imaginary(negative_imaginary)
		except ValueError as e:
			self.update_status('Factor must be a number')


	def refelec_menu_action(self):
		elec = self.refelec_menu.currentText()
		for name in IfesUI.refelecs.keys():
			if name in elec.lower():
				val = IfesUI.refelecs[name]
				self.refelec_txtbx.setEnabled(False)
				break
		else:
			val = 0
			self.refelec_txtbx.setEnabled(True)
		self.refelec_txtbx.setText(str(val))

	def refelec_txtbx_action(self):
		val = self.refelec_txtbx.text()
		try:
			val = float(val)
		except ValueError:
			val = 0
			self.update_status('Reference electrode potential must be a number')
		self.datahandler.set_refelec(val)

	def rxn_menu_action(self):
		rxn = self.rxn_menu.currentText()
		for name in IfesUI.thermo_potentials.keys():
			if name in rxn.lower():
				val = IfesUI.thermo_potentials[name]
				self.rxn_txtbx.setEnabled(False)
				break
		else:
			val = 0
			self.rxn_txtbx.setEnabled(True)
		self.rxn_txtbx.setText(str(val))

	def rxn_txtbx_action(self):
		val = self.rxn_txtbx.text()
		try:
			val = float(val)
		except ValueError:
			val = 0
			self.update_status('Thermodynamic potential must be a number')
		self.datahandler.set_rxn(val)

	def pyr_action(self):
		state = self.pyr_chkbx.isChecked()
		self.datahandler.set_pyr(state)

	def ststpts_action(self):
		pts = self.ststpts_txtbx.text()
		try:
			pts = int(pts)
			self.datahandler.set_pts_to_avg(pts)
		except ValueError:
			self.update_status('Steady state points must be a number')

	def savechkbx_action(self):
		state = self.save_chkbx_data.isChecked()
		
		self.saveloc_txtbx_data.setEnabled(state)
		self.saveloc_btn_data.setEnabled(state)
		self.datahandler.set_export_data(state)

	def choose_saveloc_data(self):
		fd = QFileDialog()
		folder = fd.getExistingDirectory(self, 'Save Location', self.default_saveloc_data())
		if not folder:
			folder = self.default_saveloc_data()
		self.saveloc_txtbx_data.setText(folder)

	def saveloc_action_data(self):
		folder = self.saveloc_txtbx_data.text()
		self.datahandler.set_saveloc(folder)
		# self.folder_txtbx_upload.setText(folder)

	def process_action(self):
		try:
			self.datahandler.process_data()
			data = self.datahandler.get_data()
			self.vishandler.set_data(data)
			self.datatable_selector.clear()
			if data:
				self.datatable_selector.setEnabled(True)
				self.data_dict = {d.get_name():d.get_processed_data() for d in data if d.get_processed_data() is not None}
				for name in self.data_dict.keys():
					self.datatable_selector.addItem(name)
				self.datatable_selector.setCurrentText(list(self.data_dict.keys())[0])
				self.update_table(list(self.data_dict.values())[0])
				self.useexisting_chkbx_vis.setCheckState(Qt.Checked)
			else:
				self.datatable_selector.setEnabled(False)
				self.useexisting_chkbx_vis.setCheckState(Qt.Unchecked)
			self.update_status('Data processed successfully')
			self.draw_plot_vis()
		except AttributeError as e:
			self.update_status('All selected files must match the selected experiment type')
		except Exception as e:
			self.update_status('ERROR: ' + str(e))

	def datatable_selector_action(self):
		try:
			name = self.datatable_selector.currentText()
			data = self.data_dict[name]
			self.update_table(data)
		except Exception as e:
			self.update_status('ERROR: ' + str(e))

	def update_table(self, data):
		self.datamodel = TableModel(data)
		self.datatable.setModel(self.datamodel)
		header = self.datatable.horizontalHeader()
		header.setSectionResizeMode(QHeaderView.Stretch)
		for i in range(header.count()):
			w = header.sectionSize(i)
			header.setSectionResizeMode(i, QHeaderView.Interactive)
			header.resizeSection(i, w)

	def default_saveloc_data(self):
		dataloc = self.folder_txtbx_data.text()
		saveloc = os.path.join(dataloc, 'processed')
		if not os.path.exists(saveloc):
			os.mkdir(saveloc)
		return saveloc

	######################
	# Data Visualization #
	######################
	### data visualization layout ###
	def visuals_layout(self):
		# data selection header
		self.header_visdata = QLabel('Select Data')
		self.header_visdata.setFont(IfesUI.headerfont)
		# use existing widgets
		self.useexisting_chkbx_vis = QCheckBox('Use previously loaded data')
		self.useexisting_chkbx_vis.setCheckState(Qt.Unchecked)
		# folder selection widgets
		self.folder_lbl_vis = QLabel('Data folder')
		self.folder_txtbx_vis = QLineEdit(IfesUI.homedir)
		self.folder_btn_vis = QPushButton('Choose folder...')
		#file selection widgets
		self.file_lbl_vis = QLabel('Data files')
		self.file_txtbx_vis = QLineEdit()
		self.file_btn_vis = QPushButton('Choose files...')
		# load data button
		self.loaddata_btn_vis = QPushButton('Load data')
		#figure layout
		self.figlayout_vis = self.figure_layout_vis()
		# save plot header
		self.header_saveplot_vis = QLabel('Save Plot')
		self.header_saveplot_vis.setFont(IfesUI.headerfont)
		# save plot widgets
		self.saveloc_lbl_vis = QLabel('Save location')
		self.saveloc_txtbx_vis = QLineEdit(self.default_saveloc_vis())
		self.saveloc_btn_vis = QPushButton('Choose location...')
		self.save_btn_vis = QPushButton('Save Current Figure')
		# connect widgets
		self.useexisting_chkbx_vis.stateChanged.connect(self.useexisting_action_vis)
		self.folder_txtbx_vis.textChanged.connect(self.folder_action_vis)
		self.folder_btn_vis.clicked.connect(self.choose_folder_vis)
		self.file_txtbx_vis.textChanged.connect(self.file_action_vis)
		self.file_btn_vis.clicked.connect(self.choose_files_vis)
		self.loaddata_btn_vis.clicked.connect(self.loaddata_action_vis)
		self.saveloc_btn_vis.clicked.connect(self.choose_saveloc_vis)
		self.save_btn_vis.clicked.connect(self.save_action_vis)
		# build layout
		layout = QGridLayout()
		row = 0
		# layout.addWidget(self.header_visdata, row, 0, 1, -1, Qt.AlignHCenter)
		# row += 1
		# layout.addWidget(self.useexisting_chkbx_vis, row, 0, 1, -1, Qt.AlignLeft)
		# row += 1
		# layout.addWidget(self.folder_lbl_vis, row, 0)
		# layout.addWidget(self.folder_txtbx_vis, row, 1)
		# layout.addWidget(self.folder_btn_vis, row, 2)
		# row += 1
		# layout.addWidget(self.file_lbl_vis, row, 0)
		# layout.addWidget(self.file_txtbx_vis, row, 1)
		# layout.addWidget(self.file_btn_vis, row, 2)
		# row += 1
		# layout.addWidget(self.loaddata_btn_vis, row, 0, 1, -1, Qt.AlignHCenter)
		# row += 1
		layout.addLayout(self.figlayout_vis, row, 0, 1, -1, Qt.AlignLeft)
		row += 1
		layout.addWidget(self.header_saveplot_vis, row, 0, 1, -1, Qt.AlignHCenter)
		row += 1
		layout.addWidget(self.saveloc_lbl_vis, row, 0)
		layout.addWidget(self.saveloc_txtbx_vis, row, 1)
		layout.addWidget(self.saveloc_btn_vis, row, 2)
		row += 1
		layout.addWidget(self.save_btn_vis, row, 0, 1, -1, Qt.AlignHCenter)
		return layout

	def figure_layout_vis(self):
		# plot features header
		self.header_plotparams_vis = QLabel('Plot Options')
		self.header_plotparams_vis.setFont(IfesUI.headerfont)
		# visualization selection widgets
		self.vistype_lbl = QLabel('Visualization type')
		self.vistype_menu = QComboBox()
		for name in list(IfesUI.vis_types.keys()):
			self.vistype_menu.addItem(name)
		# column selection layout
		self.colslayout_vis = self.colselection_layout_vis()
		# plot features
		self.plotfeatures_vis = self.plotfeatures_layout_vis()
		# actual figure
		self.figcanvas_vis  = FigureCanvas(Figure(figsize=IfesUI.default_figsize))
		self.figcanvas_vis.figure.subplots()

		# line properties header
		self.header_lineprops_vis = QLabel('Line Options')
		self.header_lineprops_vis.setFont(IfesUI.headerfont)
		# line selector menu
		self.lineselector_lbl_vis = QLabel('line')
		self.lineselector_menu_vis = QComboBox()
		# for n in IfesUI.tintin:
		# 	self.lineselector_menu_vis.addItem(n)
		# line properties layout
		self.lineprops_vis = self.lineprops_layout_vis()
		# figure properties
		self.figprops_vis = self.figprops_layout_vis()
		# connect widgets
		self.vistype_menu.currentTextChanged.connect(self.vistype_action)
		self.lineselector_menu_vis.currentTextChanged.connect(self.lineselector_action_vis)
		# build layout
		layout = QGridLayout()
		layout.addWidget(self.header_plotparams_vis, 0, 0, 1, 2, Qt.AlignHCenter)
		# layout.addWidget(self.vistype_lbl, 1, 0, Qt.AlignLeft)
		# layout.addWidget(self.vistype_menu, 1, 1, Qt.AlignLeft)
		# layout.addLayout(self.colslayout_vis, 2, 0, 1, 2, Qt.AlignLeft)
		layout.addLayout(self.plotfeatures_vis, 2, 0, 1, 2, Qt.AlignLeft)
		layout.addWidget(self.figcanvas_vis, 0, 2, 4, 1, Qt.AlignHCenter)
		layout.addLayout(self.figprops_vis, 4, 2, 1, 1, Qt.AlignHCenter)
		layout.addWidget(self.header_lineprops_vis, 0, 3, 1, 2, Qt.AlignHCenter)
		# layout.addWidget(self.lineselector_lbl_vis, 1, 3, Qt.AlignLeft)
		# layout.addWidget(self.lineselector_menu_vis, 1, 4, Qt.AlignLeft)
		layout.addLayout(self.lineprops_vis, 1, 3, 2, 2, Qt.AlignLeft)
		self.set_min_width(self.lineselector_menu_vis, 1)
		return layout

	def colselection_layout_vis(self):
		# x column
		self.xcol_lbl_vis = QLabel('x column')
		self.xcol_txtbx_vis = QLineEdit('0')
		# y column
		self.ycol_lbl_vis = QLabel('y column')
		self.ycol_txtbx_vis = QLineEdit('1')
		# error column
		self.ecol_lbl_vis = QLabel('error column')
		self.ecol_txtbx_vis = QLineEdit('3')
		# build layout
		layout = QGridLayout()
		# row = 0
		# layout.addWidget(self.xcol_lbl_vis, row, 0, Qt.AlignLeft)
		# layout.addWidget(self.xcol_txtbx_vis, row, 1, Qt.AlignLeft)
		# row += 1
		# layout.addWidget(self.ycol_lbl_vis, row, 0, Qt.AlignLeft)
		# layout.addWidget(self.ycol_txtbx_vis, row, 1, Qt.AlignLeft)
		# row += 1
		# layout.addWidget(self.ecol_lbl_vis, row, 0, Qt.AlignLeft)
		# layout.addWidget(self.ecol_txtbx_vis, row, 1, Qt.AlignLeft)
		# # connect widgets
		# self.xcol_txtbx_vis.textChanged.connect(self.xcol_action_vis)
		# self.ycol_txtbx_vis.textChanged.connect(self.ycol_action_vis)
		# self.ecol_txtbx_vis.textChanged.connect(self.ecol_action_vis)
		# resize widgets
		for i in range(layout.count()):
			w = layout.itemAt(i).widget()
			if isinstance(w, QLineEdit):
				self.set_max_width(w, 1.5)
		return layout

	def plotfeatures_layout_vis(self):
		# draw lines
		self.drawline_lbl_vis = QLabel('Draw lines')
		self.drawlines_chkbx_vis = QCheckBox()
		self.drawlines_chkbx_vis.setCheckState(Qt.Unchecked)
		# draw data points
		self.drawscatter_lbl_vis = QLabel('Draw data points')
		self.drawscatter_chkbx_vis = QCheckBox()
		self.drawscatter_chkbx_vis.setCheckState(Qt.Checked)
		#draw error bars
		self.drawerror_lbl_vis = QLabel('Draw error bars')
		self.drawerror_chkbx_vis = QCheckBox()
		self.drawerror_chkbx_vis.setCheckState(Qt.Unchecked)
		# raw data selector
		self.showleg_lbl_vis = QLabel('Show legend')
		self.showleg_chkbx_vis = QCheckBox()
		self.showleg_chkbx_vis.setCheckState(Qt.Checked)
		self.showleg_chkbx_vis.setEnabled(True)
		# x-axis label
		self.xlabel_lbl_vis = QLabel('x-axis label')
		self.xlabel_txtbx_vis = QLineEdit('Current Density in $A/cm^2$')
		# y-axis label
		self.ylabel_lbl_vis = QLabel('y-axis label')
		self.ylabel_txtbx_vis = QLineEdit('Voltage in V')
		# x-axis limits
		self.xmin_lbl_vis = QLabel('x min')
		self.xmin_txtbx_vis = QLineEdit()
		self.xmax_lbl_vis = QLabel('x max')
		self.xmax_txtbx_vis = QLineEdit()
		# y-axis limits
		self.ymin_lbl_vis = QLabel('y min')
		self.ymin_txtbx_vis = QLineEdit()
		self.ymax_lbl_vis = QLabel('y max')
		self.ymax_txtbx_vis = QLineEdit()
		# clear plot
		self.clear_lbl_vis = QLabel('Clear Plot Data')
		self.clear_btn_vis = QPushButton('Clear Plot')
		self.clear_lbl_vis.setFont(IfesUI.valuefont)
		# connect widgets
		self.drawlines_chkbx_vis.stateChanged.connect(self.drawlines_action_vis)
		self.drawscatter_chkbx_vis.stateChanged.connect(self.drawscatter_action_vis)
		self.drawerror_chkbx_vis.stateChanged.connect(self.drawerror_action_vis)
		self.showleg_chkbx_vis.stateChanged.connect(self.shwowleg_action_vis)
		self.xlabel_txtbx_vis.textChanged.connect(self.xlabel_action_vis)
		self.ylabel_txtbx_vis.textChanged.connect(self.ylabel_action_vis)
		self.xmin_txtbx_vis.textChanged.connect(self.xlim_action_vis)
		self.xmax_txtbx_vis.textChanged.connect(self.xlim_action_vis)
		self.ymin_txtbx_vis.textChanged.connect(self.ylim_action_vis)
		self.ymax_txtbx_vis.textChanged.connect(self.ylim_action_vis)
		self.clear_btn_vis.clicked.connect(self.clear_action_vis)
		# build layout
		layout = QGridLayout()
		row = 0
		layout.addWidget(self.drawline_lbl_vis, row, 0, 1, 2, Qt.AlignLeft)
		layout.addWidget(self.drawlines_chkbx_vis, row, 2, 1, 2, Qt.AlignLeft)
		row += 1
		layout.addWidget(self.drawscatter_lbl_vis, row, 0, 1, 2, Qt.AlignLeft)
		layout.addWidget(self.drawscatter_chkbx_vis, row, 2, 1, 2, Qt.AlignLeft)
		row += 1
		layout.addWidget(self.drawerror_lbl_vis, row, 0, 1, 2, Qt.AlignLeft)
		layout.addWidget(self.drawerror_chkbx_vis, row, 2, 1, 2, Qt.AlignLeft)
		row += 1
		layout.addWidget(self.showleg_lbl_vis, row, 0, 1, 2, Qt.AlignLeft)
		layout.addWidget(self.showleg_chkbx_vis, row, 2, 1, 2, Qt.AlignLeft)
		row += 1
		layout.addWidget(self.xlabel_lbl_vis, row, 0, 1, 2, Qt.AlignLeft)
		layout.addWidget(self.xlabel_txtbx_vis, row, 2, 1, 2, Qt.AlignLeft)
		row += 1
		layout.addWidget(self.ylabel_lbl_vis, row, 0, 1, 2, Qt.AlignLeft)
		layout.addWidget(self.ylabel_txtbx_vis, row, 2, 1, 2, Qt.AlignLeft)
		row += 1
		layout.addWidget(self.xmin_lbl_vis, row, 0, Qt.AlignLeft)
		layout.addWidget(self.xmin_txtbx_vis, row, 1, Qt.AlignLeft)
		layout.addWidget(self.xmax_lbl_vis, row, 2, Qt.AlignLeft)
		layout.addWidget(self.xmax_txtbx_vis, row, 3, Qt.AlignLeft)
		row += 1
		layout.addWidget(self.ymin_lbl_vis, row, 0, Qt.AlignLeft)
		layout.addWidget(self.ymin_txtbx_vis, row, 1, Qt.AlignLeft)
		layout.addWidget(self.ymax_lbl_vis, row, 2, Qt.AlignLeft)
		layout.addWidget(self.ymax_txtbx_vis, row, 3, Qt.AlignLeft)
		row += 1
		layout.addWidget(self.clear_lbl_vis, row, 0, 1, -1, Qt.AlignHCenter)
		row += 1
		layout.addWidget(self.clear_btn_vis, row, 0, 1, -1, Qt.AlignHCenter)
		# resize widgets
		for i in range(layout.count()):
			w = layout.itemAt(i).widget()
			if isinstance(w, QLineEdit):
				self.set_min_height(w)
				# self.set_min_width(w)
		self.set_max_width(self.xmin_txtbx_vis, 0.5)
		self.set_max_width(self.xmax_txtbx_vis, 0.5)
		self.set_max_width(self.ymin_txtbx_vis, 0.5)
		self.set_max_width(self.ymax_txtbx_vis, 0.5)
		return layout

	def figprops_layout_vis(self):
		# fig width
		self.figw_lbl_vis = QLabel('Figure width')
		self.figw_txtbx_vis = QLineEdit(str(IfesUI.default_figsize[0]))
		# fig height
		self.figh_lbl_vis = QLabel('Figue height')
		self.figh_txtbx_vis = QLineEdit(str(IfesUI.default_figsize[1]))
		# fig resolution
		self.figres_lbl_vis = QLabel('Figure resolution (DPI)')
		self.figres_txtbx_vis = QLineEdit(str(IfesUI.default_figres))
		# connect widgets
		self.figw_txtbx_vis.textChanged.connect(self.figsize_action_vis)
		self.figh_txtbx_vis.textChanged.connect(self.figsize_action_vis)
		# build layout
		layout = QGridLayout()
		row = 0
		layout.addWidget(self.figw_lbl_vis, row, 0, Qt.AlignHCenter)
		layout.addWidget(self.figh_lbl_vis, row, 1, Qt.AlignHCenter)
		layout.addWidget(self.figres_lbl_vis, row, 2, Qt.AlignHCenter)
		row += 1
		layout.addWidget(self.figw_txtbx_vis, row, 0, Qt.AlignHCenter)
		layout.addWidget(self.figh_txtbx_vis, row, 1, Qt.AlignHCenter)
		layout.addWidget(self.figres_txtbx_vis, row, 2, Qt.AlignHCenter)
		for i in range(layout.count()):
			w = layout.itemAt(i).widget()
			if isinstance(w, QLineEdit):
				self.set_max_width(w, 0.75)
		return layout

	def lineprops_layout_vis(self):
		# label
		self.linelbl_lbl_vis = QLabel('Label')
		self.linelbl_txtbx_vis = QLineEdit()
		# line color
		self.linecolor_lbl_vis = QLabel('Color')
		self.linecolor_btn_vis = QPushButton('Choose color...')
		# line style
		self.linestyle_lbl_vis = QLabel('Line style')
		self.linestyle_menu_vis = QComboBox()
		for ls in Line2D.lineStyles.keys():
			if Line2D.lineStyles[ls] != '_draw_nothing'	:
				self.linestyle_menu_vis.addItem(ls)
		self.linestyle_menu_vis.addItem('None')
		# line width
		self.linewidth_lbl_vis = QLabel('Line width')
		self.linewidth_txtbx_vis = QDoubleSpinBox()
		self.linewidth_txtbx_vis.setDecimals(1)
		self.linewidth_txtbx_vis.setMinimum(0.1)
		self.linewidth_txtbx_vis.setSingleStep(0.5)
		self.linewidth_txtbx_vis.setValue(1)
		# marker style
		self.marekerstyle_lbl_vis = QLabel('Marker style')
		self.markerstyle_menu_vis = QComboBox()
		for ms in Line2D.filled_markers:
			self.markerstyle_menu_vis.addItem(Line2D.markers[ms])
		self.markerstyle_menu_vis.addItem('None')
		# marker size
		self.markersize_lbl_vis = QLabel('Marker size')
		self.markersize_txtbx_vis = QSpinBox()
		self.markersize_txtbx_vis.setMinimum(1)
		# connect widgets
		self.linelbl_txtbx_vis.textChanged.connect(self.linelbl_action_vis)
		self.linecolor_btn_vis.clicked.connect(self.linecolor_action_vis)
		self.linestyle_menu_vis.currentTextChanged.connect(self.linestyle_action_vis)
		self.linewidth_txtbx_vis.valueChanged.connect(self.linewidth_action_vis)
		self.markerstyle_menu_vis.currentTextChanged.connect(self.markerstyle_action_vis)
		self.markersize_txtbx_vis.valueChanged.connect(self.markersize_action_vis)
		# build layout
		layout = QGridLayout()
		row = 0
		layout.addWidget(self.linelbl_lbl_vis, row, 0)
		layout.addWidget(self.linelbl_txtbx_vis, row, 1)
		row += 1
		layout.addWidget(self.linecolor_lbl_vis, row, 0)
		layout.addWidget(self.linecolor_btn_vis, row, 1)
		row += 1
		layout.addWidget(self.linestyle_lbl_vis, row, 0)
		layout.addWidget(self.linestyle_menu_vis, row, 1)
		row += 1
		layout.addWidget(self.linewidth_lbl_vis, row, 0)
		layout.addWidget(self.linewidth_txtbx_vis, row, 1)
		row += 1
		layout.addWidget(self.marekerstyle_lbl_vis, row, 0)
		layout.addWidget(self.markerstyle_menu_vis, row, 1)
		row += 1
		layout.addWidget(self.markersize_lbl_vis, row, 0)
		layout.addWidget(self.markersize_txtbx_vis, row, 1)
		return layout

	### data visualization actions ###
	def useexisting_action_vis(self):
		state = self.useexisting_chkbx_vis.isChecked()
		if state:
			if not self.datahandler.get_data():
				self.update_status('No data to visualize')
				self.useexisting_chkbx_vis.setCheckState(Qt.Unchecked)
				state = False
			else:
				self.vishandler.set_data(self.datahandler.get_data())
		self.folder_lbl_vis.setEnabled(not state)
		self.folder_txtbx_vis.setEnabled(not state)
		self.folder_btn_vis.setEnabled(not state)
		self.file_lbl_vis.setEnabled(not state)
		self.file_txtbx_vis.setEnabled(not state)
		self.file_btn_vis.setEnabled(not state)
		self.loaddata_btn_vis.setEnabled(not state)
		if state:
			self.draw_plot_vis()

	def choose_folder_vis(self):
		fd = QFileDialog()
		filepath = fd.getExistingDirectory(self, 'Data Folder', IfesUI.homedir)
		if filepath:
			self.folder_txtbx_vis.setText(filepath)
			self.file_txtbx_vis.setText('')

	def choose_files_vis(self):
		fd = QFileDialog()
		files, _ = fd.getOpenFileNames(self, 'Data Files', IfesUI.homedir)
		if files:
			names = [os.path.basename(f) for f in files]
			folder = os.path.dirname(files[0])
			self.file_txtbx_vis.setText('; '.join(names))
			self.folder_txtbx_vis.setText(folder)

	def folder_action_vis(self):
		try:
			folder = self.folder_txtbx_vis.text()
			self.vishandler.set_datafolder(folder)
			self.file_action_vis()
		except Exception as e:
			self.update_status('ERROR: ' + str(e))

	def file_action_vis(self):
		file_str = self.file_txtbx_vis.text()
		folder = self.folder_txtbx_vis.text()
		try:
			if not file_str:
				files = self.get_all_files(folder, valid=utils.valid_types)
				self.file_txtbx_vis.setText('; '.join(files))
			else:
				files = file_str.split('; ')
			files = [os.path.join(folder, f) for f in files]
			self.vishandler.set_datafiles(files)
		except Exception as e:
			self.update_status('ERROR: ' + str(e))

	def loaddata_action_vis(self):
		try:
			self.vishandler.load_data()
			self.draw_plot_vis()
		except Exception as e:
			self.update_status('ERROR: ' + str(e))

	def vistype_action(self):
		vistype = self.vistype_menu.currentText()
		viscode = IfesUI.vis_types[vistype]
		if viscode == 0:
			self.xcol_lbl_vis.setText('Current Column')
			self.xcol_txtbx_vis.setText('0')
			self.ycol_lbl_vis.setText('Potential Column')
			self.ycol_txtbx_vis.setText('1')
			self.ecol_txtbx_vis.setText('3')
			self.drawlines_chkbx_vis.setCheckState(Qt.Checked)
			self.drawscatter_chkbx_vis.setCheckState(Qt.Checked)
			self.drawerror_chkbx_vis.setCheckState(Qt.Unchecked)
			self.showleg_chkbx_vis.setCheckState(Qt.Checked)
			self.xlabel_txtbx_vis.setText('Current Density [$mA/cm^2$]')
			self.ylabel_txtbx_vis.setText('Potential [V]')
		elif viscode == 1:
			self.xcol_lbl_vis.setText('Potential Column')
			self.xcol_txtbx_vis.setText('1')
			self.ycol_lbl_vis.setText('Current Column')
			self.ycol_txtbx_vis.setText('0')
			self.ecol_txtbx_vis.setText('3')
			self.drawlines_chkbx_vis.setCheckState(Qt.Checked)
			self.drawscatter_chkbx_vis.setCheckState(Qt.Unchecked)
			self.drawerror_chkbx_vis.setCheckState(Qt.Unchecked)
			self.showleg_chkbx_vis.setCheckState(Qt.Checked)
			self.xlabel_txtbx_vis.setText('Potential [V]')
			self.ylabel_txtbx_vis.setText('Current Density [$mA/cm^2$]')
		elif viscode == 2:
			self.xcol_lbl_vis.setText('Potential Column')
			self.xcol_txtbx_vis.setText('2')
			self.ycol_lbl_vis.setText('Current Column')
			self.ycol_txtbx_vis.setText('1')
			self.ecol_txtbx_vis.setText('')
			self.drawlines_chkbx_vis.setCheckState(Qt.Unchecked)
			self.drawscatter_chkbx_vis.setCheckState(Qt.Checked)
			self.drawerror_chkbx_vis.setCheckState(Qt.Unchecked)
			self.showleg_chkbx_vis.setCheckState(Qt.Checked)
			self.xlabel_txtbx_vis.setText('Overpotential [V]')
			self.ylabel_txtbx_vis.setText('Current Density [$mA/cm^2$]')
		elif viscode == 3:
			self.xcol_lbl_vis.setText('Real Column')
			self.xcol_txtbx_vis.setText('0')
			self.ycol_lbl_vis.setText('Imaginary Column')
			self.ycol_txtbx_vis.setText('1')
			self.ecol_txtbx_vis.setText('')
			self.drawlines_chkbx_vis.setCheckState(Qt.Unchecked)
			self.drawscatter_chkbx_vis.setCheckState(Qt.Checked)
			self.drawerror_chkbx_vis.setCheckState(Qt.Unchecked)
			self.showleg_chkbx_vis.setCheckState(Qt.Checked)
			self.xlabel_txtbx_vis.setText('$Z_{Re} [\Omega]$')
			self.ylabel_txtbx_vis.setText('$Z_{Im} [\Omega]$')
		self.vishandler.set_vis_code(viscode)
		if viscode == 3:
			self.useexisting_chkbx_eis.setCheckState(Qt.Checked)
			self.draw_plot_eis()
		self.draw_plot_vis()

	def xcol_action_vis(self):
		col = self.xcol_txtbx_vis.text()
		if col.isdigit():
			col = int(col)
		self.vishandler.set_xcol(col)
		self.draw_plot_vis()

	def ycol_action_vis(self):
		col = self.ycol_txtbx_vis.text()
		if col.isdigit():
			col = int(col)
		self.vishandler.set_ycol(col)
		self.draw_plot_vis()

	def ecol_action_vis(self):
		col = self.ecol_txtbx_vis.text()
		if col.isdigit():
			col = int(col)
		self.vishandler.set_ecol(col)
		self.draw_plot_vis()

	def drawlines_action_vis(self):
		state = self.drawlines_chkbx_vis.isChecked()
		self.vishandler.set_drawline(state)
		if state:
			ls = '-'
		else:
			ls = ''
		ax = self.get_ax_vis()
		lines = ax.get_lines()
		for i, l in enumerate(lines):
			if self.drawerror_chkbx_vis.isChecked() and i%3 != 0:
				continue
			l.set_linestyle(ls)
		self.figcanvas_vis.draw()

	def drawscatter_action_vis(self):
		state = self.drawscatter_chkbx_vis.isChecked()
		self.vishandler.set_drawscatter(state)
		if state:
			ms = '.'
		else:
			ms = ''
		ax = self.get_ax_vis()
		lines = ax.get_lines()
		for i, l in enumerate(lines):
			if self.drawerror_chkbx_vis.isChecked() and i%3 !=0:
				continue
			l.set_marker(ms)
		self.figcanvas_vis.draw()

	def drawerror_action_vis(self):
		state = self.drawerror_chkbx_vis.isChecked()
		self.vishandler.set_drawerr(state)
		self.draw_plot_vis()

	def shwowleg_action_vis(self):
		state = self.showleg_chkbx_vis.isChecked()
		ax = self.get_ax_vis()
		if state:
			ax.legend(loc='best', edgecolor='#000000')
		else:
			ax.legend().remove()
		self.figcanvas_vis.draw()

	def xlabel_action_vis(self):
		new_label = self.xlabel_txtbx_vis.text()
		ax = self.get_ax_vis()
		ax.set_xlabel(new_label)
		self.figcanvas_vis.draw()

	def ylabel_action_vis(self):
		new_label = self.ylabel_txtbx_vis.text()
		ax = self.get_ax_vis()
		ax.set_ylabel(new_label)
		self.figcanvas_vis.draw()

	def xlim_action_vis(self):
		xmin_text = self.xmin_txtbx_vis.text()
		xmax_text = self.xmax_txtbx_vis.text()
		ax = self.get_ax_vis()
		try:
			xmin = float(xmin_text)
			ax.set_xbound(lower=xmin)
		except ValueError:
			self.update_status('xmin must be a number')
		try:
			xmax = float(xmax_text)
			ax.set_xbound(upper=xmax)
		except ValueError:
			self.update_status('xmax must be a number')
		self.figcanvas_vis.draw()

	def ylim_action_vis(self):
		ymin_text = self.ymin_txtbx_vis.text()
		ymax_text = self.ymax_txtbx_vis.text()
		ax = self.get_ax_vis()
		try:
			ymin = float(ymin_text)
			ax.set_ybound(lower=ymin)
		except ValueError:
			self.update_status('ymin must be a number')
		try:
			ymax = float(ymax_text)
			ax.set_ybound(upper=ymax)
		except ValueError:
			self.update_status('ymax must be a number')
		self.figcanvas_vis.draw()

	def clear_action_vis(self):
		self.vishandler.set_data([], replace=True)
		fig = self.figcanvas_vis.figure
		fig.clf()
		self.lineselector_menu_vis.clear()
		self.useexisting_chkbx_vis.setCheckState(Qt.Unchecked)

	def figsize_action_vis(self):
		fig = self.figcanvas_vis.figure
		width = self.figw_txtbx_vis.text()
		height = self.figh_txtbx_vis.text()
		try:
			width = float(width)
			height = float(height)
			fig.set_figwidth(width)
			fig.set_figheight(height)
			self.figcanvas_vis.draw()
		except ValueError:
			self.update_status('Figure width and height must be numbers')

	def lineselector_action_vis(self):
		try:
			label = self.lineselector_menu_vis.currentText()
			data = self.line_dict_vis[label]
			line = data.get_line()
			linestyle = line.get_linestyle()
			linewidth = line.get_linewidth()
			markerstyle = line.get_marker()
			markersize = line.get_markersize()
			self.linelbl_txtbx_vis.setText(label)
			self.linestyle_menu_vis.setCurrentText(linestyle)
			self.linewidth_txtbx_vis.setValue(linewidth)
			self.markerstyle_menu_vis.setCurrentText(Line2D.markers[markerstyle])
			self.markersize_txtbx_vis.setValue(int(markersize))
		except KeyError:
			pass

	def linelbl_action_vis(self):
		try:
			old_label = self.lineselector_menu_vis.currentText()
			new_label = self.linelbl_txtbx_vis.text()
			if old_label != new_label:
				data = self.line_dict_vis[old_label]
				ax = self.get_ax_vis()
				line = data.get_line()
				line.set_label(new_label)
				data.set_label(new_label)
				self.shwowleg_action_vis()
				self.figcanvas_vis.draw()
				self.line_dict_vis = {d.get_label():d for d in self.vishandler.get_plot_data()}
				self.lineselector_menu_vis.clear()
				for n in self.line_dict_vis.keys():
					self.lineselector_menu_vis.addItem(n)
				self.lineselector_menu_vis.setCurrentText(new_label)
		except KeyError:
			pass

	def linecolor_action_vis(self):
		try:
			label = self.lineselector_menu_vis.currentText()
			data = self.line_dict_vis[label]
			line = data.get_line()
			old_color = line.get_color()
			qd = QColorDialog()
			new_color = qd.getColor(initial=QColor(old_color)).name(QColor.HexRgb)
			line.set_color(new_color)
			self.shwowleg_action_vis()
			self.figcanvas_vis.draw()
		except KeyError:
			pass

	def linestyle_action_vis(self):
		try:
			label = self.lineselector_menu_vis.currentText()
			ls = self.linestyle_menu_vis.currentText()
			data = self.line_dict_vis[label]
			line = data.get_line()
			line.set_linestyle(ls)
			self.shwowleg_action_vis()
			self.figcanvas_vis.draw()
		except KeyError:
			pass

	def linewidth_action_vis(self):
		try:
			label = self.lineselector_menu_vis.currentText()
			lw = self.linewidth_txtbx_vis.value()
			data = self.line_dict_vis[label]
			line = data.get_line()
			line.set_linewidth(lw)
			self.shwowleg_action_vis()
			self.figcanvas_vis.draw()
		except KeyError:
			pass

	def markerstyle_action_vis(self):
		try:
			label = self.lineselector_menu_vis.currentText()
			m = self.markerstyle_menu_vis.currentText()
			data = self.line_dict_vis[label]
			line = data.get_line()
			line.set_marker(IfesUI.markerstyles_rev[m])
			self.shwowleg_action_vis()
			self.figcanvas_vis.draw()
		except KeyError:
			pass

	def markersize_action_vis(self):
		try:
			label = self.lineselector_menu_vis.currentText()
			ms = self.markersize_txtbx_vis.value()
			data = self.line_dict_vis[label]
			line = data.get_line()
			line.set_markersize(int(ms))
			self.shwowleg_action_vis()
			self.figcanvas_vis.draw()
		except KeyError:
			pass

	def choose_saveloc_vis(self):
		fd = QFileDialog()
		fd.setViewMode(QFileDialog.Detail)
		fd.setDefaultSuffix('png')
		filename, _ = fd.getSaveFileName(self, 'Save Location', self.default_saveloc_vis())
		if not filename:
			filename = self.default_saveloc_vis()
		self.saveloc_txtbx_vis.setText(filename)

	def save_action_vis(self):
		try:
			fig = self.figcanvas_vis.figure
			loc = self.saveloc_txtbx_vis.text()
			dpi = self.figres_txtbx_vis.text()
			if not dpi.isdigit():
				self.update_status('Figure resolution must be an integer')
				dpi = 300
			else:
				dpi = int(dpi)
			fig.savefig(loc, dpi=dpi)
			self.update_status('Image saved successfully')
		except Exception as e:
			self.update_status('ERROR: ' + str(e))

	def draw_plot_vis(self):
		fig = self.figcanvas_vis.figure
		fig.clf()
		ax = fig.subplots()
		self.vishandler.draw_plot(ax)
		self.xlabel_txtbx_vis.setText(ax.get_xlabel())
		self.ylabel_txtbx_vis.setText(ax.get_ylabel())
		# self.xmin_txtbx_vis.setText(f'{ax.get_xlim()[0]:.2f}')
		# self.xmax_txtbx_vis.setText(f'{ax.get_xlim()[1]:.2f}')
		# self.ymin_txtbx_vis.setText(f'{ax.get_ylim()[0]:.2f}')
		# self.ymax_txtbx_vis.setText(f'{ax.get_ylim()[1]:.2f}')
		self.line_dict_vis = {d.get_label():d for d in self.vishandler.get_plot_data()}
		self.lineselector_menu_vis.clear()
		for n in self.line_dict_vis.keys():
			self.lineselector_menu_vis.addItem(n)
		self.shwowleg_action_vis()
		ax.tick_params(axis='both', direction='in')
		self.figcanvas_vis.draw()

	def get_ax_vis(self):
		fig = self.figcanvas_vis.figure
		ax = fig.get_axes()
		return ax[0]

	def default_saveloc_vis(self):
		dataloc = self.folder_txtbx_data.text()
		saveloc = os.path.join(dataloc, 'figures')
		if not os.path.exists(saveloc):
			os.mkdir(saveloc)
		return saveloc

	##################
	# Tafel Analysis #
	##################
	### tafel layout ###
	# def tafel_layout(self):
	# 	# data selection header
	# 	self.header_tafel = QLabel('Tafel Analysis')
	# 	self.header_tafel.setFont(IfesUI.headerfont)
	# 	# use existing widgets
	# 	self.useexisting_chkbx_tafel = QCheckBox('Use previously loaded data')
	# 	self.useexisting_chkbx_tafel.setCheckState(Qt.Unchecked)
	# 	self.useexisting_chkbx_tafel.setLayoutDirection(Qt.RightToLeft)
	# 	# folder selection widgets
	# 	self.folder_lbl_tafel = QLabel('Data folder')
	# 	self.folder_txtbx_tafel = QLineEdit(IfesUI.homedir)
	# 	self.folder_btn_tafel = QPushButton('Choose folder...')
	# 	#file selection widgets
	# 	self.file_lbl_tafel = QLabel('Data files')
	# 	self.file_txtbx_tafel = QLineEdit()
	# 	self.file_btn_tafel = QPushButton('Choose files...')
	# 	# load data button
	# 	self.loaddata_btn_tafel = QPushButton('Load data')
	# 	#figure layout
	# 	self.figlayout_tafel = self.figure_layout_tafel()
	# 	# save plot header
	# 	self.header_saveplot_tafel = QLabel('Save Plot')
	# 	self.header_saveplot_tafel.setFont(IfesUI.headerfont)
	# 	# save plot widgets
	# 	self.saveloc_lbl_tafel = QLabel('Save location')
	# 	self.saveloc_txtbx_tafel = QLineEdit()
	# 	self.saveloc_btn_tafel = QPushButton('Choose location...')
	# 	self.save_btn_tafel = QPushButton('Save Current Figure')
	# 	# connect widgets
	# 	self.useexisting_chkbx_tafel.stateChanged.connect(self.useexisting_action_tafel)
	# 	self.folder_txtbx_tafel.textChanged.connect(self.folder_action_tafel)
	# 	self.folder_btn_tafel.clicked.connect(self.choose_folder_tafel)
	# 	self.file_txtbx_tafel.textChanged.connect(self.file_action_tafel)
	# 	self.file_btn_tafel.clicked.connect(self.choose_files_tafel)
	# 	self.loaddata_btn_tafel.clicked.connect(self.loaddata_action_tafel)
	# 	self.saveloc_btn_tafel.clicked.connect(self.choose_saveloc_tafel)
	# 	self.save_btn_tafel.clicked.connect(self.save_action_tafel)
	# 	# build layout
	# 	layout = QGridLayout()
	# 	row = 0
	# 	layout.addWidget(self.header_tafel, row, 0, 1, -1, Qt.AlignHCenter)
	# 	row += 1
	# 	layout.addWidget(self.useexisting_chkbx_tafel, row, 0, 1, -1, Qt.AlignRight)
	# 	row += 1
	# 	layout.addWidget(self.folder_lbl_tafel, row, 0)
	# 	layout.addWidget(self.folder_txtbx_tafel, row, 1)
	# 	layout.addWidget(self.folder_btn_tafel, row, 2)
	# 	row += 1
	# 	layout.addWidget(self.file_lbl_tafel, row, 0)
	# 	layout.addWidget(self.file_txtbx_tafel, row, 1)
	# 	layout.addWidget(self.file_btn_tafel, row, 2)
	# 	row += 1
	# 	layout.addWidget(self.loaddata_btn_tafel, row, 0, 1, -1, Qt.AlignHCenter)
	# 	row += 1
	# 	layout.addLayout(self.figlayout_tafel, row, 0, 1, -1, Qt.AlignLeft)
	# 	row += 1
	# 	layout.addWidget(self.header_saveplot_tafel, row, 0, 1, -1, Qt.AlignHCenter)
	# 	row += 1
	# 	layout.addWidget(self.saveloc_lbl_tafel, row, 0)
	# 	layout.addWidget(self.saveloc_txtbx_tafel, row, 1)
	# 	layout.addWidget(self.saveloc_btn_tafel, row, 2)
	# 	row += 1
	# 	layout.addWidget(self.save_btn_tafel, row, 0, 1, -1, Qt.AlignHCenter)

	# 	return layout

	# def figure_layout_tafel(self):
	# 	# plot features header
	# 	self.header_plotparams_tafel = QLabel('Plot Options')
	# 	self.header_plotparams_tafel.setFont(IfesUI.headerfont)
	# 	# # visualization selection widgets
	# 	# self.vistype_lbl = QLabel('Visualization type')
	# 	# self.vistype_menu = QComboBox()
	# 	# for name in IfesUI.vis_types:
	# 	# 	self.vistype_menu.addItem(name)
	# 	# column selection layout
	# 	self.colslayout_tafel = self.colselection_layout_tafel()
	# 	# plot features
	# 	self.plotfeatures_tafel = self.plotfeatures_layout_tafel()
	# 	# actual figure
	# 	self.figcanvas_tafel  = FigureCanvas(Figure(figsize=IfesUI.default_figsize))
	# 	self.figcanvas_tafel.figure.subplots()
	# 	# line properties header
	# 	self.header_lineprops_tafel = QLabel('Line Options')
	# 	self.header_lineprops_tafel.setFont(IfesUI.headerfont)
	# 	# line selector menu
	# 	self.lineselector_lbl_tafel = QLabel('line')
	# 	self.lineselector_menu_tafel = QComboBox()
	# 	# for n in IfesUI.tintin:
	# 	# 	self.lineselector_menu_tafel.addItem(n)
	# 	# line properties layout
	# 	# figure properties
	# 	self.figprops_tafel = self.figprops_layout_tafel()
	# 	self.lineselector_menu_tafel.currentTextChanged.connect(self.lineselector_action_tafel)
	# 	# build layout
	# 	layout = QGridLayout()
	# 	layout.addWidget(self.header_plotparams_tafel, 0, 0, 1, 2, Qt.AlignHCenter)
	# 	# layout.addWidget(self.vistype_lbl, 1, 0, Qt.AlignLeft)
	# 	# layout.addWidget(self.vistype_menu, 1, 1, Qt.AlignLeft)
	# 	layout.addLayout(self.colslayout_tafel, 1, 0, 1, 2, Qt.AlignLeft)
	# 	layout.addLayout(self.plotfeatures_tafel, 2, 0, 1, 2, Qt.AlignLeft)
	# 	layout.addWidget(self.figcanvas_tafel, 0, 2, 3, 1, Qt.AlignHCenter)
	# 	layout.addLayout(self.figprops_tafel, 3, 2, 1, 1, Qt.AlignHCenter)
	# 	layout.addWidget(self.header_lineprops_tafel, 0, 3, 1, 2, Qt.AlignHCenter)
	# 	layout.addWidget(self.lineselector_lbl_tafel, 1, 3, Qt.AlignLeft)
	# 	layout.addWidget(self.lineselector_menu_tafel, 1, 4, Qt.AlignLeft)
	# 	return layout

	# def colselection_layout_tafel(self):

	# 	# x column
	# 	self.xcol_lbl_tafel = QLabel('log(current) column')
	# 	self.xcol_txtbx_tafel = QLineEdit('0')
	# 	# y column
	# 	self.ycol_lbl_tafel = QLabel('Overpotential column')
	# 	self.ycol_txtbx_tafel = QLineEdit('1')
	# 	self.xcol_txtbx_tafel.textChanged.connect(self.xcol_action_tafel)
	# 	self.ycol_txtbx_tafel.textChanged.connect(self.ycol_action_tafel)
	# 	# build layout
	# 	layout = QGridLayout()
	# 	row = 0
	# 	layout.addWidget(self.xcol_lbl_tafel, row, 0, Qt.AlignLeft)
	# 	layout.addWidget(self.xcol_txtbx_tafel, row, 1, Qt.AlignLeft)
	# 	row += 1
	# 	layout.addWidget(self.ycol_lbl_tafel, row, 0, Qt.AlignLeft)
	# 	layout.addWidget(self.ycol_txtbx_tafel, row, 1, Qt.AlignLeft)
	# 	# resize widgets
	# 	for i in range(layout.count()):
	# 		w = layout.itemAt(i).widget()
	# 		if isinstance(w, QLineEdit):
	# 			self.set_max_width(w, 1.5)
	# 	return layout

	# def plotfeatures_layout_tafel(self):
	# 	# Tafel Values
	# 	self.tafel_slope_lbl = QLabel('Tafel slope: ')
	# 	self.tafel_slope_val = QLabel('')
	# 	self.tafel_exchg_lbl = QLabel('Exchange current density: ')
	# 	self.tafel_exchg_val = QLabel('')
	# 	self.tafel_rsq_lbl = QLabel('Linearity (R-squared):')
	# 	self.tafel_rsq_val = QLabel('')
	# 	self.tafel_slope_val.setFont(IfesUI.valuefont)
	# 	self.tafel_exchg_val.setFont(IfesUI.valuefont)
	# 	self.tafel_rsq_val.setFont(IfesUI.valuefont)
	# 	# x-axis label
	# 	self.xlabel_lbl_tafel = QLabel('x-axis label')
	# 	self.xlabel_txtbx_tafel = QLineEdit('log(current)')
	# 	# y-axis label
	# 	self.ylabel_lbl_tafel = QLabel('y-axis label')
	# 	self.ylabel_txtbx_tafel = QLineEdit('Overpotential [V]')
	# 	# current limits
	# 	self.mincurr_lbl_tafel = QLabel('Lower bound')
	# 	self.mincurr_txtbx_tafel = QLineEdit()
	# 	self.maxcurr_lbl_tafel = QLabel('Upper bound')
	# 	self.maxcurr_txtbx_tafel = QLineEdit()
	# 	# x-axis limits
	# 	self.xmin_lbl_tafel = QLabel('x min')
	# 	self.xmin_txtbx_tafel = QLineEdit()
	# 	self.xmax_lbl_tafel = QLabel('x max')
	# 	self.xmax_txtbx_tafel = QLineEdit()
	# 	# y-axis limits
	# 	self.ymin_lbl_tafel = QLabel('y min')
	# 	self.ymin_txtbx_tafel = QLineEdit()
	# 	self.ymax_lbl_tafel = QLabel('y max')
	# 	self.ymax_txtbx_tafel = QLineEdit()
	# 	# connect widgets
	# 	self.xlabel_txtbx_tafel.textChanged.connect(self.xlabel_action_tafel)
	# 	self.ylabel_txtbx_tafel.textChanged.connect(self.ylabel_action_tafel)
	# 	self.xmin_txtbx_tafel.textChanged.connect(self.xlim_action_tafel)
	# 	self.xmax_txtbx_tafel.textChanged.connect(self.xlim_action_tafel)
	# 	self.ymin_txtbx_tafel.textChanged.connect(self.ylim_action_tafel)
	# 	self.ymax_txtbx_tafel.textChanged.connect(self.ylim_action_tafel)
	# 	self.mincurr_txtbx_tafel.textChanged.connect(self.mincurr_action_tafel)
	# 	self.maxcurr_txtbx_tafel.textChanged.connect(self.maxcurr_action_tafel)
	# 	# build layout
	# 	layout = QGridLayout()
	# 	row = 0
	# 	layout.addWidget(self.mincurr_lbl_tafel, row, 0, 1, 2, Qt.AlignLeft)
	# 	layout.addWidget(self.mincurr_txtbx_tafel, row, 2, 1, 2, Qt.AlignLeft)
	# 	row += 1
	# 	layout.addWidget(self.maxcurr_lbl_tafel, row, 0, 1, 2, Qt.AlignLeft)
	# 	layout.addWidget(self.maxcurr_txtbx_tafel, row, 2, 1, 2, Qt.AlignLeft)
	# 	row += 1
	# 	layout.addWidget(self.tafel_slope_lbl, row, 0, 1, 2, Qt.AlignLeft)
	# 	layout.addWidget(self.tafel_slope_val, row, 2, 1, 2, Qt.AlignLeft)
	# 	row += 1
	# 	layout.addWidget(self.tafel_exchg_lbl, row, 0, 1, 2, Qt.AlignLeft)
	# 	layout.addWidget(self.tafel_exchg_val, row, 2, 1, 2, Qt.AlignLeft)
	# 	row += 1
	# 	layout.addWidget(self.tafel_rsq_lbl, row, 0, 1, 2, Qt.AlignLeft)
	# 	layout.addWidget(self.tafel_rsq_val, row, 2, 1, 2, Qt.AlignLeft)
	# 	row += 1
	# 	layout.addWidget(self.xlabel_lbl_tafel, row, 0, 1, 2, Qt.AlignLeft)
	# 	layout.addWidget(self.xlabel_txtbx_tafel, row, 2, 1, 2, Qt.AlignLeft)
	# 	row += 1
	# 	layout.addWidget(self.ylabel_lbl_tafel, row, 0, 1, 2, Qt.AlignLeft)
	# 	layout.addWidget(self.ylabel_txtbx_tafel, row, 2, 1, 2, Qt.AlignLeft)
	# 	# row += 1
	# 	# layout.addWidget(self.mincurr_lbl_tafel, row, 0, 1, 2, Qt.AlignLeft)
	# 	# layout.addWidget(self.mincurr_txtbx_tafel, row, 2, 1, 2, Qt.AlignLeft)
	# 	# row += 1
	# 	# layout.addWidget(self.maxcurr_lbl_tafel, row, 0, 1, 2, Qt.AlignLeft)
	# 	# layout.addWidget(self.maxcurr_txtbx_tafel, row, 2, 1, 2, Qt.AlignLeft)
	# 	row += 1
	# 	layout.addWidget(self.xmin_lbl_tafel, row, 0, Qt.AlignLeft)
	# 	layout.addWidget(self.xmin_txtbx_tafel, row, 1, Qt.AlignLeft)
	# 	layout.addWidget(self.xmax_lbl_tafel, row, 2, Qt.AlignLeft)
	# 	layout.addWidget(self.xmax_txtbx_tafel, row, 3, Qt.AlignLeft)
	# 	row += 1
	# 	layout.addWidget(self.ymin_lbl_tafel, row, 0, Qt.AlignLeft)
	# 	layout.addWidget(self.ymin_txtbx_tafel, row, 1, Qt.AlignLeft)
	# 	layout.addWidget(self.ymax_lbl_tafel, row, 2, Qt.AlignLeft)
	# 	layout.addWidget(self.ymax_txtbx_tafel, row, 3, Qt.AlignLeft)
	# 	# resize widgets
	# 	for i in range(layout.count()):
	# 		w = layout.itemAt(i).widget()
	# 		if isinstance(w, QLineEdit):
	# 			self.set_min_height(w)
	# 			# self.set_min_width(w)
	# 		if isinstance(w, QLabel):
	# 			self.set_max_height(w, 1.5)
	# 	self.set_max_width(self.xmin_txtbx_tafel, 0.5)
	# 	self.set_max_width(self.xmax_txtbx_tafel, 0.5)
	# 	self.set_max_width(self.ymin_txtbx_tafel, 0.5)
	# 	self.set_max_width(self.ymax_txtbx_tafel, 0.5)
	# 	return layout

	# def figprops_layout_tafel(self):
	# 	# fig width
	# 	self.figw_lbl_tafel = QLabel('Figure width')
	# 	self.figw_txtbx_tafel = QLineEdit(str(IfesUI.default_figsize[0]))
	# 	# fig height
	# 	self.figh_lbl_tafel = QLabel('Figue height')
	# 	self.figh_txtbx_tafel = QLineEdit(str(IfesUI.default_figsize[1]))
	# 	# fig resolution
	# 	self.figres_lbl_tafel = QLabel('Figure resolution (DPI)')
	# 	self.figres_txtbx_tafel = QLineEdit(str(IfesUI.default_figres))
	# 	self.figw_txtbx_tafel.textChanged.connect(self.figsize_action_tafel)
	# 	self.figh_txtbx_tafel.textChanged.connect(self.figsize_action_tafel)
	# 	# build layout
	# 	layout = QGridLayout()
	# 	row = 0
	# 	layout.addWidget(self.figw_lbl_tafel, row, 0, Qt.AlignHCenter)
	# 	layout.addWidget(self.figh_lbl_tafel, row, 1, Qt.AlignHCenter)
	# 	layout.addWidget(self.figres_lbl_tafel, row, 2, Qt.AlignHCenter)
	# 	row += 1
	# 	layout.addWidget(self.figw_txtbx_tafel, row, 0, Qt.AlignHCenter)
	# 	layout.addWidget(self.figh_txtbx_tafel, row, 1, Qt.AlignHCenter)
	# 	layout.addWidget(self.figres_txtbx_tafel, row, 2, Qt.AlignHCenter)
	# 	for i in range(layout.count()):
	# 		w = layout.itemAt(i).widget()
	# 		if isinstance(w, QLineEdit):
	# 			self.set_max_width(w, 0.75)
	# 	return layout

	# ### tafel actions ###
	# def useexisting_action_tafel(self):
	# 	state = self.useexisting_chkbx_tafel.isChecked()
	# 	if state:
	# 		if not self.datahandler.get_data():
	# 			self.update_status('No data to visualize')
	# 			self.useexisting_chkbx_tafel.setCheckState(Qt.Unchecked)
	# 			state = False
	# 		else:
	# 			self.vishandler.set_data(self.datahandler.get_data())
	# 	self.folder_lbl_tafel.setEnabled(not state)
	# 	self.folder_txtbx_tafel.setEnabled(not state)
	# 	self.folder_btn_tafel.setEnabled(not state)
	# 	self.file_lbl_tafel.setEnabled(not state)
	# 	self.file_txtbx_tafel.setEnabled(not state)
	# 	self.file_btn_tafel.setEnabled(not state)
	# 	self.loaddata_btn_tafel.setEnabled(not state)
	# 	if state:
	# 		self.draw_plot_tafel()

	# def choose_folder_tafel(self):
	# 	fd = QFileDialog()
	# 	filepath = fd.getExistingDirectory(self, 'Data Folder', IfesUI.homedir)
	# 	if filepath:
	# 		self.folder_txtbx_tafel.setText(filepath)
	# 		self.file_txtbx_tafel.setText('')

	# def choose_files_tafel(self):
	# 	fd = QFileDialog()
	# 	files, _ = fd.getOpenFileNames(self, 'Data Files', IfesUI.homedir)
	# 	if files:
	# 		names = [os.path.basename(f) for f in files]
	# 		folder = os.path.dirname(files[0])
	# 		self.file_txtbx_tafel.setText('; '.join(names))
	# 		self.folder_txtbx_tafel.setText(folder)

	# def folder_action_tafel(self):
	# 	try:
	# 		folder = self.folder_txtbx_tafel.text()
	# 		self.vishandler.set_datafolder(folder)
	# 		self.file_action_tafel()
	# 	except Exception as e:
	# 		self.update_status('ERROR: ' + str(e))

	# def file_action_tafel(self):
	# 	file_str = self.file_txtbx_tafel.text()
	# 	folder = self.folder_txtbx_tafel.text()
	# 	try:
	# 		if not file_str:
	# 			files = self.get_all_files(folder, valid=utils.valid_types)
	# 			self.file_txtbx_tafel.setText('; '.join(files))
	# 		else:
	# 			files = file_str.split('; ')
	# 		files = [os.path.join(folder, f) for f in files]
	# 		self.vishandler.set_datafiles(files)
	# 	except Exception as e:
	# 		self.update_status('ERROR: ' + str(e))

	# def loaddata_action_tafel(self):
	# 	try:
	# 		self.vishandler.load_tafel()
	# 		self.draw_plot_tafel()
	# 	except Exception as e:
	# 		self.update_status('ERROR: ' + str(e))

	# def xcol_action_tafel(self):
	# 	col = self.xcol_txtbx_tafel.text()
	# 	if col.isdigit():
	# 		col = int(col)
	# 	self.vishandler.set_xcol(col)
	# 	self.draw_plot_tafel()

	# def ycol_action_tafel(self):
	# 	col = self.ycol_txtbx_tafel.text()
	# 	if col.isdigit():
	# 		col = int(col)
	# 	self.vishandler.set_ycol(col)
	# 	self.draw_plot_tafel()

	# def mincurr_action_tafel(self):
	# 	new_min = self.mincurr_txtbx_tafel.text()
	# 	new_max = self.maxcurr_txtbx_tafel.text()
	# 	try:
	# 		new_min = float(new_min)
	# 	except ValueError:
	# 		new_min = None
	# 		self.update_status('bounds must be numbers')
	# 	try:
	# 		new_max = float(new_max)
	# 	except ValueError:
	# 		new_max = None
	# 		self.update_status('bounds must be numbers')
	# 	try:
	# 		fig = self.figcanvas_tafel.figure
	# 		fig.clf()
	# 		ax = self.figcanvas_tafel.figure.subplots()
	# 		this_data = self.tafel_dict[self.lineselector_menu_tafel.currentText()]
	# 		visuals.plot_tafel(data=[this_data], ax=ax, imin=new_min, imax=new_max)
	# 		self.tafel_slope_val.setText(str(this_data.get_tafel_slope()))
	# 		self.tafel_exchg_val.setText(str(this_data.get_exchg_curr()))
	# 		self.tafel_rsq_val.setText(str(this_data.get_tafel_rsq()))
	# 		self.figcanvas_tafel.draw()
	# 	except Exception as e:
	# 		self.update_status('ERROR: ' + str(e))

	# def maxcurr_action_tafel(self):
	# 	new_max = self.maxcurr_txtbx_tafel.text()
	# 	new_min = self.mincurr_txtbx_tafel.text()
	# 	try:
	# 		new_min = float(new_min)
	# 	except ValueError:
	# 		new_min = None
	# 		self.update_status('bounds must be numbers')
	# 	try:
	# 		new_max = float(new_max)
	# 	except ValueError:
	# 		new_max = None
	# 		self.update_status('bounds must be numbers')
	# 	try:
	# 		fig = self.figcanvas_tafel.figure
	# 		fig.clf()
	# 		ax = self.figcanvas_tafel.figure.subplots()
	# 		this_data = self.tafel_dict[self.lineselector_menu_tafel.currentText()]
	# 		visuals.plot_tafel(data=[this_data], ax=ax, imax=new_max, imin=new_min)
	# 		self.tafel_slope_val.setText(str(this_data.get_tafel_slope()))
	# 		self.tafel_exchg_val.setText(str(this_data.get_exchg_curr()))
	# 		self.tafel_rsq_val.setText(str(this_data.get_tafel_rsq()))
	# 		self.figcanvas_tafel.draw()
	# 	except Exception as e:
	# 		self.update_status('ERROR: ' + str(e))

	# def xlabel_action_tafel(self):
	# 	new_label = self.xlabel_txtbx_tafel.text()
	# 	ax = self.get_ax_tafel()
	# 	ax.set_xlabel(new_label)
	# 	self.figcanvas_tafel.draw()

	# def ylabel_action_tafel(self):
	# 	new_label = self.ylabel_txtbx_tafel.text()
	# 	ax = self.get_ax_tafel()
	# 	ax.set_ylabel(new_label)
	# 	self.figcanvas_tafel.draw()

	# def xlim_action_tafel(self):
	# 	xmin_text = self.xmin_txtbx_tafel.text()
	# 	xmax_text = self.xmax_txtbx_tafel.text()
	# 	ax = self.get_ax_tafel()
	# 	try:
	# 		xmin = float(xmin_text)
	# 		ax.set_xbound(lower=xmin)
	# 	except ValueError:
	# 		self.update_status('xmin must be a number')
	# 	try:
	# 		xmax = float(xmax_text)
	# 		ax.set_xbound(upper=xmax)
	# 	except ValueError:
	# 		self.update_status('xmax must be a number')
	# 	self.figcanvas_tafel.draw()

	# def ylim_action_tafel(self):
	# 	ymin_text = self.ymin_txtbx_tafel.text()
	# 	ymax_text = self.ymax_txtbx_tafel.text()
	# 	ax = self.get_ax_tafel()
	# 	try:
	# 		ymin = float(ymin_text)
	# 		ax.set_ybound(lower=ymin)
	# 	except ValueError:
	# 		self.update_status('ymin must be a number')
	# 	try:
	# 		ymax = float(ymax_text)
	# 		ax.set_ybound(upper=ymax)
	# 	except ValueError:
	# 		self.update_status('ymax must be a number')
	# 	self.figcanvas_tafel.draw()

	# def figsize_action_tafel(self):
	# 	fig = self.figcanvas_tafel.figure
	# 	width = self.figw_txtbx_tafel.text()
	# 	height = self.figh_txtbx_tafel.text()
	# 	try:
	# 		width = float(width)
	# 		height = float(height)
	# 		fig.set_figwidth(width)
	# 		fig.set_figheight(height)
	# 		self.figcanvas_tafel.draw()
	# 	except ValueError:
	# 		self.update_status('Figure width and height must be numbers')

	# def lineselector_action_tafel(self):
	# 	try:
	# 		new_label = self.lineselector_menu_tafel.currentText()
	# 		new_data = self.tafel_dict[new_label]
	# 		fig = self.figcanvas_tafel.figure
	# 		fig.clf()
	# 		ax = self.figcanvas_tafel.figure.subplots()
	# 		visuals.plot_tafel(data=[new_data], ax=ax)
	# 		self.figcanvas_tafel.draw()
	# 		self.tafel_slope_val.setText(str(new_data.get_tafel_slope()))
	# 		self.tafel_exchg_val.setText(str(new_data.get_exchg_curr()))
	# 		self.tafel_rsq_val.setText(str(new_data.get_tafel_rsq()))
	# 	except TypeError:
	# 		self.update_status('Invalid fit parameters')

	# def choose_saveloc_tafel(self):
	# 	fd = QFileDialog()
	# 	fd.setViewMode(QFileDialog.Detail)
	# 	fd.setDefaultSuffix('png')
	# 	filename, _ = fd.getSaveFileName(self, 'Save Location', self.default_saveloc_vis())
	# 	if not filename:
	# 		filename = self.default_saveloc_vis()
	# 	self.saveloc_txtbx_tafel.setText(filename)

	# def save_action_tafel(self):
	# 	try:
	# 		fig = self.figcanvas_tafel.figure
	# 		loc = self.saveloc_txtbx_tafel.text()
	# 		dpi = self.figres_txtbx_tafel.text()
	# 		if not dpi.isdigit():
	# 			self.update_status('Figure resolution must be an integer')
	# 			dpi = 300
	# 		else:
	# 			dpi = int(dpi)
	# 		fig.savefig(loc, dpi=dpi)
	# 		self.update_status('Image saved successfully')
	# 	except Exception as e:
	# 		self.update_status('ERROR: ' + str(e))

	# def draw_plot_tafel(self):
	# 	try:
	# 		fig = self.figcanvas_tafel.figure
	# 		fig.clf()
	# 		ax = self.figcanvas_tafel.figure.subplots()
	# 		tafel_data = self.vishandler.get_tafel_data()
	# 		self.tafel_dict = {d.get_label():d for d in tafel_data}
	# 		for n in self.tafel_dict.keys():
	# 			self.lineselector_menu_tafel.addItem(n)
	# 		this_data = tafel_data[0]
	# 		# name = self.lineselector_menu_tafel.currentText()
	# 		# data =  self.tafel_dict[name]
	# 		# self.hfrsemi_val.setText(str(data.get_hfr()))
	# 		# self.hfrlin_val.setText(str(data.get_hfr_linear()))
	# 		visuals.plot_tafel(data=[this_data], ax=ax)
	# 		self.tafel_slope_val.setText(str(this_data.get_tafel_slope()))
	# 		self.tafel_exchg_val.setText(str(this_data.get_exchg_curr()))
	# 		self.tafel_rsq_val.setText(str(this_data.get_tafel_rsq()))
	# 		self.figcanvas_tafel.draw()
	# 	except Exception as e:
	# 		self.update_status('ERROR: ' + str(e))

	# def get_ax_tafel(self):
	# 	fig = self.figcanvas_tafel.figure
	# 	ax = fig.get_axes()
	# 	return ax[0]

	###########################
	# Bayesian Tafel Analysis #
	###########################
	### bayes layout ###
	# def bayes_layout(self):
	# 	# data selection header
	# 	self.header_bayes = QLabel('Bayesian Tafel Analysis')
	# 	self.header_bayes.setFont(IfesUI.headerfont)
	# 	# use existing widgets
	# 	self.useexisting_chkbx_bayes = QCheckBox('Use previously loaded data')
	# 	self.useexisting_chkbx_bayes.setCheckState(Qt.Unchecked)
	# 	self.useexisting_chkbx_bayes.setLayoutDirection(Qt.RightToLeft)
	# 	# folder selection widgets
	# 	self.folder_lbl_bayes = QLabel('Data folder')
	# 	self.folder_txtbx_bayes = QLineEdit(IfesUI.homedir)
	# 	self.folder_btn_bayes = QPushButton('Choose folder...')
	# 	#file selection widgets
	# 	self.file_lbl_bayes = QLabel('Data files')
	# 	self.file_txtbx_bayes = QLineEdit()
	# 	self.file_btn_bayes = QPushButton('Choose files...')
	# 	# load data button
	# 	self.loaddata_btn_bayes = QPushButton('Load data')
	# 	# figure layout
	# 	self.figlayout_bayes = self.figure_layout_bayes()
	# 	# save plot header
	# 	self.header_saveplot_bayes = QLabel('Save Plot')
	# 	self.header_saveplot_bayes.setFont(IfesUI.headerfont)
	# 	# save plot widgets
	# 	self.saveloc_lbl_bayes = QLabel('Save location')
	# 	self.saveloc_txtbx_bayes = QLineEdit()
	# 	self.saveloc_btn_bayes = QPushButton('Choose location...')
	# 	self.save_btn_bayes = QPushButton('Save Current Figure')
	# 	# connect widgets
	# 	self.useexisting_chkbx_bayes.stateChanged.connect(self.useexisting_action_bayes)
	# 	self.folder_txtbx_bayes.textChanged.connect(self.folder_action_bayes)
	# 	self.folder_btn_bayes.clicked.connect(self.choose_folder_bayes)
	# 	self.file_txtbx_bayes.textChanged.connect(self.file_action_bayes)
	# 	self.file_btn_bayes.clicked.connect(self.choose_files_bayes)
	# 	self.loaddata_btn_bayes.clicked.connect(self.loaddata_action_bayes)
	# 	self.saveloc_btn_bayes.clicked.connect(self.choose_saveloc_bayes)
	# 	self.save_btn_bayes.clicked.connect(self.save_action_bayes)
	# 	# build layout
	# 	layout = QGridLayout()
	# 	row = 0
	# 	layout.addWidget(self.header_bayes, row, 0, 1, -1, Qt.AlignHCenter)
	# 	row += 1
	# 	layout.addWidget(self.useexisting_chkbx_bayes, row, 0, 1, -1, Qt.AlignRight)
	# 	row += 1
	# 	layout.addWidget(self.folder_lbl_bayes, row, 0)
	# 	layout.addWidget(self.folder_txtbx_bayes, row, 1)
	# 	layout.addWidget(self.folder_btn_bayes, row, 2)
	# 	row += 1
	# 	layout.addWidget(self.file_lbl_bayes, row, 0)
	# 	layout.addWidget(self.file_txtbx_bayes, row, 1)
	# 	layout.addWidget(self.file_btn_bayes, row, 2)
	# 	row += 1
	# 	layout.addWidget(self.loaddata_btn_bayes, row, 0, 1, -1, Qt.AlignHCenter)
	# 	row += 1
	# 	layout.addLayout(self.figlayout_bayes, row, 0, 1, -1, Qt.AlignLeft)
	# 	row += 1
	# 	layout.addWidget(self.header_saveplot_bayes, row, 0, 1, -1, Qt.AlignHCenter)
	# 	row += 1
	# 	layout.addWidget(self.saveloc_lbl_bayes, row, 0)
	# 	layout.addWidget(self.saveloc_txtbx_bayes, row, 1)
	# 	layout.addWidget(self.saveloc_btn_bayes, row, 2)
	# 	row += 1
	# 	layout.addWidget(self.save_btn_bayes, row, 0, 1, -1, Qt.AlignHCenter)
	# 	return layout

	# def figure_layout_bayes(self):
	# 	# plot features header
	# 	self.header_plotparams_bayes = QLabel('Plot Options')
	# 	self.header_plotparams_bayes.setFont(IfesUI.headerfont)
	# 	# # visualization selection widgets
	# 	# self.vistype_lbl = QLabel('Visualization type')
	# 	# self.vistype_menu = QComboBox()
	# 	# for name in IfesUI.vis_types:
	# 	# 	self.vistype_menu.addItem(name)
	# 	# column selection layout
	# 	self.colslayout_bayes = self.colselection_layout_bayes()
	# 	# plot features
	# 	self.plotfeatures_bayes = self.plotfeatures_layout_bayes()
	# 	# actual figure
	# 	self.figcanvas_bayes_cdf  = FigureCanvas(Figure(figsize=(5,5)))
	# 	self.figcanvas_bayes_cdf.figure.subplots()
	# 	self.figcanvas_bayes_kde  = FigureCanvas(Figure(figsize=(5,5)))
	# 	self.figcanvas_bayes_kde.figure.subplots()
	# 	# line properties header
	# 	self.header_lineprops_bayes = QLabel('Data Selector')
	# 	self.header_lineprops_bayes.setFont(IfesUI.headerfont)
	# 	# line selector menu
	# 	self.lineselector_lbl_bayes = QLabel('Dataset')
	# 	self.lineselector_menu_bayes = QComboBox()
	# 	# for n in IfesUI.tintin:
	# 	# 	self.lineselector_menu_bayes.addItem(n)
	# 	# line properties layout
	# 	# figure properties
	# 	self.figprops_bayes = self.figprops_layout_bayes()
	# 	self.lineselector_menu_bayes.currentTextChanged.connect(self.lineselector_action_bayes)
	# 	# build layout
	# 	layout = QGridLayout()
	# 	layout.addWidget(self.header_plotparams_bayes, 0, 0, 1, 2, Qt.AlignHCenter)
	# 	layout.addLayout(self.colslayout_bayes, 1, 0, 1, 2, Qt.AlignLeft)
	# 	layout.addLayout(self.plotfeatures_bayes, 2, 0, 1, 2, Qt.AlignLeft)
	# 	layout.addWidget(self.figcanvas_bayes_cdf, 0, 2, 3, 1, Qt.AlignHCenter)
	# 	layout.addWidget(self.figcanvas_bayes_kde, 0, 3, 3, 1, Qt.AlignHCenter)
	# 	layout.addLayout(self.figprops_bayes, 3, 2, 1, 1, Qt.AlignHCenter)
	# 	layout.addWidget(self.header_lineprops_bayes, 0, 4, 1, 2, Qt.AlignHCenter)
	# 	layout.addWidget(self.lineselector_lbl_bayes, 1, 4, Qt.AlignLeft)
	# 	layout.addWidget(self.lineselector_menu_bayes, 1, 5, Qt.AlignLeft)
	# 	return layout

	# def colselection_layout_bayes(self):

	# 	# x column
	# 	self.xcol_lbl_bayes = QLabel('log(current) column')
	# 	self.xcol_txtbx_bayes = QLineEdit('0')
	# 	# y column
	# 	self.ycol_lbl_bayes = QLabel('Overpotential column')
	# 	self.ycol_txtbx_bayes = QLineEdit('1')
	# 	self.xcol_txtbx_bayes.textChanged.connect(self.xcol_action_bayes)
	# 	self.ycol_txtbx_bayes.textChanged.connect(self.ycol_action_bayes)
	# 	# build layout
	# 	layout = QGridLayout()
	# 	row = 0
	# 	layout.addWidget(self.xcol_lbl_bayes, row, 0, Qt.AlignLeft)
	# 	layout.addWidget(self.xcol_txtbx_bayes, row, 1, Qt.AlignLeft)
	# 	row += 1
	# 	layout.addWidget(self.ycol_lbl_bayes, row, 0, Qt.AlignLeft)
	# 	layout.addWidget(self.ycol_txtbx_bayes, row, 1, Qt.AlignLeft)
	# 	# resize widgets
	# 	for i in range(layout.count()):
	# 		w = layout.itemAt(i).widget()
	# 		if isinstance(w, QLineEdit):
	# 			self.set_max_width(w, 1.5)

	# 	for i in range(layout.count()):
	# 		w = layout.itemAt(i).widget()
	# 		w.setEnabled(False)
	# 	return layout

	# def plotfeatures_layout_bayes(self):
	# 	# bayes Values
	# 	self.bayes_slope_lbl = QLabel('Tafel slope')
	# 	self.bayes_slope_val = QLabel('')
	# 	self.bayes_exchg_lbl = QLabel('Exchange current density')
	# 	self.bayes_exchg_val = QLabel('')
	# 	self.bayes_rsq_lbl = QLabel('Linearity (R-squared):')
	# 	self.bayes_rsq_val = QLabel('')
	# 	self.bayes_slope_val.setFont(IfesUI.valuefont)
	# 	self.bayes_exchg_val.setFont(IfesUI.valuefont)
	# 	self.bayes_rsq_val.setFont(IfesUI.valuefont)
	# 	# x-axis label
	# 	self.xlabel_lbl_bayes = QLabel('x-axis label')
	# 	self.xlabel_txtbx_bayes = QLineEdit('log(current)')
	# 	# y-axis label
	# 	self.ylabel_lbl_bayes = QLabel('y-axis label')
	# 	self.ylabel_txtbx_bayes = QLineEdit('Overpotential [V]')
	# 	# x-axis limits
	# 	self.xmin_lbl_bayes = QLabel('x min')
	# 	self.xmin_txtbx_bayes = QLineEdit()
	# 	self.xmax_lbl_bayes = QLabel('x max')
	# 	self.xmax_txtbx_bayes = QLineEdit()
	# 	# y-axis limits
	# 	self.ymin_lbl_bayes = QLabel('y min')
	# 	self.ymin_txtbx_bayes = QLineEdit()
	# 	self.ymax_lbl_bayes = QLabel('y max')
	# 	self.ymax_txtbx_bayes = QLineEdit()
	# 	# connect widgets
	# 	self.xlabel_txtbx_bayes.textChanged.connect(self.xlabel_action_bayes)
	# 	self.ylabel_txtbx_bayes.textChanged.connect(self.ylabel_action_bayes)
	# 	self.xmin_txtbx_bayes.textChanged.connect(self.xlim_action_bayes)
	# 	self.xmax_txtbx_bayes.textChanged.connect(self.xlim_action_bayes)
	# 	self.ymin_txtbx_bayes.textChanged.connect(self.ylim_action_bayes)
	# 	self.ymax_txtbx_bayes.textChanged.connect(self.ylim_action_bayes)
	# 	# build layout
	# 	layout = QGridLayout()
	# 	row = 0
	# 	layout.addWidget(self.bayes_slope_lbl, row, 0, 1, 2, Qt.AlignLeft)
	# 	layout.addWidget(self.bayes_slope_val, row, 2, 1, 2, Qt.AlignLeft)
	# 	row += 1
	# 	layout.addWidget(self.bayes_exchg_lbl, row, 0, 1, 2, Qt.AlignLeft)
	# 	layout.addWidget(self.bayes_exchg_val, row, 2, 1, 2, Qt.AlignLeft)
	# 	row += 1
	# 	layout.addWidget(self.bayes_rsq_lbl, row, 0, 1, 2, Qt.AlignLeft)
	# 	layout.addWidget(self.bayes_rsq_val, row, 2, 1, 2, Qt.AlignLeft)
	# 	row += 1
	# 	layout.addWidget(self.xlabel_lbl_bayes, row, 0, 1, 2, Qt.AlignLeft)
	# 	layout.addWidget(self.xlabel_txtbx_bayes, row, 2, 1, 2, Qt.AlignLeft)
	# 	row += 1
	# 	layout.addWidget(self.ylabel_lbl_bayes, row, 0, 1, 2, Qt.AlignLeft)
	# 	layout.addWidget(self.ylabel_txtbx_bayes, row, 2, 1, 2, Qt.AlignLeft)
	# 	row += 1
	# 	layout.addWidget(self.xmin_lbl_bayes, row, 0, Qt.AlignLeft)
	# 	layout.addWidget(self.xmin_txtbx_bayes, row, 1, Qt.AlignLeft)
	# 	layout.addWidget(self.xmax_lbl_bayes, row, 2, Qt.AlignLeft)
	# 	layout.addWidget(self.xmax_txtbx_bayes, row, 3, Qt.AlignLeft)
	# 	row += 1
	# 	layout.addWidget(self.ymin_lbl_bayes, row, 0, Qt.AlignLeft)
	# 	layout.addWidget(self.ymin_txtbx_bayes, row, 1, Qt.AlignLeft)
	# 	layout.addWidget(self.ymax_lbl_bayes, row, 2, Qt.AlignLeft)
	# 	layout.addWidget(self.ymax_txtbx_bayes, row, 3, Qt.AlignLeft)
	# 	# resize widgets
	# 	for i in range(layout.count()):
	# 		w = layout.itemAt(i).widget()
	# 		if isinstance(w, QLineEdit):
	# 			self.set_min_height(w)
	# 			# self.set_min_width(w)
	# 		if isinstance(w, QLabel):
	# 			self.set_max_height(w, 1.5)

	# 	for i in range(layout.count()):
	# 		w = layout.itemAt(i).widget()
	# 		w.setEnabled(False)
	# 	self.set_max_width(self.xmin_txtbx_bayes, 0.5)
	# 	self.set_max_width(self.xmax_txtbx_bayes, 0.5)
	# 	self.set_max_width(self.ymin_txtbx_bayes, 0.5)
	# 	self.set_max_width(self.ymax_txtbx_bayes, 0.5)
	# 	return layout

	# def figprops_layout_bayes(self):
	# 	# fig width
	# 	self.figw_lbl_bayes = QLabel('Figure width')
	# 	self.figw_txtbx_bayes = QLineEdit(str(IfesUI.default_figsize[0]))
	# 	# fig height
	# 	self.figh_lbl_bayes = QLabel('Figue height')
	# 	self.figh_txtbx_bayes = QLineEdit(str(IfesUI.default_figsize[1]))
	# 	# fig resolution
	# 	self.figres_lbl_bayes = QLabel('Figure resolution (DPI)')
	# 	self.figres_txtbx_bayes = QLineEdit(str(IfesUI.default_figres))
	# 	self.figw_txtbx_bayes.textChanged.connect(self.figsize_action_bayes)
	# 	self.figh_txtbx_bayes.textChanged.connect(self.figsize_action_bayes)
	# 	# build layout
	# 	layout = QGridLayout()
	# 	row = 0
	# 	layout.addWidget(self.figw_lbl_bayes, row, 0, Qt.AlignHCenter)
	# 	layout.addWidget(self.figh_lbl_bayes, row, 1, Qt.AlignHCenter)
	# 	layout.addWidget(self.figres_lbl_bayes, row, 2, Qt.AlignHCenter)
	# 	row += 1
	# 	layout.addWidget(self.figw_txtbx_bayes, row, 0, Qt.AlignHCenter)
	# 	layout.addWidget(self.figh_txtbx_bayes, row, 1, Qt.AlignHCenter)
	# 	layout.addWidget(self.figres_txtbx_bayes, row, 2, Qt.AlignHCenter)
	# 	for i in range(layout.count()):
	# 		w = layout.itemAt(i).widget()
	# 		if isinstance(w, QLineEdit):
	# 			self.set_max_width(w, 0.75)
	# 	for i in range(layout.count()):
	# 		w = layout.itemAt(i).widget()
	# 		w.setEnabled(False)
	# 	return layout

	# ### bayes actions ###
	# def useexisting_action_bayes(self):
	# 	state = self.useexisting_chkbx_bayes.isChecked()
	# 	if state:
	# 		if not self.datahandler.get_data():
	# 			self.update_status('No data to visualize')
	# 			self.useexisting_chkbx_bayes.setCheckState(Qt.Unchecked)
	# 			state = False
	# 		else:
	# 			self.vishandler.set_data(self.datahandler.get_data())
	# 	self.folder_lbl_bayes.setEnabled(not state)
	# 	self.folder_txtbx_bayes.setEnabled(not state)
	# 	self.folder_btn_bayes.setEnabled(not state)
	# 	self.file_lbl_bayes.setEnabled(not state)
	# 	self.file_txtbx_bayes.setEnabled(not state)
	# 	self.file_btn_bayes.setEnabled(not state)
	# 	self.loaddata_btn_bayes.setEnabled(not state)
	# 	if state:
	# 		self.draw_plot_bayes()

	# def choose_folder_bayes(self):
	# 	fd = QFileDialog()
	# 	filepath = fd.getExistingDirectory(self, 'Data Folder', IfesUI.homedir)
	# 	if filepath:
	# 		self.folder_txtbx_bayes.setText(filepath)
	# 		self.file_txtbx_bayes.setText('')

	# def choose_files_bayes(self):
	# 	fd = QFileDialog()
	# 	files, _ = fd.getOpenFileNames(self, 'Data Files', IfesUI.homedir)
	# 	if files:
	# 		names = [os.path.basename(f) for f in files]
	# 		folder = os.path.dirname(files[0])
	# 		self.file_txtbx_bayes.setText('; '.join(names))
	# 		self.folder_txtbx_bayes.setText(folder)

	# def folder_action_bayes(self):
	# 	try:
	# 		folder = self.folder_txtbx_bayes.text()
	# 		self.vishandler.set_datafolder(folder)
	# 		self.file_action_bayes()
	# 	except Exception as e:
	# 		self.update_status('ERROR: ' + str(e))

	# def file_action_bayes(self):
	# 	file_str = self.file_txtbx_bayes.text()
	# 	folder = self.folder_txtbx_bayes.text()
	# 	try:
	# 		if not file_str:
	# 			files = self.get_all_files(folder, valid=utils.valid_types)
	# 			self.file_txtbx_bayes.setText('; '.join(files))
	# 		else:
	# 			files = file_str.split('; ')
	# 		files = [os.path.join(folder, f) for f in files]
	# 		self.vishandler.set_datafiles(files)
	# 	except Exception as e:
	# 		self.update_status('ERROR: ' + str(e))

	# def loaddata_action_bayes(self):
	# 	try:
	# 		self.vishandler.load_bayes()
	# 		self.draw_plot_bayes()
	# 	except Exception as e:
	# 		self.update_status('ERROR: ' + str(e))

	# def xcol_action_bayes(self):
	# 	col = self.xcol_txtbx_bayes.text()
	# 	if col.isdigit():
	# 		col = int(col)
	# 	self.vishandler.set_xcol(col)
	# 	self.draw_plot_bayes()

	# def ycol_action_bayes(self):
	# 	col = self.ycol_txtbx_bayes.text()
	# 	if col.isdigit():
	# 		col = int(col)
	# 	self.vishandler.set_ycol(col)
	# 	self.draw_plot_bayes()

	# def xlabel_action_bayes(self):
	# 	new_label = self.xlabel_txtbx_bayes.text()
	# 	ax = self.get_ax_bayes()
	# 	ax.set_xlabel(new_label)
	# 	self.figcanvas_bayes_cdf.draw()

	# def ylabel_action_bayes(self):
	# 	new_label = self.ylabel_txtbx_bayes.text()
	# 	ax = self.get_ax_bayes()
	# 	ax.set_ylabel(new_label)
	# 	self.figcanvas_bayes_cdf.draw()

	# def xlim_action_bayes(self):
	# 	xmin_text = self.xmin_txtbx_bayes.text()
	# 	xmax_text = self.xmax_txtbx_bayes.text()
	# 	ax = self.get_ax_bayes()
	# 	try:
	# 		xmin = float(xmin_text)
	# 		ax.set_xbound(lower=xmin)
	# 	except ValueError:
	# 		self.update_status('xmin must be a number')
	# 	try:
	# 		xmax = float(xmax_text)
	# 		ax.set_xbound(upper=xmax)
	# 	except ValueError:
	# 		self.update_status('xmax must be a number')
	# 	self.figcanvas_bayes_cdf.draw()

	# def ylim_action_bayes(self):
	# 	ymin_text = self.ymin_txtbx_bayes.text()
	# 	ymax_text = self.ymax_txtbx_bayes.text()
	# 	ax = self.get_ax_bayes()
	# 	try:
	# 		ymin = float(ymin_text)
	# 		ax.set_ybound(lower=ymin)
	# 	except ValueError:
	# 		self.update_status('ymin must be a number')
	# 	try:
	# 		ymax = float(ymax_text)
	# 		ax.set_ybound(upper=ymax)
	# 	except ValueError:
	# 		self.update_status('ymax must be a number')
	# 	self.figcanvas_bayes_cdf.draw()

	# def figsize_action_bayes(self):
	# 	fig = self.figcanvas_bayes_cdf.figure
	# 	width = self.figw_txtbx_bayes.text()
	# 	height = self.figh_txtbx_bayes.text()
	# 	try:
	# 		width = float(width)
	# 		height = float(height)
	# 		fig.set_figwidth(width)
	# 		fig.set_figheight(height)
	# 		self.figcanvas_bayes_cdf.draw()
	# 	except ValueError:
	# 		self.update_status('Figure width and height must be numbers')

	# def lineselector_action_bayes(self):
	# 	try:
	# 		new_label = self.lineselector_menu_bayes.currentText()
	# 		new_data = self.bayes_dict[new_label]
	# 		fig_cdf = self.figcanvas_bayes_cdf.figure
	# 		fig_kde = self.figcanvas_bayes_kde.figure
	# 		fig_cdf.clf()
	# 		fig_kde.clf()
	# 		ax_cdf = self.figcanvas_bayes_cdf.figure.subplots()
	# 		ax_kde = self.figcanvas_bayes_kde.figure.subplots()
	# 		### REPLACE THESE LINES ###
	# 		visuals.plot_lsv(data=[new_data], ax=ax_cdf)
	# 		visuals.plot_lsv(data=[new_data], ax=ax_kde)
	# 		###########################
	# 		self.figcanvas_bayes_cdf.draw()
	# 		self.figcanvas_bayes_kde.draw()
	# 	except TypeError:
	# 		self.update_status('Invalid fit parameters')

	# def choose_saveloc_bayes(self):
	# 	fd = QFileDialog()
	# 	fd.setViewMode(QFileDialog.Detail)
	# 	fd.setDefaultSuffix('png')
	# 	filename, _ = fd.getSaveFileName(self, 'Save Location', self.default_saveloc_bayes())
	# 	if not filename:
	# 		filename = self.default_saveloc_bayes()
	# 	self.saveloc_txtbx_bayes.setText(filename)

	# def save_action_bayes(self):
	# 	try:
	# 		fig_cdf = self.figcanvas_bayes_cdf.figure
	# 		fig_kde = self.figcanvas_bayes_kde.figure
	# 		loc = self.saveloc_txtbx_bayes.text()
	# 		dpi = self.figres_txtbx_bayes.text()
	# 		if not dpi.isdigit():
	# 			self.update_status('Figure resolution must be an integer')
	# 			dpi = 300
	# 		else:
	# 			dpi = int(dpi)
	# 		name, filetype = loc.split('.')
	# 		loc_cdf = name + '_CDF.' + filetype
	# 		loc_kde = name + '_KDE.' + filetype
	# 		fig_cdf.savefig(loc_cdf, dpi=dpi)
	# 		fig_kde.savefig(loc_kde, dpi=dpi)
	# 		self.update_status('Image saved successfully')
	# 	except Exception as e:
	# 		self.update_status('ERROR: ' + str(e))

	# def draw_plot_bayes(self):
	# 	try:
	# 		fig_cdf = self.figcanvas_bayes_cdf.figure
	# 		fig_kde = self.figcanvas_bayes_kde.figure
	# 		fig_cdf.clf()
	# 		fig_kde.clf()
	# 		ax_cdf = self.figcanvas_bayes_cdf.figure.subplots()
	# 		ax_kde = self.figcanvas_bayes_kde.figure.subplots()
	# 		bayes_data = self.vishandler.get_bayes_data()
	# 		self.bayes_dict = {d.get_label():d for d in bayes_data}
	# 		for n in self.bayes_dict.keys():
	# 			self.lineselector_menu_bayes.addItem(n)
	# 		this_data = bayes_data[0]
	# 		### REPLACE THESE LINES ###
	# 		visuals.plot_lsv(data=[this_data], ax=ax_cdf)
	# 		visuals.plot_lsv(data=[this_data], ax=ax_kde)
	# 		###########################
	# 		self.figcanvas_bayes_cdf.draw()
	# 		self.figcanvas_bayes_kde.draw()

	# 	except Exception as e:
	# 		self.update_status('ERROR: ' + str(e))

	# def get_ax_bayes(self):
	# 	fig_cdf = self.figcanvas_bayes_cdf.figure
	# 	fig_kde = self.figcanvas_bayes_kde.figure
	# 	ax_cdf = fig_cdf.get_axes()
	# 	ax_kde = fig_kde.get_axes()
	# 	return ax_cdf, ax_kde


	################
	# EIS Analysis #
	################
	### eis layout ###
	def eis_layout(self):
		# data selection header
		self.header_eis = QLabel('HFR Analysis')
		self.header_eis.setFont(IfesUI.headerfont)
		# use existing widgets
		self.useexisting_chkbx_eis = QCheckBox('Use previously loaded data')
		self.useexisting_chkbx_eis.setStyleSheet("QCheckBox"
							   "{"
							   "spacing :5px;"
							   "font-size : 25px;"
							   "}"
							   "QCheckBox::indicator"
							   "{"
							   "width :33px;"
							   "height : 25px;"
							   "}")
		self.useexisting_chkbx_eis.setCheckState(Qt.Unchecked)
		self.useexisting_chkbx_eis.setLayoutDirection(Qt.RightToLeft)
		#figure layout
		self.figlayout_eis = self.figure_layout_eis()
		# save plot header
		self.header_saveplot_eis = QLabel('Save Plot')
		self.header_saveplot_eis.setFont(IfesUI.headerfont)
		# save plot widgets
		self.saveloc_lbl_eis = QLabel('Save location')
		self.saveloc_txtbx_eis = QLineEdit()
		self.saveloc_btn_eis = QPushButton('Choose location...')
		self.save_btn_eis = QPushButton('Save Current Figures')
		# connect widgets
		self.useexisting_chkbx_eis.stateChanged.connect(self.useexisting_action_eis)
		self.saveloc_btn_eis.clicked.connect(self.choose_saveloc_eis)
		self.save_btn_eis.clicked.connect(self.save_action_eis)
		# build layout
		layout = QGridLayout()
		row = 0
		layout.addWidget(self.header_eis, row, 0, 1, -1, Qt.AlignHCenter)
		row += 1
		layout.addWidget(self.useexisting_chkbx_eis, row, 0, 1, -1, Qt.AlignRight)
		row += 1
		layout.addLayout(self.figlayout_eis, row, 0, 1, -1, Qt.AlignLeft)
		row += 1
		layout.addWidget(self.header_saveplot_eis, row, 0, 1, -1, Qt.AlignHCenter)
		row += 1
		layout.addWidget(self.saveloc_lbl_eis, row, 0)
		layout.addWidget(self.saveloc_txtbx_eis, row, 1)
		layout.addWidget(self.saveloc_btn_eis, row, 2)
		row += 1
		layout.addWidget(self.save_btn_eis, row, 0, 1, -1, Qt.AlignHCenter)

		return layout

	def figure_layout_eis(self):
	   		# plot features
		self.plotfeatures_eis = self.plotfeatures_layout_eis()
		# plot nyquist + hfr_2pts + hfr_linkk
		self.figcanvas_eis  = FigureCanvas(Figure(figsize=IfesUI.default_figsize))
		self.figcanvas_eis.figure.subplots()
		self.toolbar = NavigationToolbar(self.figcanvas_eis, self)
		#plot HFR = f(curr_density) + Frequency(HFR)
		self.figcanvas_eis1  = FigureCanvas(Figure(figsize=IfesUI.default_figsize))
		self.figcanvas_eis1.figure.subplots()
		self.toolbar1 = NavigationToolbar(self.figcanvas_eis1, self)
		# line properties header
		self.header_lineprops_eis = QLabel('Line Options')
		self.header_lineprops_eis.setFont(IfesUI.headerfont)
		#
		self.selector_figure_lbl = QLabel('Vizualisation type')
		self.selector_figure_lbl.setFont(IfesUI.valuefont)
		self.selector_figure_menu = QComboBox()
		self.selector_figure_menu.setFont(IfesUI.valuefont)
		for n in IfesUI.vis_types.keys():
			self.selector_figure_menu.addItem(n)
		self.selector_figure_menu.currentTextChanged.connect(self.vistype_selector_figure_action)
		# Both Pots HFR = f(i) & f = f(i)
		self.plot0_chkbx =QCheckBox('HFR and HFR Frequency vs. Current density')
		self.plot0_chkbx.setCheckState(Qt.Unchecked)
		self.plot0_chkbx.setLayoutDirection(Qt.RightToLeft)
		self.plot0_chkbx.stateChanged.connect(self.plot_HFR_FHFR)
		# Only HFR = f(i)
		self.plot1_chkbx =QCheckBox('HFR vs. Current density')
		self.plot1_chkbx.setCheckState(Qt.Unchecked)
		self.plot1_chkbx.setLayoutDirection(Qt.RightToLeft)
		self.plot1_chkbx.stateChanged.connect(self.plot_only_hfr_ii)
		# Only f = f(i)
		self.plot2_chkbx =QCheckBox('HFR Frequency vs. Current density')
		self.plot2_chkbx.setCheckState(Qt.Unchecked)
		self.plot2_chkbx.setLayoutDirection(Qt.RightToLeft)
		self.plot2_chkbx.stateChanged.connect(self.plot_only_f_ii)
		# Current Voltage curve
		self.plot3_chkbx =QCheckBox('I–U curve')
		self.plot3_chkbx.setCheckState(Qt.Unchecked)
		self.plot3_chkbx.setLayoutDirection(Qt.RightToLeft)
		self.plot3_chkbx.stateChanged.connect(self.plot_I_V_curve)
		# line selector menu
		self.lineselector_lbl_eis = QLabel('line selector')
		self.lineselector_menu_eis = QComboBox()
		self.lineselector_menu_eis.adjustSize()
		self.lineselector_lbl_eis.setFont(IfesUI.valuefont)
		# x-axis limits
		self.xmin_lbl_eis = QLabel('x min')
		self.xmin_txtbx_eis = QLineEdit()
		self.xmax_lbl_eis = QLabel('x max')
		self.xmax_txtbx_eis = QLineEdit()
		# y-axis limits
		self.ymin_lbl_eis = QLabel('y min')
		self.ymin_txtbx_eis = QLineEdit()
		self.ymax_lbl_eis = QLabel('y max')
		self.ymax_txtbx_eis = QLineEdit()
		self.xmin_txtbx_eis.textChanged.connect(self.xlim_action_eis)
		self.xmax_txtbx_eis.textChanged.connect(self.xlim_action_eis)
		self.ymin_txtbx_eis.textChanged.connect(self.ylim_action_eis)
		self.ymax_txtbx_eis.textChanged.connect(self.ylim_action_eis)
		 # plot features header
		self.header_plotparams_eis = QLabel('HFR Results')
		self.header_plotparams_eis.setFont(IfesUI.headerfont)
		# for n in IfesUI.tintin:
		# 	self.lineselector_menu_eis.addItem(n)
		# line properties layout
		# figure properties
		self.figprops_eis = self.figprops_layout_eis()
		self.lineselector_menu_eis.currentTextChanged.connect(self.lineselector_action_eis)
		# build layout
		layout = QGridLayout()
		
		# resize widgets
		
		# layout.addWidget(self.vistype_lbl, 1, 0, Qt.AlignLeft)
		# layout.addWidget(self.vistype_menu, 1, 1, Qt.AlignLeft)
		layout.addWidget(self.header_lineprops_eis, 0, 0,1,3)
		layout.addWidget(self.lineselector_lbl_eis, 1, 0, Qt.AlignLeft)
		layout.addWidget(self.lineselector_menu_eis, 2, 0,1,3)
		# layout.addWidget(self.xmin_lbl_eis, 2, 0, Qt.AlignRight)
		# layout.addWidget(self.xmin_txtbx_eis, 2, 1, Qt.AlignLeft)
		# layout.addWidget(self.xmax_lbl_eis, 2, 2, Qt.AlignLeft)
		# layout.addWidget(self.xmax_txtbx_eis, 2, 3, Qt.AlignLeft)
		# layout.addWidget(self.ymin_lbl_eis, 3, 0, Qt.AlignRight)
		# layout.addWidget(self.ymin_txtbx_eis, 3, 1, Qt.AlignLeft)
		# layout.addWidget(self.ymax_lbl_eis, 3, 2, Qt.AlignLeft)
		# layout.addWidget(self.ymax_txtbx_eis, 3, 3, Qt.AlignLeft)
		
		layout.addWidget(self.header_plotparams_eis, 4, 0, Qt.AlignLeft)
		# layout.addLayout(self.colslayout_eis, 1, 0, 1, 2, Qt.AlignLeft)
		layout.addLayout(self.plotfeatures_eis, 5, 0)
		layout.addWidget(self.figcanvas_eis, 0, 4, 6, 1)
		layout.addWidget(self.toolbar,6,4)
		layout.addWidget(self.figcanvas_eis1, 0, 5, 6, 1)
		layout.addWidget(self.toolbar1,6,5)
		# layout.addWidget(self.plot0_chkbx,7,5, Qt.AlignRight)
		# layout.addWidget(self.plot1_chkbx,8,5, Qt.AlignRight)
		# layout.addWidget(self.plot2_chkbx,9,5, Qt.AlignRight)
		# layout.addWidget(self.plot3_chkbx,10,5, Qt.AlignRight)
		layout.addWidget(self.selector_figure_lbl, 7, 4, Qt.AlignRight)
		layout.addWidget(self.selector_figure_menu, 7, 5,)
		# layout.addWidget(self.figcanvas_eis2, 7, 4, 6, 1)
		# layout.addWidget(self.toolbar15,10,5)
		
		# layout.addLayout(self.figprops_eis, 3, 2, 1, 1, Qt.AlignHCenter)
		for i in range(layout.count()):
			w = layout.itemAt(i).widget()
			if isinstance(w, QLineEdit):
				self.set_min_height(w)
				# self.set_min_width(w)
		self.set_max_width(self.xmin_txtbx_eis, 0.5)
		self.set_max_width(self.xmax_txtbx_eis, 0.5)
		self.set_max_width(self.ymin_txtbx_eis, 0.5)
		self.set_max_width(self.ymax_txtbx_eis, 0.5)
		return layout

	def plot_only_hfr_ii(self):
		eis_data = self.vishandler.get_eis_data()
		this_data = eis_data[0]
		fig5 = self.figcanvas_eis1.figure
		fig5.clf()
		ax5 = self.figcanvas_eis1.figure.subplots()
		ax5.set_title('HFR vs. Current density')
		visuals.plot_only_hfr_i(data = this_data, ax = ax5)
		self.figcanvas_eis1.draw()
		return 0

	def plot_only_f_ii(self):
		eis_data = self.vishandler.get_eis_data()
		this_data = eis_data[0]
		fig5 = self.figcanvas_eis1.figure
		fig5.clf()
		ax5 = self.figcanvas_eis1.figure.subplots()
		ax5.set_title('HFR Frequency vs. Current density')
		visuals.plot_only_f_i(data = this_data, ax = ax5)
		self.figcanvas_eis1.draw()
		return 0
	

	def plot_I_V_curve(self):
		eis_data = self.vishandler.get_eis_data()
		this_data = eis_data[0]
		fig5 = self.figcanvas_eis1.figure
		fig5.clf()
		ax5 = self.figcanvas_eis1.figure.subplots()
		ax5.set_title('I-U curve')
		visuals.plot_I_U_curve(data = this_data, ax = ax5)
		self.figcanvas_eis1.draw()
		# return 


	def plot_HFR_FHFR(self):
		eis_data = self.vishandler.get_eis_data()
		this_data = eis_data[0]
		fig5 = self.figcanvas_eis1.figure
		fig5.clf()
		ax5 = self.figcanvas_eis1.figure.subplots()
		ax5.set_title('HFR & HFR Frequency vs. Current density')
		visuals.plot_hfr_vs_curr_density(data = this_data, ax = ax5)
		self.figcanvas_eis1.draw()


	def vistype_selector_figure_action(self):
		vistype = self.selector_figure_menu.currentText()
		viscode = IfesUI.vis_types[vistype]
		if viscode == 0:
			self.plot_HFR_FHFR()
		elif viscode == 1:
			self.plot_only_hfr_ii()
		elif viscode == 2:
			self.plot_only_f_ii()
		elif viscode == 3:
			self.plot_I_V_curve()
		

	def colselection_layout_eis(self):

		# x column
		self.xcol_lbl_eis = QLabel('Real column')
		self.xcol_txtbx_eis = QLineEdit('1')
		# y column
		self.ycol_lbl_eis = QLabel('Imaginary column')
		self.ycol_txtbx_eis = QLineEdit('2')
		self.xcol_txtbx_eis.textChanged.connect(self.xcol_action_eis)
		self.ycol_txtbx_eis.textChanged.connect(self.ycol_action_eis)
		# build layout
		layout = QGridLayout()
		# row = 0
		# layout.addWidget(self.xcol_lbl_eis, row, 0, Qt.AlignLeft)
		# layout.addWidget(self.xcol_txtbx_eis, row, 1, Qt.AlignLeft)
		# row += 1
		# layout.addWidget(self.ycol_lbl_eis, row, 0, Qt.AlignLeft)
		# layout.addWidget(self.ycol_txtbx_eis, row, 1, Qt.AlignLeft)
		# resize widgets
		for i in range(layout.count()):
			w = layout.itemAt(i).widget()
			if isinstance(w, QLineEdit):
				self.set_max_width(w, 1.5)
		return layout

	def plotfeatures_layout_eis(self):
		#HFR Values
		# self.hfrlin_lbl = QLabel('HFR (linear fit):')
		# self.hfrlin_val = QLabel('')
		# self.hfrsemi_lbl = QLabel('HFR (semicircle fit):')
		# self.hfrsemi_val = QLabel('')
		self.hfr_twopts_lbl = QLabel('HFR in \u03A9 (2 points fit):')
		self.hfr_twopts_val = QLabel('')
		self.hfr_twopts_val.setStyleSheet("background-color: greenyellow; border: 2px solid black")
		self.hfrlinkk_lbl = QLabel('HFR in \u03A9 (LIN KK fit):')
		self.hfrlinkk_val = QLabel('')
		self.hfrarea_lbl = QLabel('HFR * Area in m\u03A9.cm\u00b2:')
		self.hfrarea_val = QLabel('')
		self.hfrlinkk_val.setStyleSheet("background-color: indianred; border: 2px solid black")
		self.frequency_hfr_lbl = QLabel('HFR Frequency in Hz :')
		self.frequency_hfr_val = QLabel('')
		self.frequency_hfr_val.setStyleSheet("color : white;"
											 "background-color: indigo;"
											 "border: 2px solid black;")
		# self.hfrlin_val.setFont(IfesUI.valuefont)
		# self.hfrsemi_val.setFont(IfesUI.valuefont)
		self.hfr_twopts_val.setFont(IfesUI.valuefont)
		self.hfrarea_val.setFont(IfesUI.valuefont)
		self.hfrlinkk_val.setFont(IfesUI.valuefont)
		self.frequency_hfr_val.setFont(IfesUI.valuefont)
		# x-axis label
		self.xlabel_lbl_eis = QLabel('x-axis label')
		self.xlabel_txtbx_eis = QLineEdit('$Z_{Re} [\Omega]]')
		# y-axis label
		self.ylabel_lbl_eis = QLabel('y-axis label')
		self.ylabel_txtbx_eis = QLineEdit('$Z_{Im} [\Omega]]')
		# # x-axis limits
		# self.xmin_lbl_eis = QLabel('x min')
		# self.xmin_txtbx_eis = QLineEdit()
		# self.xmax_lbl_eis = QLabel('x max')
		# self.xmax_txtbx_eis = QLineEdit()
		# # y-axis limits
		# self.ymin_lbl_eis = QLabel('y min')
		# self.ymin_txtbx_eis = QLineEdit()
		# self.ymax_lbl_eis = QLabel('y max')
		# self.ymax_txtbx_eis = QLineEdit()
		# connect widgets
		self.xlabel_txtbx_eis.textChanged.connect(self.xlabel_action_eis)
		self.ylabel_txtbx_eis.textChanged.connect(self.ylabel_action_eis)
		# self.xmin_txtbx_eis.textChanged.connect(self.xlim_action_eis)
		# self.xmax_txtbx_eis.textChanged.connect(self.xlim_action_eis)
		# self.ymin_txtbx_eis.textChanged.connect(self.ylim_action_eis)
		# self.ymax_txtbx_eis.textChanged.connect(self.ylim_action_eis)
		# build layout
		layout = QGridLayout()
		row = 0
		# layout.addWidget(self.hfrlin_lbl, row, 0, 1, 2, Qt.AlignLeft)
		# layout.addWidget(self.hfrlin_val, row, 2, 1, 2, Qt.AlignLeft)
		# row += 1
		# layout.addWidget(self.hfrsemi_lbl, row, 0, 1, 2, Qt.AlignLeft)
		# layout.addWidget(self.hfrsemi_val, row, 2, 1, 2, Qt.AlignLeft)
		# row += 1
		layout.addWidget(self.hfr_twopts_lbl, row, 0, 1, 2, Qt.AlignLeft)
		layout.addWidget(self.hfr_twopts_val, row, 2, 1, 2, Qt.AlignLeft)
		row += 1
		layout.addWidget(self.hfrlinkk_lbl, row, 0, 1, 2, Qt.AlignLeft)
		layout.addWidget(self.hfrlinkk_val, row, 2, 1, 2, Qt.AlignLeft)
		row += 1
		layout.addWidget(self.frequency_hfr_lbl, row, 0, 1, 2, Qt.AlignLeft)
		layout.addWidget(self.frequency_hfr_val, row, 2, 1, 2, Qt.AlignLeft)
		row += 1
		layout.addWidget(self.hfrarea_lbl, row, 0, 1, 2, Qt.AlignLeft)
		layout.addWidget(self.hfrarea_val, row, 2, 1, 2, Qt.AlignLeft)
		# row += 1
		# layout.addWidget(self.ylabel_lbl_eis, row, 0, 1, 2, Qt.AlignLeft)
		# layout.addWidget(self.ylabel_txtbx_eis, row, 2, 1, 2, Qt.AlignLeft)
		# row += 1
		# layout.addWidget(self.xmin_lbl_eis, row, 0, Qt.AlignLeft)
		# layout.addWidget(self.xmin_txtbx_eis, row, 1, Qt.AlignLeft)
		# layout.addWidget(self.xmax_lbl_eis, row, 2, Qt.AlignLeft)
		# layout.addWidget(self.xmax_txtbx_eis, row, 3, Qt.AlignLeft)
		# row += 1
		# layout.addWidget(self.ymin_lbl_eis, row, 0, Qt.AlignLeft)
		# layout.addWidget(self.ymin_txtbx_eis, row, 1, Qt.AlignLeft)
		# layout.addWidget(self.ymax_lbl_eis, row, 2, Qt.AlignLeft)
		# layout.addWidget(self.ymax_txtbx_eis, row, 3, Qt.AlignLeft)
		# # resize widgets
		# for i in range(layout.count()):
		#     w = layout.itemAt(i).widget()
		#     if isinstance(w, QLineEdit):
		#         self.set_min_height(w)
		#         # self.set_min_width(w)
		# self.set_max_width(self.xmin_txtbx_eis, 0.5)
		# self.set_max_width(self.xmax_txtbx_eis, 0.5)
		# self.set_max_width(self.ymin_txtbx_eis, 0.5)
		# self.set_max_width(self.ymax_txtbx_eis, 0.5)
		return layout

	def figprops_layout_eis(self):
		# fig width
		self.figw_lbl_eis = QLabel('Figure width')
		self.figw_txtbx_eis = QLineEdit(str(IfesUI.default_figsize[0]))
		# fig height
		self.figh_lbl_eis = QLabel('Figue height')
		self.figh_txtbx_eis = QLineEdit(str(IfesUI.default_figsize[1]))
		# fig resolution
		self.figres_lbl_eis = QLabel('Figure resolution (DPI)')
		self.figres_txtbx_eis = QLineEdit(str(IfesUI.default_figres))
		self.figw_txtbx_eis.textChanged.connect(self.figsize_action_eis)
		self.figh_txtbx_eis.textChanged.connect(self.figsize_action_eis)
		# build layout
		layout = QGridLayout()
		row = 0
		layout.addWidget(self.figw_lbl_eis, row, 0, Qt.AlignHCenter)
		layout.addWidget(self.figh_lbl_eis, row, 1, Qt.AlignHCenter)
		layout.addWidget(self.figres_lbl_eis, row, 2, Qt.AlignHCenter)
		row += 1
		layout.addWidget(self.figw_txtbx_eis, row, 0, Qt.AlignHCenter)
		layout.addWidget(self.figh_txtbx_eis, row, 1, Qt.AlignHCenter)
		layout.addWidget(self.figres_txtbx_eis, row, 2, Qt.AlignHCenter)
		for i in range(layout.count()):
			w = layout.itemAt(i).widget()
			if isinstance(w, QLineEdit):
				self.set_max_width(w, 0.75)
		return layout

	### eis actions ###
	def useexisting_action_eis(self):
		state = self.useexisting_chkbx_eis.isChecked()
		if state:
			if not self.datahandler.get_data():
				self.update_status('No data to visualize')
				self.useexisting_chkbx_eis.setCheckState(Qt.Unchecked)
				state = False
			else:
				self.vishandler.set_data(self.datahandler.get_data())
		# self.folder_lbl_eis.setEnabled(not state)
		# self.folder_txtbx_eis.setEnabled(not state)
		# self.folder_btn_eis.setEnabled(not state)
		# self.file_lbl_eis.setEnabled(not state)
		# self.file_txtbx_eis.setEnabled(not state)
		# self.file_btn_eis.setEnabled(not state)
		# self.loaddata_btn_eis.setEnabled(not state)
		if state:
			self.draw_plot_eis()

	def choose_folder_eis(self):
		fd = QFileDialog()
		filepath = fd.getExistingDirectory(self, 'Data Folder', IfesUI.homedir)
		if filepath:
			self.folder_txtbx_eis.setText(filepath)
			self.file_txtbx_eis.setText('')

	def choose_files_eis(self):
		fd = QFileDialog()
		files, _ = fd.getOpenFileNames(self, 'Data Files', IfesUI.homedir)
		if files:
			names = [os.path.basename(f) for f in files]
			folder = os.path.dirname(files[0])
			self.file_txtbx_eis.setText('; '.join(names))
			self.folder_txtbx_eis.setText(folder)

	def folder_action_eis(self):
		try:
			folder = self.folder_txtbx_eis.text()
			self.vishandler.set_datafolder(folder)
			self.file_action_eis()
		except Exception as e:
			self.update_status('ERROR: ' + str(e))

	def file_action_eis(self):
		file_str = self.file_txtbx_eis.text()
		folder = self.folder_txtbx_eis.text()
		try:
			if not file_str:
				files = self.get_all_files(folder, valid=utils.valid_types)
				self.file_txtbx_eis.setText('; '.join(files))
			else:
				files = file_str.split('; ')
			files = [os.path.join(folder, f) for f in files]
			self.vishandler.set_datafiles(files)
		except Exception as e:
			self.update_status('ERROR: ' + str(e))

	def loaddata_action_eis(self):
		try:
			self.vishandler.load_eis()
			self.draw_plot_eis()
		except Exception as e:
			self.update_status('ERROR: ' + str(e))

	def xcol_action_eis(self):
		col = self.xcol_txtbx_eis.text()
		if col.isdigit():
			col = int(col)
		self.vishandler.set_xcol(col)
		self.draw_plot_eis()

	def ycol_action_eis(self):
		col = self.ycol_txtbx_eis.text()
		if col.isdigit():
			col = int(col)
		self.vishandler.set_ycol(col)
		self.draw_plot_eis()

	def xlabel_action_eis(self):
		new_label = self.xlabel_txtbx_eis.text()
		ax = self.get_ax_eis()
		ax.set_xlabel(new_label)
		self.figcanvas_eis.draw()

	def ylabel_action_eis(self):
		new_label = self.ylabel_txtbx_eis.text()
		ax = self.get_ax_eis()
		ax.set_ylabel(new_label)
		self.figcanvas_eis.draw()

	def xlim_action_eis(self):
		xmin_text = self.xmin_txtbx_eis.text()
		xmax_text = self.xmax_txtbx_eis.text()
		ax = self.get_ax_eis()
		try:
			xmin = float(xmin_text)
			ax.set_xbound(lower=xmin)
		except ValueError:
			self.update_status('xmin must be a number')
		try:
			xmax = float(xmax_text)
			ax.set_xbound(upper=xmax)
		except ValueError:
			self.update_status('xmax must be a number')
		self.figcanvas_eis.draw()

	def ylim_action_eis(self):
		ymin_text = self.ymin_txtbx_eis.text()
		ymax_text = self.ymax_txtbx_eis.text()
		ax = self.get_ax_eis()
		try:
			ymin = float(ymin_text)
			ax.set_ybound(lower=ymin)
		except ValueError:
			self.update_status('ymin must be a number')
		try:
			ymax = float(ymax_text)
			ax.set_ybound(upper=ymax)
		except ValueError:
			self.update_status('ymax must be a number')
		self.figcanvas_eis.draw()

	def figsize_action_eis(self):
		fig = self.figcanvas_eis.figure
		width = self.figw_txtbx_eis.text()
		height = self.figh_txtbx_eis.text()
		try:
			width = float(width)
			height = float(height)
			fig.set_figwidth(width)
			fig.set_figheight(height)
			self.figcanvas_eis.draw()
		except ValueError:
			self.update_status('Figure width and height must be numbers')



	def lineselector_action_eis(self):
		try:
			i = 0
			new_label = self.lineselector_menu_eis.currentText()
			new_data = self.eis_dict[new_label]
			fig = self.figcanvas_eis.figure
			fig.clf()
			ax = self.figcanvas_eis.figure.subplots()
			ax.set_title('Nyquist Plot')
			visuals.plot_hfr(data=new_data, ax=ax)
			self.figcanvas_eis.draw()

			linkk_data = new_data.get_processed_data_linkk()
			fig1 = self.figcanvas_linkk.figure
			fig1.clf()
			fig1.tight_layout()
			ax1 = self.figcanvas_linkk.figure.subplots()
			# ax1.legend(['Data', 'LinKK'],loc = 'best')
			ax1.set_title('Nyquist Plot')
			visuals.plot_nyquist_linkk(data=linkk_data, ax=ax1)
			self.figcanvas_linkk.draw()
			fig2 = self.figcanvas_linkk1.figure
			fig2.clf()
			ax2 = self.figcanvas_linkk1.figure.subplots()
			ax2.set_title('Real & Imaginary Residuals Plot')
			visuals.plot_residuals_linkk(data=linkk_data, ax=ax2)
			self.figcanvas_linkk1.draw()
			fig3 = self.figcanvas_linkk2.figure
			fig3.clf()
			ax3 = self.figcanvas_linkk2.figure.subplots()
			ax3.set_title('Bode Magnitude Plot')
			visuals.plot_bode_amp_linkk(data=linkk_data, ax=ax3)
			ax3.legend(['Data', 'LinKK'],loc = 'best')
			self.figcanvas_linkk2.draw()
			fig4 = self.figcanvas_linkk3.figure
			fig4.clf()
			ax4 = self.figcanvas_linkk3.figure.subplots()
			ax4.set_title('Bode Phase Plot')
			visuals.plot_bode_phase_linkk(data=linkk_data, ax=ax4)
			ax4.legend(['Data', 'LinKK'],loc = 'best')
			self.figcanvas_linkk3.draw()

			# self.hfrsemi_val.setText(str(new_data.get_hfr()))
			self.hfr_twopts_val.setText(str(new_data.get_hfr_twopts()))
			self.hfrlinkk_val.setText(str(new_data.get_hfr_linkk()))
			self.hfrarea_val.setText(str(new_data.get_hfr_area()))
			self.frequency_hfr_val.setText(str(new_data.get_frequency_hfr()))

			#
			# self.hfr_twopts_val.setText(str("{:.5f}".format(new_data.get_hfr_twopts())))
			# self.hfrlinkk_val.setText(str("{:.5f}".format(new_data.get_hfr_linkk())))
			# self.hfrarea_val.setText(str("{:.5f}".format(new_data.get_hfr_area())))
			# self.frequency_hfr_val.setText(str("{:.5f}".format(new_data.get_frequency_hfr())))


			self.randle_val.setText(str(new_data.get_randle()))
			self.mu_val.setText(str(new_data.get_mu()))
			self.rmse_val.setText(str(new_data.get_rmse()))
			i += 1
		except TypeError:
			self.update_status('Invalid fit parameters')

	def choose_saveloc_eis(self):
		fd = QFileDialog()
		folder = fd.getExistingDirectory(self, 'Save Location', self.default_saveloc_vis())
		if not folder:
			folder = self.default_saveloc_vis()
		self.saveloc_txtbx_eis.setText(folder)
		# fd.setViewMode(QFileDialog.Detail)
		# fd.setDefaultSuffix('png')
		# filename, _ = fd.getSaveFileName(self, 'Save Location', self.default_saveloc_vis())
		# if not filename:
		# 	filename = self.default_saveloc_vis()
		# self.saveloc_txtbx_eis.setText(filename)

	def save_action_eis(self):
		name = self.lineselector_menu_eis.currentText()
		folder = self.saveloc_txtbx_eis.text()
		self.datahandler.set_saveloc(folder)
		try:
			fig = self.figcanvas_eis.figure
			fig1 = self.figcanvas_eis1.figure
			title = fig1.axes[0].get_title()
			loc1 = folder+'//'+ 'Nyquist_Plot_' + name+ '.png'
			loc2 = folder+'//'+ title + '.png'
			dpi = self.figres_txtbx_eis.text()
			if not dpi.isdigit():
				self.update_status('Figure resolution must be an integer')
				dpi = 300
			else:
				dpi = int(dpi)
			fig.savefig(loc1, dpi=dpi)
			fig1.savefig(loc2, dpi = dpi)
			self.update_status('Image saved successfully')
		except Exception as e:
			self.update_status('ERROR: ' + str(e))

	def draw_plot_eis(self):
		try:
			eis_data = self.vishandler.get_eis_data()
			self.eis_dict = {d.get_label():d for d in eis_data}
			current , voltage =[], []
			# i=0
			for n in self.eis_dict.keys():
				self.lineselector_menu_eis.addItem(n)
			# 	current1 = eis_data[i].get_current_data()
			# 	voltage1 = eis_data[i].get_potential_data() 
			# 	current.append(np.mean(current1))
			# 	voltage.append(np.mean(voltage1))
			# 	i +=1
			# this_data = eis_data[0]
			# fig5 = self.figcanvas_eis1.figure
			# fig5.clf()
			# ax5 = self.figcanvas_eis1.figure.subplots()
			# ax5.set_title('HFR & HFR Frequency vs. Current density')
			# visuals.plot_hfr_vs_curr_density(data = this_data, ax = ax5)
			# self.figcanvas_eis1.draw()
		except Exception as e:
			self.update_status('ERROR: ' + str(e))

	def get_ax_eis(self):
		fig = self.figcanvas_eis.figure
		ax = fig.get_axes()
		return ax[0]
	#####################
	#LIN Kramers Kronig #
	#####################
	### Linear Kramers Krönig layout ###
	def linkk_layout(self):
		# data selection header
		self.header_linkk = QLabel('LIN Kramers Kronig')
		self.header_linkk.setFont(IfesUI.headerfont)
		# use existing widgets & take the lead 
		self.useexisting_chkbx_linkk = QCheckBox('Take the lead')
		self.useexisting_chkbx_linkk.setStyleSheet("QCheckBox"
							   "{"
							   "spacing :5px;"
							   "font-size : 25px;"
							   "}"
							   "QCheckBox::indicator"
							   "{"
							   "width :33px;"
							   "height : 25px;"
							   "}")
		self.useexisting_chkbx_linkk.setCheckState(Qt.Unchecked)
		self.useexisting_chkbx_linkk.setLayoutDirection(Qt.RightToLeft)
		#figure layout
		self.figlayout_linkk = self.figure_layout_linkk()
		# save plot header
		self.header_saveplot_linkk = QLabel('Save Plot')
		self.header_saveplot_linkk.setFont(IfesUI.headerfont)
		# save plot widgets
		self.saveloc_lbl_linkk = QLabel('Save location')
		self.saveloc_txtbx_linkk = QLineEdit()
		self.saveloc_btn_linkk = QPushButton('Choose location...')
		self.save_btn_linkk = QPushButton('Save Current Figure')
		# connect widgets
		self.useexisting_chkbx_linkk.stateChanged.connect(self.useexisting_action_linkk)
		self.saveloc_btn_linkk.clicked.connect(self.choose_saveloc_linkk)
		self.save_btn_linkk.clicked.connect(self.save_action_linkk)
		# build layout
		layout = QGridLayout()
		row = 0
		layout.addWidget(self.header_linkk, row, 0, 1, -1, Qt.AlignHCenter)
		row += 1
		layout.addWidget(self.useexisting_chkbx_linkk, row, 0, 1, -1, Qt.AlignRight)
		row += 1
		layout.addLayout(self.figlayout_linkk, row, 0, 1, -1, Qt.AlignLeft)
		row += 1
		layout.addWidget(self.header_saveplot_linkk, row, 0, 1, -1, Qt.AlignHCenter)
		row += 1
		layout.addWidget(self.saveloc_lbl_linkk, row, 0)
		layout.addWidget(self.saveloc_txtbx_linkk, row, 1)
		layout.addWidget(self.saveloc_btn_linkk, row, 2)
		row += 1
		layout.addWidget(self.save_btn_linkk, row, 0, 1, -1, Qt.AlignHCenter)

		return layout

	def figure_layout_linkk(self):
		# plot features
		# actual figure
		#plot nyquist
		self.figcanvas_linkk  = FigureCanvas(Figure(figsize= (2,3)))
		self.figcanvas_linkk.figure.subplots()
		self.toolbar_linkk = NavigationToolbar(self.figcanvas_linkk, self)
		# plot residdual error real & imag
		self.figcanvas_linkk1  = FigureCanvas(Figure(figsize= (2,3)))
		self.figcanvas_linkk1.figure.subplots()
		self.toolbar_linkk1 = NavigationToolbar(self.figcanvas_linkk1, self)
		#plot bode_amplitude 
		self.figcanvas_linkk2  = FigureCanvas(Figure(figsize= (2,3)))
		self.figcanvas_linkk2.figure.subplots()
		self.toolbar_linkk2 = NavigationToolbar(self.figcanvas_linkk2, self)
		#plot bode_phase
		self.figcanvas_linkk3  = FigureCanvas(Figure(figsize= (2,3)))
		self.figcanvas_linkk3.figure.subplots()
		self.toolbar_linkk3 = NavigationToolbar(self.figcanvas_linkk3, self)
		# line properties header
		self.header_lineprops_linkk = QLabel('Line Options')
		self.header_lineprops_linkk.setFont(IfesUI.headerfont)
		# line selector menu
		self.lineselector_lbl_linkk = QLabel('line selector')
		self.lineselector_menu_linkk = QComboBox()
		self.lineselector_menu_linkk.adjustSize()
		self.lineselector_lbl_linkk.setFont(IfesUI.valuefont)
		# plot features header fitting result
		self.header_plotparams_linkk = QLabel('Fitting result')
		self.header_plotparams_linkk.setFont(IfesUI.headerfont)
		# figure properties
		# LinKK Values
		self.randle_lbl = QLabel('M:')
		self.randle_val = QLabel('')
		# self.randle_val.setStyleSheet("border: 2px solid black")
		self.mu_lbl = QLabel('mu:')
		self.mu_val = QLabel('')
		# self.mu_val.setStyleSheet("border: 2px solid black")
		self.rmse_lbl = QLabel('RMSE:')
		self.rmse_val = QLabel('')
		# self.rmse_val.setStyleSheet("border: 2px solid black")
		self.randle_val.setFont(IfesUI.valuefont)
		self.mu_val.setFont(IfesUI.valuefont)
		self.rmse_val.setFont(IfesUI.valuefont)
		#figpros
		self.figprops_linkk = self.figprops_layout_linkk()
		self.lineselector_menu_linkk.currentTextChanged.connect(self.lineselector_action_linkk)
		# build layout
		layout = QGridLayout()
		layout.addWidget(self.header_lineprops_linkk, 0, 0,1,6)
		layout.addWidget(self.lineselector_lbl_linkk, 1, 0)
		layout.addWidget(self.lineselector_menu_linkk, 1, 1,1,3)
		layout.addWidget(self.header_plotparams_linkk, 2,0,1,3)
		row = 3
		layout.addWidget(self.randle_lbl, row, 0)
		layout.addWidget(self.randle_val, row, 1)
		row += 1
		layout.addWidget(self.mu_lbl, row, 0)
		layout.addWidget(self.mu_val, row, 1)
		row +=1
		layout.addWidget(self.rmse_lbl,row,0)
		layout.addWidget(self.rmse_val,row,1)
		layout.addWidget(self.figcanvas_linkk, 0, 5,3,6)
		layout.addWidget(self.toolbar_linkk,3,5)
		layout.addWidget(self.figcanvas_linkk1, 0, 12,3,6)
		layout.addWidget(self.toolbar_linkk1,3,12)
		layout.addWidget(self.figcanvas_linkk2, 4, 5,3,6)
		layout.addWidget(self.toolbar_linkk2,7,5)
		layout.addWidget(self.figcanvas_linkk3, 4, 12,3,6)
		layout.addWidget(self.toolbar_linkk3,7,12)
		for i in range(layout.count()):
			w = layout.itemAt(i).widget()
			if isinstance(w, QLineEdit):
				self.set_min_height(w)
		return layout


   

	def figprops_layout_linkk(self):
		# fig width
		self.figw_lbl_linkk = QLabel('Figure width')
		self.figw_txtbx_linkk = QLineEdit(str(IfesUI.default_figsize[0]))
		# fig height
		self.figh_lbl_linkk = QLabel('Figue height')
		self.figh_txtbx_linkk = QLineEdit(str(IfesUI.default_figsize[1]))
		# fig resolution
		self.figres_lbl_linkk = QLabel('Figure resolution (DPI)')
		self.figres_txtbx_linkk = QLineEdit(str(IfesUI.default_figres))
		self.figw_txtbx_linkk.textChanged.connect(self.figsize_action_linkk)
		self.figh_txtbx_linkk.textChanged.connect(self.figsize_action_linkk)
		# build layout
		layout = QGridLayout()
		row = 0
		layout.addWidget(self.figw_lbl_linkk, row, 0, Qt.AlignHCenter)
		layout.addWidget(self.figh_lbl_linkk, row, 1, Qt.AlignHCenter)
		layout.addWidget(self.figres_lbl_linkk, row, 2, Qt.AlignHCenter)
		row += 1
		layout.addWidget(self.figw_txtbx_linkk, row, 0, Qt.AlignHCenter)
		layout.addWidget(self.figh_txtbx_linkk, row, 1, Qt.AlignHCenter)
		layout.addWidget(self.figres_txtbx_linkk, row, 2, Qt.AlignHCenter)
		for i in range(layout.count()):
			w = layout.itemAt(i).widget()
			if isinstance(w, QLineEdit):
				self.set_max_width(w, 0.75)
		return layout

	### linkk actions ###
	def useexisting_action_linkk(self):
		state = self.useexisting_chkbx_eis.isChecked()
		if state:
			if not self.datahandler.get_data():
				self.update_status('No data to visualize')
				self.useexisting_chkbx_linkk.setCheckState(Qt.Unchecked)
				state = False
			else:
				self.vishandler.set_data(self.datahandler.get_data())
		if state:
			self.draw_plot_linkk()


	def choose_folder_linkk(self):
		fd = QFileDialog()
		filepath = fd.getExistingDirectory(self, 'Data Folder', IfesUI.homedir)
		if filepath:
			self.folder_txtbx_linkk.setText(filepath)
			self.file_txtbx_linkk.setText('')

	def xcol_action_linkk(self):
		col = self.xcol_txtbx_linkk.text()
		if col.isdigit():
			col = int(col)
		self.vishandler.set_xcol(col)
		self.draw_plot_linkk()

	def ycol_action_linkk(self):
		col = self.ycol_txtbx_linkk.text()
		if col.isdigit():
			col = int(col)
		self.vishandler.set_ycol(col)
		self.draw_plot_linkk()

	def xlabel_action_linkk(self):
		new_label = self.xlabel_txtbx_linkk.text()
		ax = self.get_ax_linkk()
		ax.set_xlabel(new_label)
		self.figcanvas_linkk.draw()

	def ylabel_action_linkk(self):
		new_label = self.ylabel_txtbx_linkk.text()
		ax = self.get_ax_linkk()
		ax.set_ylabel(new_label)
		self.figcanvas_linkk.draw()

	def xlim_action_linkk(self):
		xmin_text = self.xmin_txtbx_linkk.text()
		xmax_text = self.xmax_txtbx_linkk.text()
		ax = self.get_ax_linkk()
		try:
			xmin = float(xmin_text)
			ax.set_xbound(lower=xmin)
		except ValueError:
			self.update_status('xmin must be a number')
		try:
			xmax = float(xmax_text)
			ax.set_xbound(upper=xmax)
		except ValueError:
			self.update_status('xmax must be a number')
		self.figcanvas_linkk.draw()

	def ylim_action_linkk(self):
		ymin_text = self.ymin_txtbx_linkk.text()
		ymax_text = self.ymax_txtbx_linkk.text()
		ax = self.get_ax_linkk()
		try:
			ymin = float(ymin_text)
			ax.set_ybound(lower=ymin)
		except ValueError:
			self.update_status('ymin must be a number')
		try:
			ymax = float(ymax_text)
			ax.set_ybound(upper=ymax)
		except ValueError:
			self.update_status('ymax must be a number')
		self.figcanvas_linkk.draw()

	def figsize_action_linkk(self):
		fig = self.figcanvas_linkk.figure
		width = self.figw_txtbx_linkk.text()
		height = self.figh_txtbx_linkk.text()
		try:
			width = float(width)
			height = float(height)
			fig.set_figwidth(width)
			fig.set_figheight(height)
			self.figcanvas_linkk.draw()
		except ValueError:
			self.update_status('Figure width and height must be numbers')

	def lineselector_action_linkk(self):
		try:
			i = 0
			new_label = self.lineselector_menu_linkk.currentText()
			new_data = self.linkk_dict[new_label]
			linkk_data = new_data.get_processed_data_linkk()
			fig1 = self.figcanvas_linkk.figure
			fig1.clf()
			# fig1.tight_layout()
			ax1 = self.figcanvas_linkk.figure.subplots()
			ax1.set_title('Nyquist Plot')
			visuals.plot_nyquist_linkk(data=linkk_data, ax=ax1)
			self.figcanvas_linkk.draw()
			fig2 = self.figcanvas_linkk1.figure
			fig2.clf()
			ax2 = self.figcanvas_linkk1.figure.subplots()
			ax2.set_title('Real & Imaginary Residuals Plot')
			visuals.plot_residuals_linkk(data=linkk_data, ax=ax2)
			self.figcanvas_linkk1.draw()
			fig3 = self.figcanvas_linkk2.figure
			fig3.clf()
			ax3 = self.figcanvas_linkk2.figure.subplots()
			ax3.set_title('Bode Magnitude Plot')
			visuals.plot_bode_amp_linkk(data=linkk_data, ax=ax3)
			ax3.legend(['Data', 'LinKK'],loc = 'best')
			self.figcanvas_linkk2.draw()
			fig4 = self.figcanvas_linkk3.figure
			fig4.clf()
			ax4 = self.figcanvas_linkk3.figure.subplots()
			ax4.set_title('Bode Phase Plot')
			visuals.plot_bode_phase_linkk(data=linkk_data, ax=ax4)
			ax4.legend(['Data', 'LinKK'],loc = 'best')
			self.figcanvas_linkk3.draw()
			self.randle_val.setText(str(new_data.get_randle()))
			self.mu_val.setText(str(new_data.get_mu()))
			self.rmse_val.setText(str(new_data.get_rmse()))
			i += 1
		except TypeError:
			self.update_status('Invalid fit parameters')

	def choose_saveloc_linkk(self):
		fd = QFileDialog()
		folder = fd.getExistingDirectory(self, 'Save Location', self.default_saveloc_vis())
		if not folder:
			folder = self.default_saveloc_vis()
		self.saveloc_txtbx_linkk.setText(folder)
		# fd.setViewMode(QFileDialog.Detail)
		# fd.setDefaultSuffix('png')
		# filename, _ = fd.getSaveFileName(self, 'Save Location', self.default_saveloc_vis())
		# if not filename:
		# 	filename = self.default_saveloc_vis()
		# self.saveloc_txtbx_linkk.setText(filename)

	def save_action_linkk(self):
		name = self.lineselector_menu_linkk.currentText()
		folder = self.saveloc_txtbx_linkk.text()
		self.datahandler.set_saveloc(folder)
		directory = 'LINKK'
		path = os.path.join(folder, directory)
		try: 
			os.mkdir(path) 
		except OSError as error: 
			print(error)
		try:
			fig = self.figcanvas_linkk.figure
			fig1 = self.figcanvas_linkk1.figure
			fig2 = self.figcanvas_linkk2.figure
			fig3 = self.figcanvas_linkk3.figure
			loc = path + '//'+ 'Nyquist_plot_LINKK_' + name +'.png'
			loc1 = path + '//'+ 'Real&Imaginary_residuals_plot_LINKK_'+ name +'.png'
			loc2 = path + '//'+ 'Bode_Maagnitude_plot_LINKK_' + name +'.png'
			loc3 = path + '//'+ 'Bode_Phase_plot_LINKK_' + name+ '.png'
			dpi = self.figres_txtbx_linkk.text()
			if not dpi.isdigit():
				self.update_status('Figure resolution must be an integer')
				dpi = 300
			else:
				dpi = int(dpi)
			fig.savefig(loc, dpi=dpi) 
			fig1.savefig(loc1, dpi=dpi) 
			fig2.savefig(loc2, dpi=dpi) 
			fig3.savefig(loc3, dpi=dpi) 
			self.update_status('Image saved successfully')
		except Exception as e:
			self.update_status('ERROR: ' + str(e))

	def draw_plot_linkk(self):
		try:
			eis_data = self.vishandler.get_eis_data()
			self.linkk_dict = {d.get_label():d for d in eis_data}
			for n in self.linkk_dict.keys():
				self.lineselector_menu_linkk.addItem(n)

		except Exception as e:
			self.update_status('ERROR: ' + str(e))

	def get_ax_linkk(self):
		fig = self.figcanvas_linkk.figure
		ax = fig.get_axes()
		return ax[0]

	######################
	# Equivalent circuit #
	######################
	def EC_layout(self):
		self.header_ec = QLabel(' Equivalent Circuit')
		self.header_ec.setFont(IfesUI.headerfont)
		# Run data button automatically
		self.rundata_btn_ec = QPushButton('Run')
		self.rundata_btn_ec.setFont(IfesUI.notefont)
		self.rundata_btn_ec.setFixedSize(120,60)
		self.rundata_btn_ec.setStyleSheet("background-color: slateblue")
		# use existing widgets & take the lead 
		self.useexisting_chkbx_ec = QCheckBox('Take the lead and click "GO" to run')
		self.useexisting_chkbx_ec.setStyleSheet("QCheckBox"
							   "{"
							   "spacing :5px;"
							   "font-size : 25px;"
							   "}"
							   "QCheckBox::indicator"
							   "{"
							   "width :33px;"
							   "height : 25px;"
							   "}")
		self.useexisting_chkbx_ec.setCheckState(Qt.Unchecked)
		self.useexisting_chkbx_ec.setLayoutDirection(Qt.RightToLeft)
		# Run data button frol line selector 
		self.rundata_btn_ec_line_selector = QPushButton('GO')
		self.rundata_btn_ec_line_selector.setFont(IfesUI.notefont)
		self.rundata_btn_ec_line_selector.setFixedSize(80,40)
		self.rundata_btn_ec_line_selector.setStyleSheet("background-color: mediumslateblue")
		#figure layout
		self.figlayout_ec = self.figure_layout_ec()
		# save plot header
		self.header_saveplot_ec = QLabel('Save Plot')
		self.header_saveplot_ec.setFont(IfesUI.headerfont)
		# save plot widgets
		self.saveloc_lbl_ec = QLabel('Save location')
		self.saveloc_txtbx_ec = QLineEdit()
		self.saveloc_btn_ec = QPushButton('Choose location...')
		self.save_btn_ec = QPushButton('Save Current Figure and Fitting Results')
		
		
		# connect widgets
		
		self.useexisting_chkbx_ec.stateChanged.connect(self.useexisting_action_ec)
		self.saveloc_btn_ec.clicked.connect(self.choose_saveloc_ec)
		self.save_btn_ec.clicked.connect(self.save_action_ec)
		self.rundata_btn_ec.clicked.connect(self.process_fitting)
		
		# build layout
		layout = QGridLayout()
		row = 0
		layout.addWidget(self.header_ec, row, 0, 1, -1, Qt.AlignHCenter)
		layout.addWidget(self.useexisting_chkbx_ec, row, 0, 1, -1, Qt.AlignRight)
		row += 1
		layout.addWidget(self.rundata_btn_ec, row, 0, 1, -1, Qt.AlignHCenter)
		layout.addWidget(self.rundata_btn_ec_line_selector, row,0 )
		row += 1
		layout.addLayout(self.figlayout_ec, row, 0, 1, -1, Qt.AlignLeft)
		row += 1
		layout.addWidget(self.header_saveplot_ec, row, 0, 1, -1, Qt.AlignHCenter)
		row += 1
		layout.addWidget(self.saveloc_lbl_ec, row, 0)
		layout.addWidget(self.saveloc_txtbx_ec, row, 1)
		layout.addWidget(self.saveloc_btn_ec, row, 2)
		row += 1
		layout.addWidget(self.save_btn_ec, row, 0, 1, -1, Qt.AlignHCenter)

		return layout

	def figure_layout_ec(self):
		#plot fitting results
		#plot nyquist
		self.figcanvas_ec = FigureCanvas(Figure(figsize= (2,3)))
		self.figcanvas_ec.figure.subplots()
		self.toolbar_ec = NavigationToolbar(self.figcanvas_ec, self)
		#plot bode_amp
		self.figcanvas_ec1 = FigureCanvas(Figure(figsize= (2,3)))
		self.figcanvas_ec1.figure.subplots()
		self.toolbar_ec1 = NavigationToolbar(self.figcanvas_ec1, self)
		#plot bode_phase
		self.figcanvas_ec2 = FigureCanvas(Figure(figsize= (2,3)))
		self.figcanvas_ec2.figure.subplots()
		self.toolbar_ec2 = NavigationToolbar(self.figcanvas_ec2, self)
		#plot residuals
		self.figcanvas_ec3 = FigureCanvas(Figure(figsize= (2,3)))
		self.figcanvas_ec3.figure.subplots()
		self.toolbar_ec3 = NavigationToolbar(self.figcanvas_ec3, self)
		# line properties header
		self.header_lineprops_ec = QLabel('Line Options')
		self.header_lineprops_ec.setFont(IfesUI.headerfont)
		# line selector menu
		self.lineselector_lbl_ec = QLabel('line selector')
		self.lineselector_menu_ec= QComboBox()
		self.lineselector_menu_ec.adjustSize()
		self.lineselector_lbl_ec.setFont(IfesUI.valuefont)
		# plot features header
		self.header_circuitFit_ec = QLabel('Circuit Fit Analysis')
		self.header_circuitFit_ec.setFont(IfesUI.headerfont1)
		#Initial guess
		#circuit guess
		self.circuit_guess_lbl_ec = QLabel('Circuit guess')#
		self.circuit_guess_lbl_ec.setFont(IfesUI.valuefont)
		self.circuit_guess_txtbx_ec = QLineEdit('R_0-p(R_1,CPE_1)-p(R_2,CPE_2)')#
		self.circuit_guess_txtbx_ec.setFixedWidth(300)
		#parameters guess
		self.parameter_guess_lbl_ec = QLabel('Parameters guess')
		self.parameter_guess_lbl_ec.setFont(IfesUI.valuefont)
		self.parameter_guess_txtbx_ec = QLineEdit('1.48e-02,0.002, 0.5, 0.00001, 0.0005, 0.0001,0.5')
		self.parameter_guess_txtbx_ec.setFixedWidth(300)
		#Fitting results
		#circuit fit
		self.fitting_rslt_lbl_ec = QLabel('Fitting results')
		self.fitting_rslt_val_ec = QLabel('')
		self.fitting_rslt_val_ec.setFont(IfesUI.valuefont)
		self.fitting_rslt_lbl_ec.setFont(IfesUI.valuefont)
		#error statistics
		self.error_stat_lbl_ec = QLabel('Error Statistics')
		self.error_stat_val_ec = QLabel('')
		self.error_stat_val_ec.setFont(IfesUI.valuefont)
		self.error_stat_lbl_ec.setFont(IfesUI.valuefont)
		#frequency range 
		self.freqpred_lbl_ec = QLabel('Frequency range')
		self.freqpred_lbl_ec.setFont(IfesUI.valuefont)
		self.startfrequency_lbl_ec = QLabel('Start')
		self.startfrequency_txtbx_ec = QLineEdit('Start')
		self.endfrequency_lbl_ec = QLabel('End')
		self.endfrequency_txtbx_ec = QLineEdit('End')
		# use previous initial guess for the ECC fit 
		self.rundata_btn_ec_with_same_IG = QPushButton('Use the previous initial guess')
		self.rundata_btn_ec_with_same_IG.setFixedSize(200,20)
		self.rundata_btn_ec_with_same_IG.setFont(IfesUI.notefont)
		self.rundata_btn_ec_with_same_IG.setStyleSheet("background-color: sandybrown")
		
		#connect data
		# self.lineselector_menu_ec.currentTextChanged.connect(self.lineselector_action_ec)
		self.circuit_guess_txtbx_ec.textChanged.connect(self.get_circuit_guess_ec)
		self.parameter_guess_txtbx_ec.textChanged.connect(self.get_parameter_guess_ec)
		# self.lineselector_menu_ec.currentTextChanged.connect(self.lineselector_action_ec)
		self.rundata_btn_ec_line_selector.clicked.connect(self.lineselector_action_ec)
		self.rundata_btn_ec_with_same_IG.clicked.connect(self.action_ec_using_previous_guess)
	   
		# build layout 
		layout = QGridLayout()
		# layout.addWidget(self.header_lineprops_ec, 0, 0,1,3)
		layout.addWidget(self.lineselector_lbl_ec, 1, 0,1,3)
		layout.addWidget(self.lineselector_menu_ec, 1, 1,1,2)
		# layout.addWidget(self.freqpred_lbl_ec, 2, 0,1,3,Qt.AlignLeft)
		# # layout.addWidget(self.startfrequency_lbl_ec, 3, 0,Qt.AlignLeft)
		# layout.addWidget(self.startfrequency_txtbx_ec, 3, 0,Qt.AlignLeft)
		# # layout.addWidget(self.endfrequency_lbl_ec, 3, 2,Qt.AlignLeft)
		# layout.addWidget(self.endfrequency_txtbx_ec, 3, 1,Qt.AlignLeft)
		layout.addWidget(self.rundata_btn_ec_with_same_IG, 2, 0,2,2,Qt.AlignLeft)
		layout.addWidget(self.header_circuitFit_ec,5,0,1,2 ,Qt.AlignLeft)
		layout.addWidget(self.circuit_guess_lbl_ec,6,0,1,3,Qt.AlignLeft)
		layout.addWidget(self.circuit_guess_txtbx_ec,7,0,1,3,Qt.AlignLeft)
		layout.addWidget(self.parameter_guess_lbl_ec,8,0,1,3,Qt.AlignLeft)
		layout.addWidget(self.parameter_guess_txtbx_ec,9,0,1,2,Qt.AlignLeft)
		layout.addWidget(self.fitting_rslt_lbl_ec,10,0,1,3,Qt.AlignLeft)
		layout.addWidget(self.fitting_rslt_val_ec,11,0,16,5,Qt.AlignLeft)
		layout.addWidget(self.error_stat_lbl_ec,30,0,1,3,Qt.AlignLeft)
		layout.addWidget(self.error_stat_val_ec,31,0,1,3,Qt.AlignLeft)
		layout.addWidget(self.figcanvas_ec, 0, 5,12,3)
		layout.addWidget(self.toolbar_ec,13,5)
		layout.addWidget(self.figcanvas_ec1, 0, 13,12,3)
		layout.addWidget(self.toolbar_ec1,13,13)
		layout.addWidget(self.figcanvas_ec2, 15, 5,12,3)
		layout.addWidget(self.toolbar_ec2,27,5)
		layout.addWidget(self.figcanvas_ec3, 15, 13,12,3)
		layout.addWidget(self.toolbar_ec3,27,13)

		return layout

	def useexisting_action_ec(self):
		state = self.useexisting_chkbx_eis.isChecked()
		if state:
			if not self.datahandler.get_data():
				self.update_status('No data to visualize')
				self.useexisting_chkbx_ec.setCheckState(Qt.Unchecked)
				state = False
			else:
				self.vishandler.set_data(self.datahandler.get_data())
		if state:
			self.draw_plot_ec()

	def draw_plot_ec(self):
		try:
			eis_data = self.vishandler.get_eis_data()
			self.ec_dict = {d.get_label():d for d in eis_data}
			for n in self.ec_dict.keys():
				self.lineselector_menu_ec.addItem(n)

		except Exception as e:
			self.update_status('ERROR: ' + str(e))

	def get_circuit_guess_ec(self):
		guess = self.circuit_guess_txtbx_ec.text()
		# if isinstance(guess, str):
		# guess = guess.split(';')
		return guess

	def get_parameter_guess_ec(self):
		guess = self.parameter_guess_txtbx_ec.text()
		guess = guess.split(',')
		return guess

	def get_previous_initial_guess(self):
		return self.previous_initial_guess

	def set_previous_initial_guess(self, new_val):
		self.previous_initial_guess = new_val

	def lineselector_action_ec(self):
		try:
			i = 0
			new_label = self.lineselector_menu_ec.currentText()
			new_data = self.ec_dict[new_label]
			fig = self.figcanvas_ec.figure
			fig.clf()
			fig1 = self.figcanvas_ec1.figure
			fig1.clf()
			fig2 = self.figcanvas_ec2.figure
			fig2.clf()
			fig3 = self.figcanvas_ec3.figure
			fig3.clf()
			self.error_stat_val_ec.clear()
			self.fitting_rslt_val_ec.clear()
			# get dat 
			linkk_data = new_data.get_processed_data_linkk()
			Z = linkk_data['Z in Ohm']
			f = linkk_data['Frequency in Hz']
			Z = np.asarray(Z)
			f = np.asarray(f)
			circuit_gues = str(self.get_circuit_guess_ec())
			params_guess = self.get_parameter_guess_ec()
			params_guess1 = list(np.float_(params_guess))
			coucou = CustomCircuit(initial_guess= params_guess1,circuit=circuit_gues)
			coucou.fit(f,Z)
			# Fit results
			elements , units = [] , []
			elements,units = coucou.get_param_names()
			fitted_params , fitted_errors = [],[]
			fitted_params , fitted_errors = coucou.get_fitted_data(f,Z)
			self.set_previous_initial_guess(list(np.float_(fitted_params)))
			df = pd.DataFrame({'Elements': elements, 'Fit value':fitted_params, 'Error range (+/-)': fitted_errors, 'Unit': units })
			#
			f_pred = np.logspace(10,-1)
			coucou1 = coucou.predict(f_pred)
			coucou2 = coucou.predict(f)
			#plot nyquist 
			ax = self.figcanvas_ec.figure.subplots()
			plot_nyquistlinkk(ax, Z, fmt='s')
			plot_nyquistlinkk(ax,coucou1, fmt='-')
			ax.legend(['Data', 'Custom Circuit'],loc = 'best')
			# ax.legend(['Data', 'Custom Circuit'])
			ax.set_title('Nyquist Plot')
			self.figcanvas_ec.draw()
			# plot residuals
			res_meas_real = (Z - coucou.predict(f)).real/np.abs(Z)
			res_meas_imag = (Z - coucou.predict(f)).imag/np.abs(Z)
			ax1 = self.figcanvas_ec1.figure.subplots()
			plot_residuals(ax1, f, res_meas_real, res_meas_imag)
			ax1.set_title('Real & Imaginary Residuals Plot')
			self.figcanvas_ec1.draw()
			#plot bode 
			# Amplitude
			ax2 = self.figcanvas_ec2.figure.subplots()
			
			plot_bode_amp(ax2,f, Z)
			plot_bode_amp(ax2,f, coucou2)
			ax2.legend(['Data', 'Custom Circuit'],loc = 'best')
			ax2.set_title('Bode Magnitude Plot')
			self.figcanvas_ec2.draw()
			# Phase 
			ax3 = self.figcanvas_ec3.figure.subplots()
			plot_bode_phase(ax3,f, Z)
			plot_bode_phase(ax3,f,coucou2)
			ax3.legend(['Data', 'Custom Circuit'],loc = 'best')
			ax3.set_title('Bode Phase Plot')
			self.figcanvas_ec3.draw()
			# Error 
			error = rmse(Z,coucou2)
			self.error_stat_val_ec.setText(str(error))
			self.fitting_rslt_val_ec.setText(str(coucou))
			i +=1
		except TypeError:
			self.update_status('Invalid fit parameters')
		return df


	def action_ec_using_previous_guess(self):
		x = self.get_previous_initial_guess()
		self.parameter_guess_txtbx_ec.setText(str(x)[1:-1])



	def process_fitting(self):
		#clear plots
		fig = self.figcanvas_ec.figure
		fig.clf()
		fig1 = self.figcanvas_ec1.figure
		fig1.clf()
		fig2 = self.figcanvas_ec2.figure
		fig2.clf()
		fig3 = self.figcanvas_ec3.figure
		fig3.clf()
		circuit_gues = str(self.get_circuit_guess_ec())
		params_guess = self.get_parameter_guess_ec()
		params_guess1 = list(np.float_(params_guess))
		coucou = CustomCircuit(initial_guess= params_guess1,circuit=circuit_gues)
		new_label = self.lineselector_menu_eis.currentText()
		new_data = self.eis_dict[new_label]
		linkk_data = new_data.get_processed_data_linkk()
		Z = linkk_data['Z in Ohm']
		f = linkk_data['Frequency in Hz']
		Z = np.asarray(Z)
		f = np.asarray(f)
		coucou.fit(f,Z)
		elements , units = [] , []
		elements,units = coucou.get_param_names()
		fitted_params , fitted_errors = [],[]
		fitted_params , fitted_errors = coucou.get_fitted_data(f,Z)
		self.set_previous_initial_guess(list(np.float_(fitted_params)))
		df = pd.DataFrame({'Elements': elements, 'Fit value':fitted_params, 'Error range (+/-)': fitted_errors, 'Unit': units })
		f_pred = np.logspace(10,-1)
		coucou1 = coucou.predict(f_pred)
		coucou2 = coucou.predict(f)
		ax = self.figcanvas_ec.figure.subplots()
		plot_nyquistlinkk(ax, Z, fmt='s')
		plot_nyquistlinkk(ax,coucou1, fmt='-')
		ax.legend(['Data', 'Custom Circuit'],loc = 'best') # loc = 'best'
		ax.set_title('Nyquist Plot')
		self.figcanvas_ec.draw()
		res_meas_real = (Z - coucou.predict(f)).real/np.abs(Z)
		res_meas_imag = (Z - coucou.predict(f)).imag/np.abs(Z)
		ax1 = self.figcanvas_ec1.figure.subplots()
		plot_residuals(ax1, f, res_meas_real, res_meas_imag)
		ax1.set_title('Real & Imaginary Residuals Plot')
		self.figcanvas_ec1.draw()
		ax2 = self.figcanvas_ec2.figure.subplots()
		plot_bode_amp(ax2,f, Z)
		plot_bode_amp(ax2,f, coucou2)
		ax2.legend(['Data', 'Custom Circuit'],loc = 'best')
		ax2.set_title('Bode Magnitude Plot')
		# ax2.legend(['Data', 'Custom Circuit'])
		self.figcanvas_ec2.draw()
		ax3 = self.figcanvas_ec3.figure.subplots()
		plot_bode_phase(ax3,f, Z)
		plot_bode_phase(ax3,f,coucou2)
		ax3.legend(['Data', 'Custom Circuit'],loc = 'best')
		# ax3.legend(['Data', 'Custom Circuit'])
		ax3.set_title('Bode Phase Plot')
		self.figcanvas_ec3.draw()
		error = rmse(Z,coucou2)
		self.error_stat_val_ec.setText(str(error))
		self.fitting_rslt_val_ec.setText(str(coucou))
		return coucou

	def choose_saveloc_ec(self):
		fd = QFileDialog()
		folder = fd.getExistingDirectory(self, 'Save Location', self.default_saveloc_vis())
		if not folder:
			folder = self.default_saveloc_vis()
		self.saveloc_txtbx_ec.setText(folder)


	def save_action_ec(self):
		df = self.lineselector_action_ec()
		name = self.lineselector_menu_ec.currentText()
		folder = self.saveloc_txtbx_ec.text()
		self.datahandler.set_saveloc(folder)
		directory = 'Equivalent Circuit'
		path = os.path.join(folder, directory)
		try: 
			os.mkdir(path) 
		except OSError as error: 
			print(error)
		try:
			fig = self.figcanvas_ec.figure
			fig1 = self.figcanvas_ec1.figure
			fig2 = self.figcanvas_ec2.figure
			fig3 = self.figcanvas_ec3.figure
			loc = path + '//'+ 'Nyquist_plot_EC_' +name + '.png'
			loc1 = path + '//'+ 'Real&Imaginary_residuals_plot_EC_' +name + '.png'
			loc2 = path + '//'+ 'Bode_Maagnitude_plot_EC_' +name + '.png'
			loc3 = path + '//'+ 'Bode_Phase_plot_EC_' +name + '.png'
			dpi = self.figres_txtbx_eis.text()
			utils.save_data(df, name+'.csv',path )
			if not dpi.isdigit():
				self.update_status('Figure resolution must be an integer')
				dpi = 300
			else:
				dpi = int(dpi)
			fig.savefig(loc, dpi=dpi) 
			fig1.savefig(loc1, dpi=dpi) 
			fig2.savefig(loc2, dpi=dpi) 
			fig3.savefig(loc3, dpi=dpi) 
			self.update_status('Image saved successfully')
		except Exception as e:
			self.update_status('ERROR: ' + str(e))





def main():
	app = QApplication(sys.argv)
	window = IfesWindow()
	ui = IfesUI(window)
	window.show()
	app.exec_()

if __name__ == "__main__":
	sys.exit(main())