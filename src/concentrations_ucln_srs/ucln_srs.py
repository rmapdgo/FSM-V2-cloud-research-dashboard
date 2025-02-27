import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

class PhantomDataProcessor:
    def formula(self, data):
        # Assuming data is a DataFrame
        data_df = pd.DataFrame(data)
        # Extract the data starting from row 9
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
        
        # Extract the time data
        Time = data['Time']
        
        # Group mappings
        GroupA_Detector1 = ['LED_A_784_DET1', 'LED_A_800_DET1', 'LED_A_818_DET1', 'LED_A_835_DET1', 'LED_A_851_DET1', 'LED_A_881_DET1']
        GroupA_Detector2 = ['LED_A_784_DET2', 'LED_A_800_DET2', 'LED_A_818_DET2', 'LED_A_835_DET2', 'LED_A_851_DET2', 'LED_A_881_DET2']
        GroupA_Detector3 = ['LED_A_784_DET3', 'LED_A_800_DET3', 'LED_A_818_DET3', 'LED_A_835_DET3', 'LED_A_851_DET3', 'LED_A_881_DET3']
        
        GroupB_Detector1 = ['LED_B_784_DET1', 'LED_B_800_DET1', 'LED_B_818_DET1', 'LED_B_835_DET1', 'LED_B_851_DET1', 'LED_B_881_DET1']
        GroupB_Detector2 = ['LED_B_784_DET2', 'LED_B_800_DET2', 'LED_B_818_DET2', 'LED_B_835_DET2', 'LED_B_851_DET2', 'LED_B_881_DET2']
        GroupB_Detector3 = ['LED_B_784_DET3', 'LED_B_800_DET3', 'LED_B_818_DET3', 'LED_B_835_DET3', 'LED_B_851_DET3', 'LED_B_881_DET3']

        
        group_sets = [GroupA_Detector1, GroupA_Detector2, GroupA_Detector3, GroupB_Detector1, GroupB_Detector2, GroupB_Detector3]
        for i in group_sets:
            print('i', i)
            for j in i:
                print('j', j)
                x = data[j]
                print('x', x)
                if x.iloc[0] == 0.0000:
                    x.iloc[0] = 1.0 
        
        # Extracting the data for each group
        group_a_1 = data[GroupA_Detector1].apply(pd.to_numeric, errors='coerce').fillna(0).values
        group_a_2 = data[GroupA_Detector2].apply(pd.to_numeric, errors='coerce').fillna(0).values
        group_a_3 = data[GroupA_Detector3].apply(pd.to_numeric, errors='coerce').fillna(0).values
        group_b_1 = data[GroupB_Detector1].apply(pd.to_numeric, errors='coerce').fillna(0).values
        group_b_2 = data[GroupB_Detector2].apply(pd.to_numeric, errors='coerce').fillna(0).values
        group_b_3 = data[GroupB_Detector3].apply(pd.to_numeric, errors='coerce').fillna(0).values
        
        # Wavelength and DPF values
        #wavelengths = np.array([800, 818, 835, 851, 881])
        wavelengths = np.array([784, 800, 818, 835, 851, 881])
        dpf = 4.99
        
        # Load extinction coefficients
        extinction_coefficients = pd.read_csv("src/concentrations_ucln_srs/defaults.csv")
        
        # Inverse of extinction coefficients
        ex_co = []
        for wavelength in wavelengths:
            for i, j in enumerate(extinction_coefficients.iloc[:, 0]):
                if wavelength == j:
                    ex_co.append(extinction_coefficients.iloc[i, :])
        
        ex_co = np.array(ex_co)
        ext_coeffs = ex_co[:, 1:4]  # The first column is the wavelength
        ext_coeffs_inv = np.linalg.pinv(ext_coeffs)
        
        # Wavelength dependency (assuming it's part of the data)
        wavelength_dependency = ex_co[:, 4]

        # Return the data and coefficients for further processing
        return group_a_1, group_a_2, group_a_3, group_b_1, group_b_2, group_b_3, wavelengths, dpf, wavelength_dependency, ext_coeffs_inv
    

    def UCLN(self, data):
        # Using the formula function to extract the necessary variables
        group_a_1, group_a_2, group_a_3, group_b_1, group_b_2, group_b_3, wavelengths, dpf, wavelength_dependency, ext_coeffs_inv = self.formula(data)

        # Initialize attenuation matrices
        x, y = group_a_1.shape
        atten_a_1 = np.zeros((x, y))
        atten_a_2 = np.zeros((x, y))
        atten_a_3 = np.zeros((x, y))
        atten_b_1 = np.zeros((x, y))
        atten_b_2 = np.zeros((x, y))
        atten_b_3 = np.zeros((x, y))

        data_group_ab_1 = group_a_1 + group_b_1
        data_group_ab_2 = group_a_2 + group_b_2
        data_group_ab_3 = group_a_3 + group_b_3

        # Calculate log10 attenuation
        for i in range(x):
            atten_a_1[i, :] = np.log10(group_a_1[0, :] / group_a_1[i, :])
            atten_a_2[i, :] = np.log10(group_a_2[0, :] / group_a_2[i, :])
            atten_a_3[i, :] = np.log10(group_a_3[0, :] / group_a_3[i, :])
            atten_b_1[i, :] = np.log10(group_b_1[0, :] / group_b_1[i, :])
            atten_b_2[i, :] = np.log10(group_b_2[0, :] / group_b_2[i, :])
            atten_b_3[i, :] = np.log10(group_b_3[0, :] / group_b_3[i, :])

        # Averaged attenuation for AB groups
        atten_ab_1 = 0.5 * (atten_a_1 + atten_b_1)
        atten_ab_2 = 0.5 * (atten_a_2 + atten_b_2)
        atten_ab_3 = 0.5 * (atten_a_3 + atten_b_3)

        # Apply wavelength dependency
        atten_a_1_wldep = atten_a_1 / wavelength_dependency
        atten_a_2_wldep = atten_a_2 / wavelength_dependency
        atten_a_3_wldep = atten_a_3 / wavelength_dependency
        atten_b_1_wldep = atten_b_1 / wavelength_dependency
        atten_b_2_wldep = atten_b_2 / wavelength_dependency
        atten_b_3_wldep = atten_b_3 / wavelength_dependency
        atten_ab_1_wldep = atten_ab_1 / wavelength_dependency
        atten_ab_2_wldep = atten_ab_2 / wavelength_dependency
        atten_ab_3_wldep = atten_ab_3 / wavelength_dependency

        # Calculate concentrations using the inverse of extinction coefficients
        conc_a_1 = np.transpose(np.matmul(ext_coeffs_inv, atten_a_1_wldep.T) * (1 / (4 * dpf)))
        conc_a_2 = np.transpose(np.matmul(ext_coeffs_inv, atten_a_2_wldep.T) * (1 / (4 * dpf)))
        conc_a_3 = np.transpose(np.matmul(ext_coeffs_inv, atten_a_3_wldep.T) * (1 / (4 * dpf)))
        conc_b_1 = np.transpose(np.matmul(ext_coeffs_inv, atten_b_1_wldep.T) * (1 / (4 * dpf)))
        conc_b_2 = np.transpose(np.matmul(ext_coeffs_inv, atten_b_2_wldep.T) * (1 / (4 * dpf)))
        conc_b_3 = np.transpose(np.matmul(ext_coeffs_inv, atten_b_3_wldep.T) * (1 / (4 * dpf)))
        conc_ab_1 = np.transpose(np.matmul(ext_coeffs_inv, atten_ab_1_wldep.T) * (1 / (4 * dpf)))
        conc_ab_2 = np.transpose(np.matmul(ext_coeffs_inv, atten_ab_2_wldep.T) * (1 / (4 * dpf)))
        conc_ab_3 = np.transpose(np.matmul(ext_coeffs_inv, atten_ab_3_wldep.T) * (1 / (4 * dpf)))

        # Convert to DataFrames for plotting
        conc_a_1_df = pd.DataFrame(conc_a_1, columns=['HbO', 'HHb', 'oxCCO'])
        conc_a_2_df = pd.DataFrame(conc_a_2, columns=['HbO', 'HHb', 'oxCCO'])
        conc_a_3_df = pd.DataFrame(conc_a_3, columns=['HbO', 'HHb', 'oxCCO'])
        conc_b_1_df = pd.DataFrame(conc_b_1, columns=['HbO', 'HHb', 'oxCCO'])
        conc_b_2_df = pd.DataFrame(conc_b_2, columns=['HbO', 'HHb', 'oxCCO'])
        conc_b_3_df = pd.DataFrame(conc_b_3, columns=['HbO', 'HHb', 'oxCCO'])
        conc_ab_1_df = pd.DataFrame(conc_ab_1, columns=['HbO', 'HHb', 'oxCCO'])
        conc_ab_2_df = pd.DataFrame(conc_ab_2, columns=['HbO', 'HHb', 'oxCCO'])
        conc_ab_3_df = pd.DataFrame(conc_ab_3, columns=['HbO', 'HHb', 'oxCCO'])

        atten_a_1 = pd.DataFrame(atten_a_1)
        atten_a_2 = pd.DataFrame(atten_a_2)
        atten_a_3 = pd.DataFrame(atten_a_3)

        atten_b_1 = pd.DataFrame(atten_b_1)
        atten_b_2 = pd.DataFrame(atten_b_2)
        atten_b_3 = pd.DataFrame(atten_b_3)

        # Column names for attenuation arrays
        atten_a_1.columns = ['LED_A_784_DET1', 'LED_A_800_DET1', 'LED_A_818_DET1', 'LED_A_835_DET1', 'LED_A_851_DET1', 'LED_A_881_DET1']
        atten_a_2.columns = ['LED_A_784_DET2', 'LED_A_800_DET2', 'LED_A_818_DET2', 'LED_A_835_DET2', 'LED_A_851_DET2', 'LED_A_881_DET2']
        atten_a_3.columns = ['LED_A_784_DET3', 'LED_A_800_DET3', 'LED_A_818_DET3', 'LED_A_835_DET3', 'LED_A_851_DET3', 'LED_A_881_DET3']
    
        atten_b_1.columns = ['LED_B_784_DET1', 'LED_B_800_DET1', 'LED_B_818_DET1', 'LED_B_835_DET1', 'LED_B_851_DET1', 'LED_B_881_DET1']
        atten_b_2.columns = ['LED_B_784_DET2', 'LED_B_800_DET2', 'LED_B_818_DET2', 'LED_B_835_DET2', 'LED_B_851_DET2', 'LED_B_881_DET2']
        atten_b_3.columns = ['LED_B_784_DET3', 'LED_B_800_DET3', 'LED_B_818_DET3', 'LED_B_835_DET3', 'LED_B_851_DET3', 'LED_B_881_DET3']

        return conc_a_1_df, conc_a_2_df, conc_a_3_df, conc_b_1_df, conc_b_2_df, conc_b_3_df, ext_coeffs_inv, atten_a_1, atten_a_2, atten_a_3, atten_b_1, atten_b_2, atten_b_3, ext_coeffs_inv

#==================================SRS===================================================================================


def SRS(atten_a_1, atten_a_2, atten_a_3, atten_b_1, atten_b_2, atten_b_3, ext_coeffs_inv):
    wavelengths = np.array([784, 800, 818, 835, 851, 881])

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

    return sto2_a, sto2_b
#==================================Dual Slope===================================================================================


def dual_slope_wavelength(data, wavelengths, LED_A_det_seps, LED_B_det_seps, ext_coeffs_inv, dsf=8):
    ds_mua_results = {}
    
    for wavelength in wavelengths:
        col_A_det1 = f'LED_A_{wavelength}_DET1'
        col_A_det3 = f'LED_A_{wavelength}_DET3'
        col_B_det1 = f'LED_B_{wavelength}_DET1'
        col_B_det3 = f'LED_B_{wavelength}_DET3'
        
        LED_A_data = data[[col_A_det1, col_A_det3]].values
        LED_B_data = data[[col_B_det3, col_B_det1]].values
        
        ss_LED_A = []
        ss_LED_B = []
        
        for row in LED_A_data:
            num_detectors = len(LED_A_det_seps)
            avg_det = np.mean(LED_A_det_seps)
            var_det = np.var(LED_A_det_seps, ddof=1)
            slope_sum = 0
            for i in [num_detectors // 2]:
                r_N = LED_A_det_seps[num_detectors - (i + 1)]
                r_1 = LED_A_det_seps[i]
                I_N = row[num_detectors - (i + 1)]
                I_1 = row[i]
                log_ratio_r = 2 * np.log(r_N / r_1)
                log_ratio_I = np.log(I_N / I_1)
                slope_sum += (r_N - avg_det) * (log_ratio_r + log_ratio_I)
            ss_LED_A.append(slope_sum / (num_detectors * var_det))
        
        for row in LED_B_data:
            num_detectors = len(LED_B_det_seps)
            avg_det = np.mean(LED_B_det_seps)
            var_det = np.var(LED_B_det_seps, ddof=1)
            slope_sum = 0
            for i in [num_detectors // 2]:
                r_N = LED_B_det_seps[num_detectors - (i + 1)]
                r_1 = LED_B_det_seps[i]
                I_N = row[num_detectors - (i + 1)]
                log_ratio_I = np.log(I_N / I_1)
                slope_sum += (r_N - avg_det) * (log_ratio_r + log_ratio_I)
            ss_LED_B.append(slope_sum / (num_detectors * var_det))
        
        ss_LED_A = np.array(ss_LED_A) / dsf
        ss_LED_B = np.array(ss_LED_B) / dsf
        ds_mua_results[wavelength] = -(ss_LED_A + ss_LED_B) / (2 * dsf)
    
    mua_dual_slope = np.vstack([ds_mua_results[wl] for wl in wavelengths])
    conc_dual_slope = np.matmul(ext_coeffs_inv, mua_dual_slope)
    oxy_dual_slope = conc_dual_slope[0, :]
    deoxy_dual_slope = conc_dual_slope[1, :]
    sto2_dual_slope = (oxy_dual_slope / (oxy_dual_slope + deoxy_dual_slope)) * 100

    return sto2_dual_slope
