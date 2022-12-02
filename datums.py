import this
from typing import final
import numpy as np
import pandas as pd
import visuals
import sys
from scipy import stats
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from scipy import stats, interpolate, optimize
from scipy.optimize import curve_fit
import os
import model
import re
import utils
from model import Datum
from impedance.models.circuits import CustomCircuit, Randles
from impedance import preprocessing
from impedance.models.circuits.fitting import rmse
from impedance.visualization import plot_nyquist, plot_residuals,plot_bode
from impedance.validation import linKK

dlm_default = utils.dlm_default
col_default_labels = {'frequency':'f','current':'i', 'potential':'v', 'time':'t', 'current_err':'i_sd', 'potential_err':'v_sd', 'overpotential':'eta', 'tafelcurrent':'log(ioi)', 'realcurr':'reall', 'imagcurr':'imag'}
col_default_ids = {'current':2, 'potential':1, 'frequency':0, 'time':0, 'current_err':2, 'potential_err':3, 'overpotential':2, 'tafelcurrent':3}
ref_electrodes = {'she':0, 'sce':0.241}
thermo_potentials = {'none':0, 'oer':1.23}
expt_types_all = ['cv', 'cp', 'ca', 'lsv', 'eis']




def load_data(filename=None, folder=None, pattern='', expt_type='', filetype='', delimiter=dlm_default):

	"""
	Loads data file(s) as a Datum Object
	Function to load electrochemical data files as a Datum object. If called with no
	arguments, loads all supported data files in the present folder.
	Parameters
	___________
	filename: str, path object, or file-like (default=None)
		Full filename of a file in the present directory or a complete path to an individual file. If filename is specified, all other arguments except delimiter are ignored.
	folder: str, path object, or path-like (default=None)
		Directory in which data files are stored. If none, defaults to the present directory.
	pattern: str or regex
		If specified, only files matching this pattern in the specified folder are loaded. Ignored if filename is specified.
	expt_type: str (default='')
		Alternative to specifying pattern; ignored if pattern is specified. All files containing expt_type anywhere in the file name will be loaded. Ex: to load all chronopotentiometry files, specify expt_type='cp'.
	filetype : str
		Any supported filetype. Only files of the specified file type will be loaded. Can be used in conjunction with pattern or expt_type.
	delimiter : char (default = '\t')
		Delimiting character if the file is a text file. Defaults to '\t' (tab-delimiting).
	Returns
	________
	data:list of Datum
		Returns a list of Datum objects, with each entry corresponding to an individual data file
	"""
	data = []

	if filename:
		if type(filename) != list:
			filename = [filename]
		# for f in filename:
		# 	data.append(utils.read_file(f, delimiter))
	if folder:
		dirpath = os.path.realpath(folder)
	else:
		dirpath = os.getcwd()
	if expt_type and not pattern:

		pattern = r'.*' + expt_type + r'.*'
	files = utils.get_files(dirpath, pattern, filetype, filename)
	for f in files:
		path = os.path.join(dirpath, f)
		this_data = utils.read_file(path, delimiter)
		if expt_type:
			this_data.set_expt_type(expt_type.lower())
		else:
			for this_type in expt_types_all:
				pattern = r'.*' + this_type + r'.*'
				if re.match(pattern, f):
					this_data.set_expt_type(this_type.lower())
					break

		if this_data is not None:
			data.append(this_data)
	return data


def linkk_process(data=None, freq_column=0, real_column=1, imag_column=2):
	if data is None:
		data = eis_raw(**kwargs)
	new_data = []
	for d in data:
		if d.get_expt_type() == 'eis':
			basename = d.get_name()
			raw = d.get_raw_data()
			### TODO: add support for GEIS and PEIS specifically, as well as frequency analysis ###
			freq_all = np.asarray(raw.iloc[:,0])
			real_all = np.asarray(raw.iloc[:,1])
			imag_all = np.asarray(raw.iloc[:,2])
			f , Z = drop_neg_and_split_zeros(real_all, imag_all, freq_all)
			M, mu, Z_linKK, res_real, res_imag = linKK(f, Z, c=.5, max_M=100, fit_type='complex', add_cap=True)
			processed = pd.DataFrame({'Frequency in Hz':freq_all,'Z in Ohm': Z, 'Z_linkk in Ohm':Z_linKK})
			d.set_processed_data(processed)
			new_data.append(d)
			if export_data:
				name = d.get_name()
				save_data(processed, name+'.csv', save_dir)
	return new_data


def ca_raw(filename=None, folder=None, pattern='', filetype='', delimiter=dlm_default):
	"""
	Loads chronoamperometry data
	Efficient way to load multiple chronoamperometry data files at once; equivalent to calling load_data and specifying expt_type='ca'. If called with no arguments, loads all chronoamperometryd files in the present folder.
	Parameters
	___________
	filename: str, path object, or file-like (default=None)
		Full filename of a file in the present directory or a complete path to an individual file. If filename is specified, all other arguments except delimiter are ignored.
	folder: str, path object, or path-like (default=None)
		Directory in which data files are stored. If none, defaults to the present directory.
	pattern: str or regex
		If specified, only files matching this pattern in the specified folder are loaded. Ignored if filename is specified.
	filetype : str
		Any supported filetype. Only files of the specified file type will be loaded. Can be used in conjunction with pattern or expt_type.
	delimiter : char (default = '\t')
		Delimiting character if the file is a text file. Defaults to '\t' (tab-delimiting).
	Returns
	________
	data:list of Datum
		Returns a list of Datum objects, with each entry corresponding to an individual data file
	"""
	data = load_data(filename, folder, pattern, 'ca', filetype, delimiter)
	return data

def cp_raw(filename=None, folder=None, pattern='', filetype='', delimiter=dlm_default):
	"""
	Loads chronoamperometry data
	Efficient way to load multiple chornopotentiometry files at once; equivalent to calling load_data and specifying expt_type='cp'. If called with no arguments, loads all chronopotentiometry files in the present folder.
	Parameters
	___________
	filename: str, path object, or file-like (default=None)
		Full filename of a file in the present directory or a complete path to an individual file. If filename is specified, all other arguments except delimiter are ignored.
	folder: str, path object, or path-like (default=None)
		Directory in which data files are stored. If none, defaults to the present directory.
	pattern: str or regex
		If specified, only files matching this pattern in the specified folder are loaded. Ignored if filename is specified.
	filetype : str
		Any supported filetype. Only files of the specified file type will be loaded. Can be used in conjunction with pattern or expt_type.
	delimiter : char (default = '\t')
		Delimiting character if the file is a text file. Defaults to '\t' (tab-delimiting).
	Returns
	________
	data:list of Datum
		Returns a list of Datum objects, with each entry corresponding to an individual data file
	"""
	data = load_data(filename, folder, pattern, 'cp', filetype, delimiter)
	return data

def cv_raw(filename=None, folder=None, pattern='', filetype='', delimiter=dlm_default):
	"""
	Loads cyclic voltammetry data
	Efficient way to load multiple cyclic voltammetry files at once; equivalent to calling load_data and specifying expt_type='cv'. If called with no arguments, loads all cyclic voltammetry files in the present folder.
	Parameters
	___________
	filename: str, path object, or file-like (default=None)
		Full filename of a file in the present directory or a complete path to an individual file. If filename is specified, all other arguments except delimiter are ignored.
	folder: str, path object, or path-like (default=None)
		Directory in which data files are stored. If none, defaults to the present directory.
	pattern: str or regex
		If specified, only files matching this pattern in the specified folder are loaded. Ignored if filename is specified.
	filetype : str
		Any supported filetype. Only files of the specified file type will be loaded. Can be used in conjunction with pattern or expt_type.
	delimiter : char (default = '\t')
		Delimiting character if the file is a text file. Defaults to '\t' (tab-delimiting).
	Returns
	________
	data:list of Datum
		Returns a list of Datum objects, with each entry corresponding to an individual data file
	"""
	data = load_data(filename, folder, pattern, 'cv', filetype, delimiter)
	return data

def lsv_raw(filename=None, folder=None, pattern='', filetype='', delimiter=dlm_default):
	"""
	Loads linear sweep voltammetry data
	Efficient way to load multiple linear sweep voltammetry files at once; equivalent to calling load_data and specifying expt_type='lsv'. If called with no arguments, loads all linear sweep voltammetry files in the present folder.
	Parameters
	___________
	filename: str, path object, or file-like (default=None)
		Full filename of a file in the present directory or a complete path to an individual file. If filename is specified, all other arguments except delimiter are ignored.
	folder: str, path object, or path-like (default=None)
		Directory in which data files are stored. If none, defaults to the present directory.
	pattern: str or regex
		If specified, only files matching this pattern in the specified folder are loaded. Ignored if filename is specified.
	filetype : str
		Any supported filetype. Only files of the specified file type will be loaded. Can be used in conjunction with pattern or expt_type.
	delimiter : char (default = '\t')
		Delimiting character if the file is a text file. Defaults to '\t' (tab-delimiting).
	Returns
	________
	data:list of Datum
		Returns a list of Datum objects, with each entry corresponding to an individual data file
	"""
	data = load_data(filename, folder, pattern, 'lsv', filetype, delimiter)
	return data

def eis_raw(filename=None, folder=None, pattern='', filetype='', delimiter=dlm_default):
	"""
	Loads electrochemical impedance spectroscopy data
	Efficient way to load multiple electrochemical impedance spectroscopy files at once; equivalent to calling load_data and specifying expt_type='eis'. If called with no arguments, loads all electrochemical impedance spectroscopy files in the present folder.
	Parameters
	___________
	filename: str, path object, or file-like (default=None)
		Full filename of a file in the present directory or a complete path to an individual file. If filename is specified, all other arguments except delimiter are ignored.
	folder: str, path object, or path-like (default=None)
		Directory in which data files are stored. If none, defaults to the present directory.
	pattern: str or regex
		If specified, only files matching this pattern in the specified folder are loaded. Ignored if filename is specified.
	filetype : str
		Any supported filetype. Only files of the specified file type will be loaded. Can be used in conjunction with pattern or expt_type.
	delimiter : char (default = '\t')
		Delimiting character if the file is a text file. Defaults to '\t' (tab-delimiting).
	Returns
	________
	data:list of Datum
		Returns a list of Datum objects, with each entry corresponding to an individual data file
	"""
	data = load_data(filename, folder, pattern, 'eis', filetype, delimiter)
	return data

### high-level functions for processing data ###
def ca_process(data=None, current_column=2, potential_column=1, area=5, reference='she', thermo_potential=0, export_data=False, save_dir='processed', threshold=5, min_step_length=50, pts_to_average=300, pyramid=False, **kwargs):
	"""
	Processes chronoamperometry data
	Can either process pre-loaded data or load and process data files. If called with no arguments, loads and processes all 'ca' files in the present folder. See process_steps for details on the operations performed.
	Parameters
	___________
	data: list of Datum
		List of Datum objects containing CA data. If unspecified, data will be loaded using ca_raw before processing.
	current_column : int or str (default=1)
		Index or label of the column containing current data. Used only if automatic column identification fails
	potential_column : int or str (default=2)
		Index or label of the column containing potential data. Used only if automatic column identification fails
	threshold: int (default=5)
		Minimum consecutive absolute difference which constitutes a step
	min_step_length: int (default=25)
		Minimum length of the arrays which result from spliting the intial array. Arrays shorter than this value will be discarded
	pts_to_average: int (default=300)
		Steady-state average and sd are calculated using the last pts_to_average values of the array. Default is 300 points, which is the last 30 seconds of each hold at the instrument's default collection rate of 10 Hz.
	pyramid: bool (default=True)
		Specifies whether the current is ramped in both directions. Set pyramid=False if only ramping up or only ramping down.
	area: int or float (default=5)
		Geometric active area of the MEA. Scaling factor to convert current to current density.
	reference: {'she', 'sce'}, int, or float (default='she')
		Either a string identifying the reference electrode (ie 'she' or 'sce'), or the potential of the reference electrode used. sce=0.241
	**kwargs:
		Remaining arguments are passed to ca_raw to load data
	"""
	if data is None:
		data = ca_raw(**kwargs)
	for d in data:
		if d.get_expt_type() == 'ca':
			raw = d.get_raw_data()
			processed = process_steps(raw, potential_column, current_column, threshold, min_step_length, pts_to_average, pyramid, 'ca', area, reference, thermo_potential)
			d.set_processed_data(processed)
			d.set_current_data(processed['i'])
			d.set_potential_data(processed['v'])
			d.set_overpotential_data(processed['eta'])
			d.set_error_data(processed['i_sd'])
			set_datum_params(d, area, reference, thermo_potential)
			if export_data:
				name = d.get_name()
				utils.save_data(processed, name+'.csv', save_dir)
	return data

def cp_process(data=None, current_column=2, potential_column=1, area=5, reference='she', thermo_potential=0, export_data=False, save_dir='processed', threshold=5, min_step_length=25, pts_to_average=300, pyramid=True, **kwargs):
	"""
	Processes chronopotentiometry data
	Can either process pre-loaded data or load and process data files. If called with no arguments, loads and processes all 'cp' files in the present folder. See process_steps for details on the operations performed.
	Parameters
	___________
	data: list of Datum
		List of Datum objects containing CP data. If unspecified, data will be loaded using cp_raw before processing.
	current_column : int or str (default=1)
		Index or label of the column containing current data. Used only if automatic column identification fails
	potential_column : int or str (default=2)
		Index or label of the column containing potential data. Used only if automatic column identification fails
	threshold: int (default=5)
		Minimum consecutive absolute difference which constitutes a step
	min_step_length: int (default=25)
		Minimum length of the arrays which result from spliting the intial array. Arrays shorter than this value will be discarded
	pts_to_average: int (default=300)
		Steady-state average and sd are calculated using the last pts_to_average values of the array. Default is 300 points, which is the last 30 seconds of each hold at the instrument's default collection rate of 10 Hz.
	pyramid: bool (default=True)
		Specifies whether the current is ramped in both directions. Set pyramid=False if only ramping up or only ramping down.
	area: int or float (default=5)
		Geometric active area of the MEA. Scaling factor to convert current to current density.
	reference: {'she', 'sce'}, int, or float (default='she')
		Either a string identifying the reference electrode (ie 'she' or 'sce'), or the potential of the reference electrode used. sce=0.241
	**kwargs:
		Remaining arguments are passed to cp_raw to load data
	"""
	if data is None:
		data = cp_raw(**kwargs)
	for d in data:
		if d.get_expt_type() == 'cp':
			raw = d.get_raw_data()
			processed = process_steps(raw, current_column, potential_column, threshold, min_step_length, pts_to_average, pyramid, 'cp', area, reference, thermo_potential)
			d.set_processed_data(processed)
			d.set_current_data(processed['i'])
			d.set_potential_data(processed['v'])
			d.set_overpotential_data(processed['eta'])
			d.set_error_data(processed['v_sd'])
			set_datum_params(d, area, reference, thermo_potential)
			if export_data:
				name = d.get_name()
				utils.save_data(processed, name+'.csv', save_dir)
	return data

def cv_process(data=None, current_column=1, potential_column=0, area=5, reference='she', thermo_potential=0, export_data=False, save_dir='processed', **kwargs):
	"""
	Processes cyclic voltammetry data
	Can either process pre-loaded data or load and process data files. If called with no arguments, loads and processes all 'cv' files in the present folder. Peforms the following operations in order:
	1. Parse column labels to find columns containing current and potential data. If parsing fails, specified labels/indices are used
	2. Convert current to current density using the specified area
	Parameters
	__________
	data: list of Datum
		List of Datum objects containing CV data. If unspecified, data will be loaded using cv _raw before processing.
	area : int or float (default=5)
		Geometric active area of the MEA. Scaling factor to convert current to durrent density
	current_column : int or str (default=1)
		Index or label of the column containing current data. Used only if automatic column identification fails
	potential_column : int or str (default=0)
		Index or label of the column containing potential data. Used only if automatic column identification fails
	**kwargs:
		Remaining arguments are passed to cv_raw to load data
	"""
	if data is None:
		data = cv_raw(**kwargs)
	for d in data:
		if d.get_expt_type() == 'cv':
			raw = d.get_raw_data()
			current = find_col(raw, 'current', current_column)
			current = current / area
			potential = find_col(raw, 'potential', potential_column)
			potential = electrode_correct(potential, reference)
			overpotential = overpotential_correct(potential, thermo_potential)
			processed = pd.DataFrame({'i':current, 'v':potential, 'eta':overpotential})
			d.set_processed_data(processed)
			d.set_current_data(current)
			d.set_potential_data(potential)
			d.set_overpotential_data(overpotential)
			set_datum_params(d, area, reference, thermo_potential)
			if export_data:
				name = d.get_name()
				utils.save_data(processed, name+'.csv', save_dir)
	return data

def lsv_process(data=None, potential_column=0, current_column=1, area=5, reference='she', thermo_potential=0, export_data=False, save_dir='processed', **kwargs):
	"""
	Processes linear sweep voltammetry data
	Can either process pre-loaded data or load and process data files. If called with no arguments, loads and processes all 'lsv' files in the present folder. Peforms the following operations in order:
	Parameters
	__________
	data: list of Datum
		List of Datum objects containing LSV data. If unspecified, data will be loaded using lsv_raw before processing.
	area : int or float (default=5)
		Geometric active area of the MEA. Scaling factor to convert current to durrent density
	current_column : int or str (default=1)
		Index or label of the column containing current data. Used only if automatic column identification fails
	potential_column : int or str (default=0)
		Index or label of the column containing potential data. Used only if automatic column identification fails
	**kwargs:
		Remaining arguments are passed to cv_raw to load data
	"""
	area = area / 10000 #cm2 to m2
	if data is None:
		data = lsv_raw(**kwargs)
	for d in data:
		if d.get_expt_type() == 'lsv':
			raw = d.get_raw_data()
			potential = find_col(raw, 'potential', potential_column)
			potential = electrode_correct(potential, reference)
			overpotential = overpotential_correct(potential, thermo_potential)
			current = find_col(raw, 'current', current_column)
			current = current / area
			log_current = current - min(current) + 0.000001
			log_current = np.log10(log_current)
			processed = pd.DataFrame({'v':potential, 'i':current, 'eta':overpotential, 'log(ioi)':log_current})
			d.set_processed_data(processed)
			d.set_potential_data(potential)
			d.set_overpotential_data(potential)
			d.set_current_data(current)
			d.set_logcurrent_data(log_current)
			set_datum_params(d, area, reference, thermo_potential)
			if export_data:
				name = d.get_name()
				utils.save_data(processed, name+'.csv', save_dir)
	return data

def drop_neg_and_split_zeros(real, imag,freq):
	Z, f =[] , []
	for x in range (len(real)):
		if (float(imag[x]) != 0) & (float(imag[x])<0):
			Z.append(complex(float(real[x]), float(imag[x])))
			f.append(float(freq[x]))
	return np.asarray(f), np.asarray(Z)

def ignoreBelowX(real, imag):
	real_new , imag_new = [] , []
	for x in range (len(real)):
		if (float(imag[x]) != 0) & (float(imag[x])<0):
			real_new.append(float(real[x]))
			imag_new.append(float(imag[x]))
	return np.asarray(real_new), np.asarray(imag_new)

def HFR_LIN2P(time, real, imag,f,maxfreq):
	real = np.asarray(real) #Convert the input to an array
	imag = np.asarray(imag)
	rer, imm = [], []
	y=0 
	for i in range(len(real)):
		if float(f[i]) > 200: #keep only data with frequency more than 200Hz (high frequency)
			rer.append(float(real[i])) 
			imm.append(float(imag[i]))
	im = np.abs(imm) # Calculate the absolute value element-wise
	sort_index = np.argsort(im) # Returns the indices that would sort an array
	y = time[sort_index[0]]
	re_hfr, im_hfr = [], []
	for i in range (0,2): # i in (0,1)
		re_hfr.append(real[sort_index[i]])
		im_hfr.append(imag[sort_index[i]])
	hfrf = interpolate.interp1d(re_hfr,im_hfr,fill_value="extrapolate") #Build the hfrf function 1D interpolation
	x = float(optimize.fsolve(hfrf, 0.0)) #Return the roots of the (non-linear) equations defined by hfrf(x) = 0 
	return x, y 

def HFR_LIN_KK(Z_linKK):
	xx = np.real(Z_linKK)
	yy = np.imag(Z_linKK)
	hfrf = interpolate.interp1d(xx,yy ,fill_value="extrapolate")
	ff =[]
	ff.append(float(optimize.fsolve(hfrf,0.0)))
	x = float(optimize.fsolve(hfrf,0.0))
	return x

def frequency_HFR(re, im, f, hfr):
	real = np.asarray(re)
	imag = np.asarray(im)
	freq = np.asarray(f)
	hfr = float(hfr)
	rer = real[(imag < 0) & (real > 0)]
	imm = imag[(imag < 0) & (real > 0)]
	ff = freq[(imag < 0) & (real > 0)]
	Z =[]
	for x in range (len(rer)):
		Z.append(complex(float(rer[x]), float(imm[x])))	
	f_hfr_func = interpolate.interp1d(np.abs(Z),ff,fill_value="extrapolate")
	f_hfr = f_hfr_func(hfr)
	return f_hfr



def split_at_XM (timevals, voltvals, curvals,freqvals,realvals, imagvals, maxfreq):
	this_time, this_real, this_imag, this_freq, this_volt, this_cur = [],[], [], [], [], []
	final_time, final_real, final_imag, final_freq, final_volt, final_cur =[],[], [], [], [], []
	size = len(freqvals)
	idx_list = [idx for idx, val in enumerate(freqvals) if val == maxfreq]
	this_time = [timevals[i: j] for i, j in zip([0] + idx_list, idx_list + ([size] if idx_list[0] != size else []))]
	this_freq = [freqvals[i: j] for i, j in zip([0] + idx_list, idx_list + ([size] if idx_list[0] != size else []))]
	this_real = [realvals[i: j] for i, j in zip([0] + idx_list, idx_list + ([size] if idx_list[0] != size else []))]
	this_imag = [imagvals[i: j] for i, j in zip([0] + idx_list, idx_list + ([size] if idx_list[0] != size else []))]
	this_volt = [voltvals[i: j] for i, j in zip([0] + idx_list, idx_list + ([size] if idx_list[0] != size else []))]
	this_cur = [curvals[i: j] for i, j in zip([0] + idx_list, idx_list + ([size] if idx_list[0] != size else []))]
	for i in range(len(idx_list)+1):
		if len(this_freq[i]) != 0:
			final_time.append(this_time[i])
			final_freq.append(this_freq[i])
			final_real.append(this_real[i])
			final_imag.append(this_imag[i])
			final_volt.append(this_volt[i])
			final_cur.append(this_cur[i])

	return  final_time, final_volt, final_cur , final_freq, final_real, final_imag

def eis_process(data=None,time_column= 1, voltage_column = 2, current_column =3, freq_column=4, real_column=5, imag_column=6, area=22.68, maxfreq = 100000,voltage_factor = 1, current_factor =1, negative_imaginary = 1, min_step_length=5, export_data=False, save_dir='processed', **kwargs):
	"""
	Processes electrochemical impedance spectroscopy data
	Can either process pre-loaded data or load and process data files. If called with no arguments, loads and processes all 'eis' files in the present folder. Peforms the following operations in order:
	Parameters
	__________
	data: list of Datum
		List of Datum objects containing EIS data. If unspecified, data will be loaded using eis_raw before processing.
	area : int or float (default=5)
		Geometric active area of the MEA. Scaling factor to convert current to durrent density
	current_column : int or str (default=1)
		Index or label of the column containing current data. Used only if automatic column identification fails
	potential_column : int or str (default=0)
		Index or label of the column containing potential data. Used only if automatic column identification fails
	**kwargs:
		Remaining arguments are passed to cv_raw to load data
	"""
	if data is None:
		data = eis_raw(**kwargs)
	new_data = []
	for d in data:
		if d.get_expt_type() == 'eis':
			basename = d.get_name()
			raw = d.get_raw_data()
			### TODO: add support for GEIS and PEIS specifically, as well as frequency analysis ###
			freq_all = np.asarray(raw.iloc[:,freq_column])
			v_all = np.asarray(raw.iloc[:,voltage_column])
			i_all = np.asarray(raw.iloc[:,current_column])
			real_all = np.asarray(raw.iloc[:,real_column])
			imag_all = np.asarray(raw.iloc[:,imag_column])
			time_all = np.asarray(raw.iloc[:,time_column])
			imag_all = imag_all * negative_imaginary
			v_all = v_all * voltage_factor
			i_all = i_all * current_factor
			t_splits, v_splits, i_splits, freq_splits, re_splits, im_splits = split_at_XM(time_all, v_all, i_all ,freq_all,real_all, imag_all, maxfreq)
			i = 0
			hfrlinkk_total,hfr2_total,hfr_area_total =[],[],[]
			f_HFR =[]
			curr_dens = []
			hfr_time =[]
			curr_density = []
			volt_mean, current_mean = [], []
			for  t, f, re, im, volt,cur in zip(t_splits, freq_splits, re_splits, im_splits, v_splits, i_splits):
				re = np.asarray(re)
				im = np.asarray(im)
				f = np.asarray(f)
				t=np.asarray(t)
				
				# print('test time',np.asarray(hfr_time))
				# print('test time1',len(np.asarray(hfr_time)))
				volt, cur = np.asarray(volt), np.asarray(cur)
				df = pd.DataFrame({'U in V': volt, 'I  in A': cur, 'f in Hz':f, 'Re(Z) in \u03A9':re, 'Im(Z) in \u03A9':im })
				this_data = Datum(basename + f'_{i:02d}', df)
				this_data.set_processed_data(df)
				volt, cur = np.asarray(volt), np.asarray(cur)
				current_mean.append(np.mean(cur))
				volt_mean.append(np.mean(volt))
				# print('test v',np.asarray(volt_mean))#col2
				# print('test vv',len(np.asarray(volt_mean)))
				this_data.set_current_data(current_mean)
				this_data.set_potential_data(volt_mean)
				# # ''' HFR ANALYSIS'''
				# # 2 Points fit HFR
				hfr2, time_hfr1  = HFR_LIN2P(t, re, im,f,maxfreq)
				# print("test11 ", time_hfr1)
				hfr_time.append(time_hfr1)#colone
				hfr2_total.append(np.asarray(hfr2))
				# print('test hfr2',np.asarray(hfr2_total))#col2
				# print('test hfr22',len(np.asarray(hfr2_total)))
				this_data.set_hfr_twopts(hfr2)
				#HFR * Area in [m Ohm . cm²]
				HFR_Area = hfr2 * area * 1000
				hfr_area_total.append(HFR_Area)
				# print('test area',np.asarray(hfr_area_total))#col2
				# print('test area1',len(np.asarray(hfr_area_total)))
				this_data.set_hfr_area(HFR_Area)
				# # #linearfit HFR
				rex, imx = ignoreBelowX(re, im)
				# # '''LIN_KK VAlidation'''
				ff , ZZ = drop_neg_and_split_zeros(rex, imx, f)
				M, mu, Z_linKK, res_real, res_imag = linKK(ff, ZZ, c=.5, max_M=100, fit_type='complex', add_cap=True)
				rms = rmse(ZZ,Z_linKK)
				df_save_linkk_data = pd.DataFrame([[M,mu,rms]], columns=['M', 'mu', 'RMSE'])
				processed_linkk = pd.DataFrame({'Frequency in Hz': ff, 'Z in Ohm': ZZ, 'Z_linkk in Ohm': Z_linKK, 'Residuals of Re(Z_linkk) in %':res_real, 'Residuals of Im(Z_linkk) in %': res_imag})
				df_save_linkk_data_result = pd.concat([processed_linkk, df_save_linkk_data], axis=1)
				this_data.set_processed_data_linkk(processed_linkk)
				# # #LIN_KK fit HFR
				hfrlinkk = HFR_LIN_KK(Z_linKK)
				hfr_frequency = frequency_HFR(re,im,f,hfrlinkk)
				cvcvc = np.asarray(hfr_frequency)
				f_HFR.append(cvcvc)
				# print('test fhfr',f_HFR)#col5
				# print('test fhfr2',len(f_HFR))
				this_data.set_frequency_hfr(hfr_frequency)
				this_data.set_frequency_hfr_frequency(f_HFR)
				#current_density vs hfr
				hfrlinkk_total.append(hfrlinkk)
				# print('test hfrlinkk',hfrlinkk_total)#col4
				# print('test hfrlinkk1',len(hfrlinkk_total))
				curr_dens = np.asarray(cur)/area
				curr_density.append(np.mean(curr_dens))
				# print('test dichte',curr_density)#col3
				# print('test dichte1',len(curr_density))
				this_data.set_curr_density(curr_density)
				this_data.set_hfrlinkk_total(hfrlinkk_total)
				this_data.set_hfr_linkk(hfrlinkk)
				this_data.set_randle(M)
				this_data.set_mu(mu)
				this_data.set_rmse(rms)
				df_save_HFR_Analysis_data = pd.DataFrame([[hfr2,hfrlinkk,hfr_frequency,HFR_Area]], columns=['HFR in Ohm (2 points fit)', 'HFR in Ohm (LINKK fit)', 'HFR Frequency in Hz', 'HFR * Area in m.Ohm*cm*cm'])
				this_data.set_expt_type('eis')
				new_data.append(this_data)
				if export_data:
					name = this_data.get_name()
					directory0 = 'EIS Data'
					directory = 'HFR Analysis'
					directory1 = 'Analysis Results'
					path0 = os.path.join(save_dir, directory0)
					path1 = os.path.join(save_dir, directory)
					path2 = os.path.join(save_dir, directory1)
					try: 
						os.mkdir(path0) 
						os.mkdir(path1) 
						os.mkdir(path2)
					except OSError as error: 
						print(error)  

					directory2 = 'LINKK'
					directory3 = 'HFR Analysis'
					path3 = os.path.join(path2, directory2)	
					path4 = os.path.join(path2, directory3)
					try: 
						os.mkdir(path3)
						os.mkdir(path4) 
					except OSError as error: 
						print(error) 

					fig, ax = plt.subplots()
					visuals.plot_hfr(data=this_data, ax= ax)
					savepath = path1+'//'+'Nyquist_Plot_'+ name+'.png'
					fig.savefig(savepath)
					utils.save_data(df_save_linkk_data_result,'Linkk_results_' + name + '.csv',path3)
					utils.save_data(df_save_HFR_Analysis_data,'HFR_Analysis_results_' + name + '.csv',path4)
					utils.save_data(df, name+'.csv', path0)
				i += 1
		if export_data:
			directory5 = 'Measurement per polarization curve'
			path5 = os.path.join(save_dir, directory5)
			try: 
				os.mkdir(path5) 
			except OSError as error: 
				print(error) 
			df_save_hfr_result = pd.DataFrame({'Time in s': hfr_time, 'current density': curr_density , ' Voltage in V':volt_mean, 'HFR (2pts)': hfr2_total, 'HFR (linkk)': hfrlinkk_total, 'HFR Frequency': f_HFR, 'HFR Area': hfr_area_total})
			
			utils.save_data(df_save_hfr_result,'HFR for all measurements' + '.csv',path5)
			

		return new_data

def return_Z(real, imag,freq):
	Z, f =[] , []
	for x in range (len(real)):
		# if (float(imag[x]) != 0) & (float(imag[x])<0):
		Z.append(complex(float(real[x]), float(imag[x])))
		f.append(float(freq[x]))
	return np.asarray(f), np.asarray(Z)




### cp/ca analysis ###
def process_steps(data, control_column=0, response_column=1, threshold=5, min_step_length=25, pts_to_average=300, pyramid=True, expt_type='cp', area=1, reference='she', thermo_potential=0):
	"""
	Processes stepwise data (ex chronopotentiometry and chronoamperometry data)
	Performs the following operations in order:
	1. Parse column labels to find the columns containing the desired data. If automatic parsing fails, the specified column labels/indices are used.
	2. Find the points at which the independent variable steps up or down using the specified threshold value.
	3. Split the data  at these split points. Holds with fewer than the minimum number of points are filtered out to account for outliers. Note: splitting is based upon values of the independent variable, so this will not result in the loss of meaningful data.
	4. Average and standard deviation are calculated using the last several points of each step to obtain steady-state values.
	5. If the indpendent variable is ramped up and down, the steady-state average and standard deviation are calculated across both the ramp-up and ramp-down holds.
	6. Any necessary scaling or transformations are performed (ex. reference electrode correction, coversion to current density, etc.)
	Parameters
	___________
	data: DataFrame
		Dataframe containing the data to be processed
	control_column: int or str (default=0)
		Label or index of the column containing the control/independent variable values
	response_column: int or str (default=1)
		Label or index of the column cotaining the response/dependent variabble values
	threshold: int (default=5)
		Minimum consecutive absolute difference which constitutes a step
	min_step_length: int (default=25)
		Minimum length of the arrays which result from spliting the intial array. Arrays shorter than this value will be discarded
	pts_to_average: int (default=300)
		Steady-state average and sd are calculated using the last pts_to_average values of the array. Default is 300 points, which is the last 30 seconds of each hold at the instrument's default collection rate of 10 Hz.
	pyramid: bool (default=True)
		Specifies whether the current is ramped in both directions. Set pyramid=False if only ramping up or only ramping down.
	expt_type: {'cp', 'ca'} (default='cp')
		Specifies the type of experiment being analyzed. This is used to determine which variables are the control and response variables.
	area: int or float (default=5)
		Geometric active area of the MEA. Scaling factor to convert current to current density.
	reference: {'she', 'sce'}, int, or float (default='she')
		Either a string identifying the reference electrode (ie 'she' or 'sce'), or the potential of the reference electrode used. sce=0.241
	"""
	if expt_type == 'ca':
		control_var = 'potential'
		response_var = 'current'
	elif expt_type == 'cp':
		control_var = 'current'
		response_var = 'potential'
	control = np.asarray(find_col(data, control_var, control_column))
	response = np.asarray(find_col(data, response_var, response_column))
	split_pts = find_steps(control, threshold=threshold)
	control_steps = split_and_filter(control, split_pts, min_length=min_step_length)
	response_steps = split_and_filter(response, split_pts, min_length=min_step_length)
	control_avg = array_apply(control_steps, avg_last_pts, numpts=pts_to_average)
	response_avg = array_apply(response_steps, avg_last_pts, numpts=pts_to_average)
	control_std = array_apply(control_steps, std_last_pts, numpts=pts_to_average)
	response_std = array_apply(response_steps, std_last_pts, numpts=pts_to_average)
	# if expt_type == 'ca':
	# 	split_pts = find_steps(potential, threshold=threshold)
	# elif expt_type == 'cp':
	# 	split_pts = find_steps(current, threshold=threshold)
	# current_steps = split_and_filter(current, split_pts, min_length=min_step_length)
	# potential_steps = split_and_filter(potential, split_pts, min_length=min_step_length)
	# current_avg = array_apply(current_steps, avg_last_pts, numpts=pts_to_average)
	# potential_avg = array_apply(potential_steps, avg_last_pts, numpts=pts_to_average)
	# current_std = array_apply(current_steps, std_last_pts, numpts=pts_to_average)
	# potential_std = array_apply(potential_steps, std_last_pts, numpts=pts_to_average)
	if pyramid:
		sort_idx = np.argsort(control_avg)
		control_avg = control_avg[sort_idx]
		response_avg = response_avg[sort_idx]
		control_std = control_std[sort_idx]
		response_std = response_std[sort_idx]
		split_pts = find_steps(control_avg, threshold=2)
		# if expt_type == 'ca':
		# 	split_pts = find_steps(potential_avg, threshold=2)
		# elif expt_type == 'cp':
		# 	split_pts = find_steps(current_avg, threshold=2)
		control_steps = split_and_filter(control_avg, split_pts)
		response_steps = split_and_filter(response_avg, split_pts)
		control_std_steps = split_and_filter(control_std, split_pts)
		response_std_steps = split_and_filter(response_std, split_pts)
		control_avg = array_apply(control_steps, np.mean)
		response_avg = array_apply(response_steps, np.mean)
		control_std = array_apply(control_std_steps, std_agg)
		response_std = array_apply(response_std_steps, std_agg)
	# current_avg = current_avg / area
	# current_std = current_std / area
	if expt_type == 'ca':
		# if reference:
		control_avg = electrode_correct(control_avg, reference)
		overpotential = overpotential_correct(control_avg, thermo_potential)
		response_avg = response_avg / area
		response_std = response_std / np.sqrt(area)
		processed = pd.DataFrame({'i':response_avg, 'v':control_avg, 'i_sd':response_std, 'v_sd':control_std, 'eta':overpotential})
	elif expt_type == 'cp':
		# if reference:
		response_avg = electrode_correct(response_avg, reference)
		overpotential = overpotential_correct(response_avg, thermo_potential)
		control_avg = control_avg / area
		control_std = control_std / np.sqrt(area)
		processed = pd.DataFrame({'i':control_avg, 'v':response_avg, 'i_sd':control_std, 'v_sd':response_std, 'eta':overpotential})
	return processed

### tafel analysis ###
def tafel_slope(log_curr, eta, min_curr=None, max_curr=None):
	min_idx = 0
	max_idx = len(log_curr)
	if min_curr and min_curr >= min(log_curr):
		min_idx = np.where(log_curr <= min_curr)[0][-1]
	if max_curr and max_curr <= max(log_curr):
		max_idx = np.where(log_curr >= max_curr)[0][0]
	log_curr_trim = log_curr[min_idx:max_idx+1]
	eta_trim = eta[min_idx:max_idx+1]
	a, b, r, p, err = stats.linregress(log_curr_trim, eta_trim)
	rsquare = r**2
	exchg_curr = 10 ** (b / -a)
	return a, exchg_curr, rsquare, log_curr_trim, eta_trim

def tafel_eqn(log_curr, exchg_curr, slope):
	eta = slope * (log_curr - np.log10(exchg_curr))
	return eta

### hfr analysis ###
def fit_eis_semicircle(real, imag):
	try:
		rguess = max(imag) / 2
		hguess = np.mean(real)
		# popt, pcov = curve_fit(semicircle, real,-1*imag, maxfev=50000)
		popt, pcov = curve_fit(semicircle, real,imag, maxfev=50000)
		r = popt[0]
		h = popt[1]
	except RuntimeError as e:
		return (0,0,0), 0, 0
	# hfr = -1*np.sqrt(r**2 - k**2) + h
	hfr=h-r
	lfr = 0
	return popt, hfr, lfr

def fit_eis_linear(real, imag):
	slopes = []
	first_real, first_imag = real[0], imag[0]
	for x, y in zip(real[1:], imag[1:]):
		this_slope = np.abs((y-first_imag) / (x-first_real))
		slopes.append(this_slope)
	slopes = np.asarray(slopes)
	idx = np.where(slopes == max(slopes))[0][0]
	real_trim, imag_trim = real[:idx], imag[:idx]
	try:
		m, b, _, _, _ = stats.linregress(real_trim, imag_trim)
		popt = (m,b)
		hfr = -b / m
	except ValueError as e:
		return (0,0), 0
	return popt, hfr

def semicircle(x, r, h, k):
	x = np.asarray(x)
	y = np.sqrt((r**2 - (x-h)**2)) + k
	return y

### misc auxilliary functions ###
def electrode_correct(arr, ref='she'):
	"""
	Corrects for the reference electrode
	Parameters
	___________
	arr: list or numpy array
		Array of potential values to which the correction will be applied
	ref: {'she', 'sce'}, int, or float (default='she')
		Either a string identifying the reference electrode (ie 'she' or 'sce'), or the potential of the reference electrode used. sce=0.241
	"""
	if type(arr) == list:
		arr = np.asarray(arr)
	corrected = arr
	if utils.check_str(ref):
		ref = ref.lower()
		try:
			corrected = corrected + ref_electrodes[ref]
		except KeyError:
			pass
	elif utils.check_float(ref) or utils.check_int(ref):
		corrected = corrected + ref
	return corrected

def overpotential_correct(arr, rxn=0):
	"""
	Calculate overpotential
	Calculates overpotential for given potential data using the specified thermodynamic potential.
	Parameters
	___________
	arr: list or numpy array
		Array of potential values to which the correction will be applied
	ref: {'she', 'sce'}, int, or float (default='she')
		Either a string identifying the reference electrode (ie 'she' or 'sce'), or the potential of the reference electrode used. sce=0.241
	"""
	if type(arr) == list:
		arr = np.asarray(arr)
	corrected = arr
	if utils.check_str(rxn):
		rxn = rxn.lower()
		try:
			corrected = corrected - thermo_potentials[rxn]
		except KeyError:
			pass
	elif utils.check_float(rxn) or utils.check_int(rxn):
		corrected = corrected - rxn
	return corrected

def find_col(data, col_type, label=None):
	"""
	Finds column containing the desired measurement
	Parameters
	___________
	data: DataFrame
		DataFrame containing the full data set
	col_type: one of {'current', 'potential', 'time', 'current_err', 'potential_err', 'overpotential', 'tafelcurrent', 'realcurr', 'imagcurr'}
		Type of data being searched for
	label: str or int (default=None)
		Label or index of the desired column if the column label cannot be automatically parsed
	Returns
	________
	col: numpy array
		Array of the desired measurement values
	"""
	default_label = col_default_labels[col_type]
	default_id = col_default_ids[col_type]
	newdf = data.copy()
	newdf.columns = utils.check_labels(newdf)
	if default_label in newdf.columns:
		col = newdf[default_label]
	elif label:
		if utils.check_str(label):
			col = newdf[label]
		else:
			col = newdf.iloc[:,label]
	else:
		col = newdf.iloc[:, default_id]
	col = np.asarray(col)
	return col

### auxilliary array manipulation functions ###
def set_datum_params(data, area, ref, rxn):
	data.set_area(area)
	if ref in ref_electrodes.keys():
		ref = ref_electrodes[ref]
	data.set_refelec(ref)
	if rxn in thermo_potentials.keys():
		rxn = thermo_potentials[rxn]
	data.set_thermo_potential(rxn)

def split_at_zeros(xvals, yvals):
	final_x, final_y = [], []
	this_x, this_y = [], []
	for x, y in zip(xvals, yvals):
		if x!=0 or y!=0:
			this_x.append(x)
			this_y.append(y)
		else:
			if len(this_x) != 0:
				final_x.append(this_x)
				final_y.append(this_y)
			this_x = []
			this_y = []
	if len(this_x) != 0:
		final_x.append(this_x)
		final_y.append(this_y)
	return final_x, final_y

def drop_neg(xvals, yvals):
	"""
	Appli
	"""
	final_x, final_y = [],[]
	this_x, this_y = [],[]
	for x, y in zip(xvals, yvals):
		this_x = [i for i,j in zip(x,y) if i>=0 and j>=0]
		this_y = [j for i,j in zip(x,y) if i>=0 and j>=0]
		if len(this_x) != 0:
			final_x.append(this_x)
			final_y.append(this_y)
	return final_x, final_y

def array_apply(arr, func, **kwargs):
	"""
	Applies a function to each value in an array
	Parameters
	___________
	arr: array-like
		Array to which function will be applied
	func: function
		function to apply to each value
	**kwargs:
		Any other arguments required by the specified function
	Returns
	________
	result: numpy array
		Array of the transformed values
	"""
	result =  np.asarray([func(a, **kwargs) for a in arr])
	return result

def avg_last_pts(arr, numpts=300):
	"""
	Average of the last several values of an array
	Auxilliary function to compute the average of an array accross the last several data points. Useful for obtaining a steady-state average.
	Parameters
	___________
	arr: list or numpy array
		Array of values used to compute the average.
	numpts: int (default=300)
		Average is calculated using the last numpts values of the array.
	Returns
	________
	avg: float
		Average of the last several values
	"""
	if type(arr) == list:
		arr = np.asarray(arr)
	avg = np.mean(arr[-numpts:])
	return avg

def std_last_pts(arr, numpts=300):
	"""
	Standard deviation of the last several values of an array
	Auxilliary function to compute the standard deviation of an array accross the last several data points. Useful for obtaining a steady-state standard deviation.
	Parameters
	___________
	arr: list or numpy array
		Array of values used to compute the standard deviation.
	numpts: int (default=300)
		Standard deviation is calculated using the last numpts values of the array.
	Returns
	________
	sd: float
		Standard deviation of the last several values
	"""
	if type(arr) == list:
		arr = np.asarray(arr)
	sd = np.std(arr[-numpts:], ddof=1)
	return sd

def std_agg(arr):
	"""
	Aggregate standard deviations of multiple measurements.
	Auxilliary function to calculate the aggregate standard deviation of multiple measuremtns. Assumes that the measurements are independent of each other
	Parameters
	___________
	arr: list or numpy array
		Array of standard deviations to be aggregated
	Returns
	________
	sd: float
		Aggregated standard deviation
	"""
	if type(arr) == list:
		arr = np.asarray(arr)
	sd = np.sqrt(np.sum(arr**2))
	return sd

def split_and_filter(arr, split_pts, min_length=0):
	"""
	Split continuous array at the specified points.
	Auxilliary function to split continuous current or voltage data into individual holds. Splits the array at the specified indices and discards resulting arrays which are shorter than the required minimum length.
	Parameters
	___________
	arr: list or numpy array
		Array to split
	split_pts: int or array-like
		Indices at which to split the array
	min_length: int (default=0)
		Minimum length of the arrays which result from spliting the intial array. Arrays shorter than this value will be discarded

	Returns
	________
	steps: numpy array
		Array containing one array for each hold/step
	"""
	if type(arr) == list:
		arr = np.asarray(arr)
	steps = np.split(arr, split_pts)
	steps = np.asarray([s for s in steps if len(s) > min_length])
	return steps

def find_steps(arr, threshold=5):
	"""
	Find indices at which an array of roughly stepwise data changes values
	Auxilliary function to find the points at which curren/voltage is stepped up or down during and experiment. Identifies 'steps' by determining the points at which the consecutive absolute difference between array values is greater than a specified threshold.
	Parameters
	___________
	arr: list or numpy array
		Array of roughly stepwise data
	threshold: int or float  (default=5)
		Minimum consecutive absolute difference which constitutes a step
	Returns
	________
	splits: numpy array
		Indices at which the array steps up or down
	"""
	if type(arr) == list:
		arr = np.asarray(arr)
	diffs = np.abs(np.diff(arr))
	splits = np.where(diffs > threshold)[0] + 1
	return splits