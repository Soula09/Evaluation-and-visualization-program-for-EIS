# # def split_at_XM (voltvals, curvals,freqvals,realvals, imagvals):
# #     print('Hallo')
# #     this_real, this_imag, this_freq, this_volt, this_cur = [], [], [], [], []
# #     final_real, final_imag, final_freq, final_volt, final_cur = [], [], [], [], []
# #     size = len(freqvals)
# #     print(size)
# #     idx_list = [idx for idx, val in enumerate(freqvals) if val == 100000]
# #     this_freq = [freqvals[i: j] for i, j in zip([0] + idx_list, idx_list + ([size] if idx_list[0] != size else []))]
# #     this_real = [realvals[i: j] for i, j in zip([0] + idx_list, idx_list + ([size] if idx_list[0] != size else []))]
# #     this_imag = [imagvals[i: j] for i, j in zip([0] + idx_list, idx_list + ([size] if idx_list[0] != size else []))]
# #     this_volt = [voltvals[i: j] for i, j in zip([0] + idx_list, idx_list + ([size] if idx_list[0] != size else []))]
# #     this_cur = [curvals[i: j] for i, j in zip([0] + idx_list, idx_list + ([size] if idx_list[0] != size else []))]
# #     for i in range(len(idx_list)+1):
# #         if len(this_freq[i]) != 0:
# #             final_freq.append(this_freq[i])
# #             final_real.append(this_real[i])
# #             final_imag.append(this_imag[i])
# #             final_volt.append(this_volt[i])
# #             final_cur.append(this_cur[i])

# #     return  final_volt, final_cur , final_freq, final_real, final_imag


# # df = pd.DataFrame({'U (V)': volt, 'I (A)': cur, 'f (Hz)':f, "Z' (\u03A9)":re, "Z'' (\u03A9)":im })

# #     # mea area widgets
# #         self.area_lbl = QLabel(f'MEA area [cm<sup>2</sup>]')
# #         self.area_txtbx = QLineEdit('22.68')
# #         #Maximal frequency
# #         self.maxfreq_lbl = QLabel('Maximum frequency (Hz)')
# #         self.maxfreq_txtbx = QLineEdit('100000')

# #          # def maxfreq_action(self):
# #     #     maxfeq = self.maxfreq_txtbx.text()
# #     #     try:
# #     #         maxfeq = float(maxfeq)
# #     #         self.datahandler.set_maxfreq(maxfeq)
# #     #     except ValueError as e:
# #     #         self.update_status('Maximal frequency must be a number')

# # import numpy
# # s = numpy.array([6, -1, 8, -10, 5])
# # ss = numpy.abs(s)
# # sort_index = numpy.argsort(ss)
# # kk =[]
# # # kk.append(s[sort_index[0]])
# # # kk.append(s[sort_index[1]])
# # for i in range (0,2):
# #     kk.append(s[sort_index[i]])
# # print(kk)

# # importing os module
# # import os
  
# # # Directory
# # directory = "GeeksforGeeks3"
  
# # # Parent Directory path
# # parent_dir = "C:/Users/ousssoul/OneDrive - Magna/24_03_2022/Tests Plot"
  
# # # Path
# # path = os.path.join(parent_dir, directory)
# # print(path)
# # # Create the directory
# # # 'GeeksForGeeks' in
# # # '/home / User / Documents'
# # os.mkdir(path)
# # print("Directory '% s' created" % directory)
  
# # # Directory
# # directory = "Geeks3"
  
# # # Parent Directory path
# # parent_dir = "C:/Users/ousssoul/OneDrive - Magna/24_03_2022/Tests Plot"
  
# # # mode
# # mode = 0o666
  
# # # Path
# # path = os.path.join(parent_dir, directory)
  
# # # Create the directory
# # # 'GeeksForGeeks' in
# # # '/home / User / Documents'
# # # with mode 0o666
# # os.mkdir(path, mode)
# # print("Directory '% s' created" % directory)
# import ctypes

# import numpy as np 

# # x = [1,2,32,3,654,5,8,8,0,234564]
# # x = np.asarray(x)
# # y = max(x)
# # z = min(x)
# # print(y)
# # print(z)
# y = 2
# x = 2**y
# print('pow(x,2)')
# # xcx
# # df_save_HFR_Analysis = pd.DataFrame({'HFR (2 points fit)': hfr2, 'HFR (LINKK fit)': hfrlinkk, 'HFR frequency': xcx})
# # 				print('HFR LINKK : ',hfrlinkk)
# # 				df_save_LINKK_Validation = pd.DataFrame({'Frequency': ff, 'Z': ZZ, 'Z_LINKK': Z_linKK, 'Resisuals of Re(Z)':res_real, 'Resisuals of Im(Z)': res_imag, 'M (number of randles)' : M, 'mu': mu , 'RMSE': rms})
# # 				if export_data:
# # 					name = this_data.get_name()
# # 					directory = 'HFR Analysis'
# # 					directory1 = 'Analysis Results'
# # 					path1 = os.path.join(save_dir, directory)
# # 					path2 = os.path.join(save_dir, directory1)
# # 					try: 
# # 						os.mkdir(path1) 
# # 						os.mkdir(path2)
# # 					except OSError as error: 
# # 						print(error)  
# # 					fig, ax = plt.subplots()
# # 					visuals.plot_hfr(data=this_data, ax= ax)
# # 					savepath_HFR = path1+'//'+'Nyquist_Plot_'+ name+'.png'
# # 					fig.savefig(savepath_HFR)
# # 					utils.save_data(df_save_HFR_Analysis, name+'.csv', save_dir)
# # 					utils.save_data(df, name+'.csv', savepath_HFR)#_HFR_Analysis_result

# def get_fitted_data(self, frequencies, impedance, bounds=None,
#             weight_by_modulus=False, **kwargs):

#         if not isinstance(frequencies, np.ndarray):
#             raise TypeError('frequencies is not of type np.ndarray')
#         if not (np.issubdtype(frequencies.dtype, np.integer) or
#                 np.issubdtype(frequencies.dtype, np.floating)):
#             raise TypeError('frequencies array should have a numeric ' +
#                             f'dtype (currently {frequencies.dtype})')
#         if not isinstance(impedance, np.ndarray):
#             raise TypeError('impedance is not of type np.ndarray')
#         if impedance.dtype != np.complex:
#             raise TypeError('impedance array should have a complex ' +
#                             f'dtype (currently {impedance.dtype})')
#         if len(frequencies) != len(impedance):
#             raise TypeError('length of frequencies and impedance do not match')

#         if self.initial_guess != []:
#             parameters, conf = circuit_fit(frequencies, impedance,
#                                            self.circuit, self.initial_guess,
#                                            constants=self.constants,
#                                            bounds=bounds,
#                                            weight_by_modulus=weight_by_modulus,
#                                            **kwargs)
#             self.parameters_ = parameters
#             if conf is not None:
#                 self.conf_ = conf
#         else:
#             # TODO auto calculate initial guesses
#             raise ValueError('no initial guess supplied')
#         return parameters , conf

from fileinput import filename
import pandas as pd
filename = 'C:/Users/User/Desktop/Masterarbeit/V1/V1/24_03_2022/eis/eis/Test_voltage.xlsx'
data = pd.read_excel(filename)
print(data)