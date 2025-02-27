import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Define the PhantomDataProcessor class with formula and UCLN methods
# Define the class that contains both formula and UCLN methods
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
        extinction_coefficients = pd.read_csv("/home/darshana/Desktop/FSM_v2-dashboard/src/utils/defaults (1).csv")
        
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
    
    def UCLN(self, data, plot=False):
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

        print('atten_a_1', atten_a_1.shape)
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

        print('conc_a_1_df', conc_a_1_df)
        print('conc_a_2_df', conc_a_2_df)

        # Return results
        return conc_a_1_df, conc_a_2_df, conc_a_3_df, conc_b_1_df, conc_b_2_df, conc_b_3_df, conc_ab_1_df, conc_ab_2_df, conc_ab_3_df,atten_a_1_wldep, atten_a_2_wldep, atten_a_3_wldep, atten_b_1_wldep, atten_b_2_wldep, atten_b_3_wldep, ext_coeffs_inv


        
# Function to apply get_slope over each distance for Group A and Group B
def get_slope(atten_wldep, distances):
    # Ensure distances is reshaped correctly
    distances = np.array(distances).reshape(-1, 1)  # Shape should be (N, 1)
    
    A = np.hstack((np.ones_like(distances), distances))  # Shape (N, 2)
    results = []
    
    for i in range(atten_wldep.shape[0]):  # Iterate over rows (time points)
        for j in range(atten_wldep.shape[1]):  # Iterate over detectors
            p = np.linalg.lstsq(A, atten_wldep[i, j, :], rcond=None)[0]  # Least squares fit
            results.append(p[1])  # Append only the slope (p[1] is the slope)
    
    return np.array(results)


# Function to calculate k_mua, concentrations, and StO2
def srs_values(slope, wavelengths, ext_coeffs_inv, distances):
    h = 6.3e-4  # Heuristic constant for absorption
    
    k_mua = ((np.log(10) * np.mean(slope)) - (2 / np.mean([distances])**2)) / (3 * (1 - h * wavelengths))
    
    C = np.matmul(ext_coeffs_inv, k_mua)
    oxy, deoxy = C[0], C[1]
    StO2 = (oxy / (oxy + deoxy)) * 100
    
    return C, StO2, k_mua

# Assuming the PhantomDataProcessor class and other functions are already defined
# Assuming data is loaded from an Excel file
file_path = '/home/darshana/Desktop/FSM_v2-dashboard/src/uploads/PHANTOM_fsm_data_20241126_151441.xlsx'
data = pd.read_excel(file_path)

# Initialize PhantomDataProcessor instance
processor = PhantomDataProcessor()

# Call formula to extract necessary data
group_a_1, group_a_2, group_a_3, group_b_1, group_b_2, group_b_3, wavelengths, dpf, wavelength_dependency, ext_coeffs_inv = processor.formula(data)

# Call UCLN to get the wavelength-dependent attenuation values
conc_a_1_df, conc_a_2_df, conc_a_3_df, conc_b_1_df, conc_b_2_df, conc_b_3_df, conc_ab_1_df, conc_ab_2_df, conc_ab_3_df,atten_a_1_wldep, atten_a_2_wldep, atten_a_3_wldep, atten_b_1_wldep, atten_b_2_wldep, atten_b_3_wldep, ext_coeffs_inv = processor.UCLN(data)

# Stack the attenuation arrays for Group A and Group B
atten_wldep_A = np.stack([atten_a_1_wldep, atten_a_2_wldep, atten_a_3_wldep], axis=2)
atten_wldep_B = np.stack([atten_b_1_wldep, atten_b_2_wldep, atten_b_3_wldep], axis=2)

# Define the distances
detector_A_distance = [3, 4, 5]
detector_B_distance = [5, 4, 3]

# Get slopes for Group A and Group B
slope_A = get_slope(atten_wldep_A, detector_A_distance)
slope_B = get_slope(atten_wldep_B, detector_B_distance)

distances = [3,4,5]

# Calculate SRS values for Group A and Group B
C_A, StO2_A, k_mua_A = srs_values(slope_A, wavelengths, ext_coeffs_inv, distances)
C_B, StO2_B, k_mua_B = srs_values(slope_B, wavelengths, ext_coeffs_inv, distances)

# Now you have the results:
# slope_A, slope_B - slopes for Group A and Group B
# C_A, C_B - concentrations for Group A and Group B
# StO2_A, StO2_B - StO2 for Group A and Group B
# k_mua_A, k_mua_B - k_mua values for Group A and Group B

print('slope_A', slope_A)
print('slope_B', slope_B)
print('C_A', C_A)
print('C_B', C_B)
print('StO2_A', StO2_A)
print('StO2_B', StO2_B)
print('k_mua_A', k_mua_A)
print('k_mua_B', k_mua_B)

# Plotting the concentrations for HbO, HHb, and oxCCO
plt.figure(figsize=(12, 8))

# Plot HbO concentrations for Group A, B, and AB
plt.subplot(3, 1, 1)
plt.plot(conc_a_1_df['HbO'], label=' HbO', color='red')
plt.plot(conc_a_1_df['HHb'], label='HHb', color='blue')#
plt.plot(conc_a_1_df['oxCCO'], label='oxCCO', color='green')
#plt.plot(conc_ab_1_df['HbO'], label='Group AB', color='green')
plt.title('Concentration of conc_a_1_df')
plt.xlabel('Time')
plt.ylabel('HbO Concentration (µM)')
plt.legend()

# Plot HHb concentrations for Group A, B, and AB
plt.subplot(3, 1, 2)

plt.plot(conc_b_1_df['HbO'], label='HbO', color='red')
plt.plot(conc_b_1_df['HHb'], label='HHb', color='blue')
plt.plot(conc_b_1_df['oxCCO'], label='oxCCO', color='green')
#plt.plot(conc_ab_1_df['HHb'], label='Group AB', color='green')
plt.title('Concentration of conc_b_1_df')
plt.xlabel('Time')
plt.ylabel('HHb Concentration (µM)')
plt.legend()



# Plotting k_mua for Group A and Group B in a separate figure
plt.figure(figsize=(12, 6))

# Plot k_mua for Group A and Group B
plt.plot(k_mua_A, label='Group A k_mua', color='blue')
plt.plot(k_mua_B, label='Group B k_mua', color='red')
plt.title('k_mua Values for Group A and Group B')
plt.xlabel('Time')
plt.ylabel('k_mua')
plt.legend()

# Show the k_mua plot
plt.tight_layout()
plt.show()

# Plotting the slopes for Group A and Group B in a separate figure
plt.figure(figsize=(12, 6))

# Plot slopes for Group A and Group B
plt.plot(slope_A, label='Group A Slopes', color='blue')
plt.plot(slope_B, label='Group B Slopes', color='red')
plt.title('Slopes for Group A and Group B')
plt.xlabel('Time')
plt.ylabel('Slope')
plt.legend()

# Show the slopes plot
plt.tight_layout()
plt.show()

