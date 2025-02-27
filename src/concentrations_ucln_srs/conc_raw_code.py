import numpy as np
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt

file_path = '/home/darshana/Desktop/FSM_v2-dashboard/src/uploads/PHANTOM_fsm_data_20241126_151441.xlsx'
data = pd.read_excel(file_path)

data_df = pd.DataFrame(data)
data = data_df.iloc[9:, :]

data.columns = ['Time', 'System Time (s)', 'Sample Time (s)',
                'LED_A_784_DET1', 'LED_A_784_DET2', 'LED_A_784_DET3',
                'LED_A_800_DET1', 'LED_A_800_DET2', 'LED_A_800_DET3',
                'LED_A_818_DET1', 'LED_A_818_DET2', 'LED_A_818_DET3',
                'LED_A_835_DET1', 'LED_A_835_DET2', 'LED_A_835_DET3',
                'LED_A_851_DET1', 'LED_A_851_DET2', 'LED_A_851_DET3',
                'LED_A_881_DET1', 'LED_A_881_DET2', 'LED_A_881_DET3',
                'LED_A_DARK_DET1', 'LED_A_DARK_DET2', 'LED_A_DARK_DET3',
                'LED_B_784_DET1', 'LED_B_784_DET2', 'LED_B_784_DET3',
                'LED_B_800_DET1', 'LED_B_800_DET2', 'LED_B_800_DET3',
                'LED_B_818_DET1', 'LED_B_818_DET2', 'LED_B_818_DET3',
                'LED_B_835_DET1', 'LED_B_835_DET2', 'LED_B_835_DET3',
                'LED_B_851_DET1', 'LED_B_851_DET2', 'LED_B_851_DET3',
                'LED_B_881_DET1', 'LED_B_881_DET2', 'LED_B_881_DET3',
                'LED_B_DARK_DET1', 'LED_B_DARK_DET2', 'LED_B_DARK_DET3']

Time = data['Time']
wavelengths = np.array([784, 800, 818, 835, 851, 881])
dpf = 4.99

extinction_coefficients = pd.read_csv(
    "/home/darshana/Desktop/FSM_v2-dashboard/src/concentrations_ucln_srs/defaults.csv")

ex_co = []
for wavelength in wavelengths:
    for i, j in enumerate(extinction_coefficients.iloc[:, 0]):
        if wavelength == j:
            ex_co.append(extinction_coefficients.iloc[i, :])

ex_co = np.array(ex_co)
ext_coeffs = ex_co[:, 1:3]  # just take oxy and deoxy for now
#ext_coeffs_t = ext_coeffs.T
ext_coeffs_inv = np.linalg.pinv(ext_coeffs)


wavelength_dependency = ex_co[:, 4]

GroupA_Detector1 = ['LED_A_784_DET1', 'LED_A_800_DET1', 'LED_A_818_DET1', 'LED_A_835_DET1', 'LED_A_851_DET1',
                    'LED_A_881_DET1']
GroupA_Detector2 = ['LED_A_784_DET2', 'LED_A_800_DET2', 'LED_A_818_DET2', 'LED_A_835_DET2', 'LED_A_851_DET2',
                    'LED_A_881_DET2']
GroupA_Detector3 = ['LED_A_784_DET3', 'LED_A_800_DET3', 'LED_A_818_DET3', 'LED_A_835_DET3', 'LED_A_851_DET3',
                    'LED_A_881_DET3']

GroupB_Detector1 = ['LED_B_784_DET1', 'LED_B_800_DET1', 'LED_B_818_DET1', 'LED_B_835_DET1', 'LED_B_851_DET1',
                    'LED_B_881_DET1']
GroupB_Detector2 = ['LED_B_784_DET2', 'LED_B_800_DET2', 'LED_B_818_DET2', 'LED_B_835_DET2', 'LED_B_851_DET2',
                    'LED_B_881_DET2']
GroupB_Detector3 = ['LED_B_784_DET3', 'LED_B_800_DET3', 'LED_B_818_DET3', 'LED_B_835_DET3', 'LED_B_851_DET3',
                    'LED_B_881_DET3']

# Extracting the data for each group
group_a_1 = data[GroupA_Detector1].apply(pd.to_numeric, errors='coerce').fillna(0).values
group_a_2 = data[GroupA_Detector2].apply(pd.to_numeric, errors='coerce').fillna(0).values
group_a_3 = data[GroupA_Detector3].apply(pd.to_numeric, errors='coerce').fillna(0).values
group_b_1 = data[GroupB_Detector1].apply(pd.to_numeric, errors='coerce').fillna(0).values
group_b_2 = data[GroupB_Detector2].apply(pd.to_numeric, errors='coerce').fillna(0).values
group_b_3 = data[GroupB_Detector3].apply(pd.to_numeric, errors='coerce').fillna(0).values

x, y = group_a_1.shape
atten_a_1 = np.zeros((x, y))
atten_a_2 = np.zeros((x, y))
atten_a_3 = np.zeros((x, y))
atten_b_1 = np.zeros((x, y))
atten_b_2 = np.zeros((x, y))
atten_b_3 = np.zeros((x, y))

for i in range(x):
    atten_a_1[i, :] = np.log10(group_a_1[0, :] / group_a_1[i, :])
    atten_a_2[i, :] = np.log10(group_a_2[0, :] / group_a_2[i, :])
    atten_a_3[i, :] = np.log10(group_a_3[0, :] / group_a_3[i, :])

    atten_b_1[i, :] = np.log10(group_b_1[0, :] / group_b_1[i, :])
    atten_b_2[i, :] = np.log10(group_b_2[0, :] / group_b_2[i, :])
    atten_b_3[i, :] = np.log10(group_b_3[0, :] / group_b_3[i, :])

atten_a_1_wldep = atten_a_1
atten_a_2_wldep = atten_a_2
atten_a_3_wldep = atten_a_3

atten_b_1_wldep = atten_b_1
atten_b_2_wldep = atten_b_2
atten_b_3_wldep = atten_b_3

atten_a_1 = pd.DataFrame(atten_a_1)
atten_a_2 = pd.DataFrame(atten_a_2)
atten_a_3 = pd.DataFrame(atten_a_3)

atten_b_1 = pd.DataFrame(atten_b_1)
atten_b_2 = pd.DataFrame(atten_b_2)
atten_b_3 = pd.DataFrame(atten_b_3)

atten_a_1.columns = ['LED_A_784_DET1', 'LED_A_800_DET1', 'LED_A_818_DET1', 'LED_A_835_DET1', 'LED_A_851_DET1',
                     'LED_A_881_DET1']
atten_a_2.columns = ['LED_A_784_DET2', 'LED_A_800_DET2', 'LED_A_818_DET2', 'LED_A_835_DET2', 'LED_A_851_DET2',
                     'LED_A_881_DET2']
atten_a_3.columns = ['LED_A_784_DET3', 'LED_A_800_DET3', 'LED_A_818_DET3', 'LED_A_835_DET3', 'LED_A_851_DET3',
                     'LED_A_881_DET3']

atten_b_1.columns = ['LED_B_784_DET1', 'LED_B_800_DET1', 'LED_B_818_DET1', 'LED_B_835_DET1', 'LED_B_851_DET1',
                     'LED_B_881_DET1']
atten_b_2.columns = ['LED_B_784_DET2', 'LED_B_800_DET2', 'LED_B_818_DET2', 'LED_B_835_DET2', 'LED_B_851_DET2',
                     'LED_B_881_DET2']
atten_b_3.columns = ['LED_B_784_DET3', 'LED_B_800_DET3', 'LED_B_818_DET3', 'LED_B_835_DET3', 'LED_B_851_DET3',
                     'LED_B_881_DET3']

Group_A_784 = [atten_a_1['LED_A_784_DET1'], atten_a_2['LED_A_784_DET2'], atten_a_3['LED_A_784_DET3']]
Group_A_800 = [atten_a_1['LED_A_800_DET1'], atten_a_2['LED_A_800_DET2'], atten_a_3['LED_A_800_DET3']]
Group_A_818 = [atten_a_1['LED_A_818_DET1'], atten_a_2['LED_A_818_DET2'], atten_a_3['LED_A_818_DET3']]
Group_A_835 = [atten_a_1['LED_A_835_DET1'], atten_a_2['LED_A_835_DET2'], atten_a_3['LED_A_835_DET3']]
Group_A_851 = [atten_a_1['LED_A_851_DET1'], atten_a_2['LED_A_851_DET2'], atten_a_3['LED_A_851_DET3']]
Group_A_881 = [atten_a_1['LED_A_881_DET1'], atten_a_2['LED_A_881_DET2'], atten_a_3['LED_A_881_DET3']]

Group_B_784 = [atten_b_1['LED_B_784_DET1'], atten_b_2['LED_B_784_DET2'], atten_b_3['LED_B_784_DET3']]
Group_B_800 = [atten_b_1['LED_B_800_DET1'], atten_b_2['LED_B_800_DET2'], atten_b_3['LED_B_800_DET3']]
Group_B_818 = [atten_b_1['LED_B_818_DET1'], atten_b_2['LED_B_818_DET2'], atten_b_3['LED_B_818_DET3']]
Group_B_835 = [atten_b_1['LED_B_835_DET1'], atten_b_2['LED_B_835_DET2'], atten_b_3['LED_B_835_DET3']]
Group_B_851 = [atten_b_1['LED_B_851_DET1'], atten_b_2['LED_B_851_DET2'], atten_b_3['LED_B_851_DET3']]
Group_B_881 = [atten_b_1['LED_B_881_DET1'], atten_b_2['LED_B_881_DET2'], atten_b_3['LED_B_881_DET3']]

detector_A_distance = np.array([[3], [4], [5]])
detector_B_distance = np.array([[5], [4], [3]])

##Do group A first##
A_groupA = np.hstack((detector_A_distance,np.ones_like(detector_A_distance) ))

# 784nm
atten_wldep_A_784 = np.array(Group_A_784, dtype=float)  # change atten_wldp with group from above
m_784_A = np.zeros((1, len(atten_wldep_A_784[0])))
c_784_A = np.zeros((1, len(atten_wldep_A_784[0])))
for x in range(0, len(atten_wldep_A_784[0])):
    m_784_A[0, x], c_784_A[0, x] = np.linalg.lstsq(A_groupA, atten_wldep_A_784[:, x], rcond=None)[0]

# 800nm
atten_wldep_A_800 = np.array(Group_A_800, dtype=float)  # change atten_wldp with group from above
m_800_A = np.zeros((1, len(atten_wldep_A_800[0])))
c_800_A = np.zeros((1, len(atten_wldep_A_800[0])))
for x in range(0, len(atten_wldep_A_800[0])):
    m_800_A[0, x], c_800_A[0, x] = np.linalg.lstsq(A_groupA, atten_wldep_A_800[:, x], rcond=None)[0]

# 818nm
atten_wldep_A_818 = np.array(Group_A_818, dtype=float)  # change atten_wldp with group from above
m_818_A = np.zeros((1, len(atten_wldep_A_818[0])))
c_818_A = np.zeros((1, len(atten_wldep_A_818[0])))
for x in range(0, len(atten_wldep_A_818[0])):
    m_818_A[0, x], c_818_A[0, x] = np.linalg.lstsq(A_groupA, atten_wldep_A_818[:, x], rcond=None)[0]

# 835nm
atten_wldep_A_835 = np.array(Group_A_835, dtype=float)  # change atten_wldp with group from above
m_835_A = np.zeros((1, len(atten_wldep_A_835[0])))
c_835_A = np.zeros((1, len(atten_wldep_A_835[0])))
for x in range(0, len(atten_wldep_A_818[0])):
    m_835_A[0, x], c_835_A[0, x] = np.linalg.lstsq(A_groupA, atten_wldep_A_835[:, x], rcond=None)[0]

# 851nm
atten_wldep_A_851 = np.array(Group_A_851, dtype=float)  # change atten_wldp with group from above
m_851_A = np.zeros((1, len(atten_wldep_A_851[0])))
c_851_A = np.zeros((1, len(atten_wldep_A_851[0])))
for x in range(0, len(atten_wldep_A_851[0])):
    m_851_A[0, x], c_851_A[0, x] = np.linalg.lstsq(A_groupA, atten_wldep_A_851[:, x], rcond=None)[0]

# 881nm
atten_wldep_A_881 = np.array(Group_A_881, dtype=float)  # change atten_wldp with group from above
m_881_A = np.zeros((1, len(atten_wldep_A_881[0])))
c_881_A = np.zeros((1, len(atten_wldep_A_881[0])))
for x in range(0, len(atten_wldep_A_881[0])):
    m_881_A[0, x], c_881_A[0, x] = np.linalg.lstsq(A_groupA, atten_wldep_A_881[:, x], rcond=None)[0]

##Do group B##
A_groupB = np.hstack((detector_B_distance,np.ones_like(detector_B_distance) ))

# 784nm
atten_wldep_B_784 = np.array(Group_B_784, dtype=float)  # change atten_wldp with group from above
m_784_B = np.zeros((1, len(atten_wldep_B_784[0])))
c_784_B = np.zeros((1, len(atten_wldep_B_784[0])))
for x in range(0, len(atten_wldep_B_784[0])):
    m_784_B[0, x], c_784_B[0, x] = np.linalg.lstsq(A_groupB, atten_wldep_B_784[:, x], rcond=None)[0]

# 800nm
atten_wldep_B_800 = np.array(Group_B_800, dtype=float)  # change atten_wldp with group from above
m_800_B = np.zeros((1, len(atten_wldep_B_800[0])))
c_800_B = np.zeros((1, len(atten_wldep_B_800[0])))
for x in range(0, len(atten_wldep_B_800[0])):
    m_800_B[0, x], c_800_B[0, x] = np.linalg.lstsq(A_groupB, atten_wldep_B_800[:, x], rcond=None)[0]

# 818nm
atten_wldep_B_818 = np.array(Group_B_818, dtype=float)  # change atten_wldp with group from above
m_818_B = np.zeros((1, len(atten_wldep_B_818[0])))
c_818_B = np.zeros((1, len(atten_wldep_B_818[0])))
for x in range(0, len(atten_wldep_B_818[0])):
    m_818_B[0, x], c_818_B[0, x] = np.linalg.lstsq(A_groupB, atten_wldep_B_818[:, x], rcond=None)[0]

# 835nm
atten_wldep_B_835 = np.array(Group_B_835, dtype=float)  # change atten_wldp with group from above
m_835_B = np.zeros((1, len(atten_wldep_B_835[0])))
c_835_B = np.zeros((1, len(atten_wldep_B_835[0])))
for x in range(0, len(atten_wldep_B_818[0])):
    m_835_B[0, x], c_835_B[0, x] = np.linalg.lstsq(A_groupB, atten_wldep_B_835[:, x], rcond=None)[0]

# 851nm
atten_wldep_B_851 = np.array(Group_B_851, dtype=float)  # change atten_wldp with group from above
m_851_B = np.zeros((1, len(atten_wldep_B_851[0])))
c_851_B = np.zeros((1, len(atten_wldep_B_851[0])))
for x in range(0, len(atten_wldep_B_851[0])):
    m_851_B[0, x], c_851_B[0, x] = np.linalg.lstsq(A_groupB, atten_wldep_B_851[:, x], rcond=None)[0]

# 881nm
atten_wldep_B_881 = np.array(Group_B_881, dtype=float)  # change atten_wldp with group from above
m_881_B = np.zeros((1, len(atten_wldep_B_881[0])))
c_881_B = np.zeros((1, len(atten_wldep_B_881[0])))
for x in range(0, len(atten_wldep_B_881[0])):
    m_881_B[0, x], c_881_B[0, x] = np.linalg.lstsq(A_groupB, atten_wldep_B_881[:, x], rcond=None)[0]

h = 6.3e-4
# group A
k_mua_784_A = (1 / (3 * (1 - (h * wavelengths[0])))) * (np.log(10) * m_784_A - (2 / np.mean(detector_A_distance)))**2
k_mua_800_A = (1 / (3 * (1 - (h * wavelengths[1])))) * (np.log(10) * m_800_A - (2 / np.mean(detector_A_distance)))**2
k_mua_818_A = (1 / (3 * (1 - (h * wavelengths[2])))) * (np.log(10) * m_818_A - (2 / np.mean(detector_A_distance)))**2
k_mua_835_A = (1 / (3 * (1 - (h * wavelengths[3])))) * (np.log(10) * m_835_A - (2 / np.mean(detector_A_distance)))**2
k_mua_851_A = (1 / (3 * (1 - (h * wavelengths[4])))) * (np.log(10) * m_851_A - (2 / np.mean(detector_A_distance)))**2
k_mua_881_A = (1 / (3 * (1 - (h * wavelengths[5])))) * (np.log(10) * m_881_A - (2 / np.mean(detector_A_distance)))**2

#groupB
k_mua_784_B = (1 / (3 * (1 - (h * wavelengths[0])))) * (np.log(10) * m_784_B - (2 / np.mean(detector_B_distance)))**2
k_mua_800_B = (1 / (3 * (1 - (h * wavelengths[1])))) * (np.log(10) * m_800_B - (2 / np.mean(detector_B_distance)))**2
k_mua_818_B = (1 / (3 * (1 - (h * wavelengths[2])))) * (np.log(10) * m_818_B - (2 / np.mean(detector_B_distance)))**2
k_mua_835_B = (1 / (3 * (1 - (h * wavelengths[3])))) * (np.log(10) * m_835_B - (2 / np.mean(detector_B_distance)))**2
k_mua_851_B = (1 / (3 * (1 - (h * wavelengths[4])))) * (np.log(10) * m_851_B - (2 / np.mean(detector_B_distance)))**2
k_mua_881_B = (1 / (3 * (1 - (h * wavelengths[5])))) * (np.log(10) * m_881_B - (2 / np.mean(detector_B_distance)))**2


k_mua_A = np.vstack([k_mua_784_A, k_mua_800_A,k_mua_818_A,k_mua_835_A,k_mua_851_A, k_mua_881_A])
k_mua_B = np.vstack([k_mua_784_B, k_mua_800_B,k_mua_818_B,k_mua_835_B,k_mua_851_B, k_mua_881_B])

C_A = np.matmul(ext_coeffs_inv, k_mua_A)
C_B = np.matmul(ext_coeffs_inv, k_mua_B)

oxy_a = C_A[0]
deoxy_a = C_A[1]

oxy_b = C_B[0]
deoxy_b = C_B[1]

sto2_a = (oxy_a / (oxy_a + deoxy_a)) * 100
sto2_b = (oxy_b / (oxy_b + deoxy_b)) * 100

matplotlib.use('TkAgg')
plt.figure()
plt.plot(sto2_a)
plt.savefig('/home/darshana/Desktop/FSM_v2-dashboard/src/concentration_data/sto2_a.png')


matplotlib.use('TkAgg')
plt.figure()
plt.plot(sto2_b)
plt.savefig('/home/darshana/Desktop/FSM_v2-dashboard/src/concentration_data/sto2_b.png')



print('end')

