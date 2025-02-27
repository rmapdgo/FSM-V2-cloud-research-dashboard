import pandas as pd
import numpy as np
import h5py
import os
import datetime

def create_snirf(filepath):
    # Read data from the Excel sheet
    raw_data = pd.read_excel(filepath)
    print('raw_data', raw_data)

    # Extract the relevant metadata
    Hardware_Version = raw_data.iloc[2, 1]
    Firmware_Version = raw_data.iloc[3, 1]
    NIR_LED_Emitter_Current = raw_data.iloc[6, 1]
    ADC_Gain = raw_data.iloc[7, 1]
    date_part_from_filename = raw_data.iloc[4, 1]
    time_part_from_filename = raw_data.iloc[5, 1]

    # Extract the data starting from row 6
    data = raw_data.iloc[9:, :]
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

    print('data', data)

    # Convert the relevant columns to numeric, forcing errors to NaN
    data = data.apply(pd.to_numeric, errors='coerce')

    wavelengths = [784, 800, 818, 835, 851, 881]
    detector_labels = ['DET1', 'DET2', 'DET3']
    source_labels = ['LED_A', 'LED_B']


    # Prepare new data structure
    data_new_columns = {}

    # Loop to add LED-A and LED-B data for each wavelength and detector
    for i, wavelength in enumerate(wavelengths):
        # Extracting data for each wavelength and detector
        data_new_columns[f'LED_A_{wavelength}_DET1'] = data[f'LED_A_{wavelength}_DET1']
        data_new_columns[f'LED_A_{wavelength}_DET2'] = data[f'LED_A_{wavelength}_DET2']
        data_new_columns[f'LED_A_{wavelength}_DET3'] = data[f'LED_A_{wavelength}_DET3']
        data_new_columns[f'LED_B_{wavelength}_DET1'] = data[f'LED_B_{wavelength}_DET1']
        data_new_columns[f'LED_B_{wavelength}_DET2'] = data[f'LED_B_{wavelength}_DET2']
        data_new_columns[f'LED_B_{wavelength}_DET3'] = data[f'LED_B_{wavelength}_DET3']

    # Extracting the 'Dark' columns (A and B)
    data_new_columns['LED_A_DARK_DET1'] = data['LED_A_DARK_DET1']
    data_new_columns['LED_A_DARK_DET2'] = data['LED_A_DARK_DET2']
    data_new_columns['LED_A_DARK_DET3'] = data['LED_A_DARK_DET3']

    data_new_columns['LED_B_DARK_DET1'] = data['LED_B_DARK_DET1']
    data_new_columns['LED_B_DARK_DET2'] = data['LED_B_DARK_DET2']
    data_new_columns['LED_B_DARK_DET3'] = data['LED_B_DARK_DET3']

    # Convert to DataFrame
    data_new_columns_df = pd.DataFrame(data_new_columns)
    print('data_new_columns_df', data_new_columns_df)

    # Ensure all columns are numeric (float) before writing to HDF5
    data_new_columns_df = data_new_columns_df.astype(np.float32)

    output_dir = '/home/darshana/Documents/Code/FSM-V2/src/output_files'

    # Prepare the SNIRF file
    snirf_file = os.path.join(output_dir, os.path.splitext(os.path.basename(filepath))[0] + ".snirf")

    #Get filename
    snirf_file_name = (os.path.splitext(os.path.basename(filepath))[0] + ".snirf")

    # Metadata to be added to the SNIRF file
    data_new_columns_name = np.array(data_new_columns_df.columns, dtype='S')
    print('data_new_columns_name', data_new_columns_name)

    # Ensure the column is in datetime format
    raw_data.iloc[10:, 0] = pd.to_datetime(raw_data.iloc[10:, 0])

    # Apply strftime to each entry in the time data
    time_data = raw_data.iloc[10:, 0].apply(lambda x: x.strftime("%H:%M:%S %f"))

    # Convert the time data to numpy string format
    time_data = np.array(time_data, dtype='S')
    print('time_data', time_data)

    # Detector positions
    detpos = np.array([[3.], [4.], [5.]])  # Assuming a 3-detector setup

    # Source positions (just placeholders in this case)
    sorpos = np.array([[0., 8.]])

    # Wavelengths as float values
    wavelen = [float(i) for i in wavelengths]

    detector_source_distance_data = np.array([
    ['LED_A', 'DET_1', 'DET_2', 'DET_3', 'LED_B'],     # Row for "X" (labels or zeros)
    ['0cm', '3cm', '4cm', '5cm', '8cm'],  # Row for distances for LED_A
    ], dtype='S10')  # String type for labels like "0cm", "3cm", etc.

    # Write SNIRF file
    with h5py.File(snirf_file, 'w') as f:
        f.create_dataset("/formatVersion", data='1.0')

        nirs_group = f.create_group("nirs/data1")
        nirs_group.create_dataset("dataTimeSeries", data=data_new_columns_df.to_numpy())
        nirs_group.create_dataset("time", data=time_data)
        
        measurementlist1 = nirs_group.create_group("measurementList1")
        measurementlist1.create_dataset("dataType", data=np.array([1]))  # Assuming 1 is the intended data type
        measurementlist1.create_dataset("dataTypeIndex", data=np.array([1]))
        measurementlist1.create_dataset("detectorIndex", data=np.array([1]))  # Adjust according to your number of detectors
        measurementlist1.create_dataset("sourceIndex", data=np.array([1]))
        measurementlist1.create_dataset("wavelengthIndex", data=np.array([1]))  # Adjust for actual wavelength index
    
        measurementlist2 = nirs_group.create_group("measurementList2")
        measurementlist2.create_dataset("dataType", data=np.array([1]))
        measurementlist2.create_dataset("dataTypeIndex", data=np.array([1]))
        measurementlist2.create_dataset("detectorIndex", data=np.array([2]))  # Adjust for actual detector index
        measurementlist2.create_dataset("sourceIndex", data=np.array([1]))
        measurementlist2.create_dataset("wavelengthIndex", data=np.array([1]))

        measurementlist3 = nirs_group.create_group(f"measurementList3")
        measurementlist3.create_dataset("dataType", data=np.array([1]))
        measurementlist3.create_dataset("dataTypeIndex", data=np.array([1]))
        measurementlist3.create_dataset("detectorIndex", data=np.array([3]))
        measurementlist3.create_dataset("sourceIndex", data=np.array([1]))
        measurementlist3.create_dataset("wavelengthIndex", data=np.array([1]))

        measurementlist4 = nirs_group.create_group(f"measurementList4")
        measurementlist4.create_dataset("dataType", data=np.array([1]))
        measurementlist4.create_dataset("dataTypeIndex", data=np.array([1]))
        measurementlist4.create_dataset("detectorIndex", data=np.array([1]))
        measurementlist4.create_dataset("sourceIndex", data=np.array([2]))
        measurementlist4.create_dataset("wavelengthIndex", data=np.array([1]))

        measurementlist5 = nirs_group.create_group(f"measurementList5")
        measurementlist5.create_dataset("dataType", data=np.array([1]))
        measurementlist5.create_dataset("dataTypeIndex", data=np.array([1]))
        measurementlist5.create_dataset("detectorIndex", data=np.array([2]))
        measurementlist5.create_dataset("sourceIndex", data=np.array([2]))
        measurementlist5.create_dataset("wavelengthIndex", data=np.array([1]))

        measurementlist6 = nirs_group.create_group(f"measurementList6")
        measurementlist6.create_dataset("dataType", data=np.array([1]))
        measurementlist6.create_dataset("dataTypeIndex", data=np.array([1]))
        measurementlist6.create_dataset("detectorIndex", data=np.array([3]))
        measurementlist6.create_dataset("sourceIndex", data=np.array([2]))
        measurementlist6.create_dataset("wavelengthIndex", data=np.array([1]))

        measurementlist7 = nirs_group.create_group(f"measurementList7")
        measurementlist7.create_dataset("dataType", data=np.array([1]))
        measurementlist7.create_dataset("dataTypeIndex", data=np.array([1]))
        measurementlist7.create_dataset("detectorIndex", data=np.array([1]))
        measurementlist7.create_dataset("sourceIndex", data=np.array([1]))
        measurementlist7.create_dataset("wavelengthIndex", data=np.array([2]))

        measurementlist8 = nirs_group.create_group(f"measurementList8")
        measurementlist8.create_dataset("dataType", data=np.array([1]))
        measurementlist8.create_dataset("dataTypeIndex", data=np.array([1]))
        measurementlist8.create_dataset("detectorIndex", data=np.array([2]))
        measurementlist8.create_dataset("sourceIndex", data=np.array([1]))
        measurementlist8.create_dataset("wavelengthIndex", data=np.array([2]))

        measurementlist9 = nirs_group.create_group(f"measurementList9")
        measurementlist9.create_dataset("dataType", data=np.array([1]))
        measurementlist9.create_dataset("dataTypeIndex", data=np.array([1]))
        measurementlist9.create_dataset("detectorIndex", data=np.array([3]))
        measurementlist9.create_dataset("sourceIndex", data=np.array([1]))
        measurementlist9.create_dataset("wavelengthIndex", data=np.array([2]))
        
        measurementlist10 = nirs_group.create_group(f"measurementList10")
        measurementlist10.create_dataset("dataType", data=np.array([1]))
        measurementlist10.create_dataset("dataTypeIndex", data=np.array([1]))
        measurementlist10.create_dataset("detectorIndex", data=np.array([1]))
        measurementlist10.create_dataset("sourceIndex", data=np.array([2]))
        measurementlist10.create_dataset("wavelengthIndex", data=np.array([2]))

        measurementlist11 = nirs_group.create_group(f"measurementList11")
        measurementlist11.create_dataset("dataType", data=np.array([1]))
        measurementlist11.create_dataset("dataTypeIndex", data=np.array([1]))
        measurementlist11.create_dataset("detectorIndex", data=np.array([2]))
        measurementlist11.create_dataset("sourceIndex", data=np.array([2]))
        measurementlist11.create_dataset("wavelengthIndex", data=np.array([2]))

        measurementlist12 = nirs_group.create_group(f"measurementList12")
        measurementlist12.create_dataset("dataType", data=np.array([1]))
        measurementlist12.create_dataset("dataTypeIndex", data=np.array([1]))
        measurementlist12.create_dataset("detectorIndex", data=np.array([3]))
        measurementlist12.create_dataset("sourceIndex", data=np.array([2]))
        measurementlist12.create_dataset("wavelengthIndex", data=np.array([2]))

        measurementlist13 = nirs_group.create_group(f"measurementList13")
        measurementlist13.create_dataset("dataType", data=np.array([1]))
        measurementlist13.create_dataset("dataTypeIndex", data=np.array([1]))
        measurementlist13.create_dataset("detectorIndex", data=np.array([1]))
        measurementlist13.create_dataset("sourceIndex", data=np.array([1]))
        measurementlist13.create_dataset("wavelengthIndex", data=np.array([3]))

        measurementlist14 = nirs_group.create_group(f"measurementList14")
        measurementlist14.create_dataset("dataType", data=np.array([1]))
        measurementlist14.create_dataset("dataTypeIndex", data=np.array([1]))
        measurementlist14.create_dataset("detectorIndex", data=np.array([2]))
        measurementlist14.create_dataset("sourceIndex", data=np.array([1]))
        measurementlist14.create_dataset("wavelengthIndex", data=np.array([3]))

        measurementlist15 = nirs_group.create_group(f"measurementList15")
        measurementlist15.create_dataset("dataType", data=np.array([1]))
        measurementlist15.create_dataset("dataTypeIndex", data=np.array([1]))
        measurementlist15.create_dataset("detectorIndex", data=np.array([3]))
        measurementlist15.create_dataset("sourceIndex", data=np.array([1]))
        measurementlist15.create_dataset("wavelengthIndex", data=np.array([3]))

        measurementlist16 = nirs_group.create_group(f"measurementList16")
        measurementlist16.create_dataset("dataType", data=np.array([1]))
        measurementlist16.create_dataset("dataTypeIndex", data=np.array([1]))
        measurementlist16.create_dataset("detectorIndex", data=np.array([1]))
        measurementlist16.create_dataset("sourceIndex", data=np.array([2]))
        measurementlist16.create_dataset("wavelengthIndex", data=np.array([3]))
        
        measurementlist17 = nirs_group.create_group(f"measurementList17")
        measurementlist17.create_dataset("dataType", data=np.array([1]))
        measurementlist17.create_dataset("dataTypeIndex", data=np.array([1]))
        measurementlist17.create_dataset("detectorIndex", data=np.array([2]))
        measurementlist17.create_dataset("sourceIndex", data=np.array([2]))
        measurementlist17.create_dataset("wavelengthIndex", data=np.array([3]))

        measurementlist18 = nirs_group.create_group(f"measurementList18")
        measurementlist18.create_dataset("dataType", data=np.array([1]))
        measurementlist18.create_dataset("dataTypeIndex", data=np.array([1]))
        measurementlist18.create_dataset("detectorIndex", data=np.array([3]))
        measurementlist18.create_dataset("sourceIndex", data=np.array([2]))
        measurementlist18.create_dataset("wavelengthIndex", data=np.array([3]))
        
        measurementlist19 = nirs_group.create_group(f"measurementList19")
        measurementlist19.create_dataset("dataType", data=np.array([1]))
        measurementlist19.create_dataset("dataTypeIndex", data=np.array([1]))
        measurementlist19.create_dataset("detectorIndex", data=np.array([1]))
        measurementlist19.create_dataset("sourceIndex", data=np.array([1]))
        measurementlist19.create_dataset("wavelengthIndex", data=np.array([4]))

        measurementlist20 = nirs_group.create_group(f"measurementList20")
        measurementlist20.create_dataset("dataType", data=np.array([1]))
        measurementlist20.create_dataset("dataTypeIndex", data=np.array([1]))
        measurementlist20.create_dataset("detectorIndex", data=np.array([2]))
        measurementlist20.create_dataset("sourceIndex", data=np.array([1]))
        measurementlist20.create_dataset("wavelengthIndex", data=np.array([4]))

        measurementlist21 = nirs_group.create_group(f"measurementList21")
        measurementlist21.create_dataset("dataType", data=np.array([1]))
        measurementlist21.create_dataset("dataTypeIndex", data=np.array([1]))
        measurementlist21.create_dataset("detectorIndex", data=np.array([3]))
        measurementlist21.create_dataset("sourceIndex", data=np.array([1]))
        measurementlist21.create_dataset("wavelengthIndex", data=np.array([4]))

        measurementlist22 = nirs_group.create_group(f"measurementList22")
        measurementlist22.create_dataset("dataType", data=np.array([1]))
        measurementlist22.create_dataset("dataTypeIndex", data=np.array([1]))
        measurementlist22.create_dataset("detectorIndex", data=np.array([1]))
        measurementlist22.create_dataset("sourceIndex", data=np.array([2]))
        measurementlist22.create_dataset("wavelengthIndex", data=np.array([4]))

        measurementlist23 = nirs_group.create_group(f"measurementList23")
        measurementlist23.create_dataset("dataType", data=np.array([1]))
        measurementlist23.create_dataset("dataTypeIndex", data=np.array([1]))
        measurementlist23.create_dataset("detectorIndex", data=np.array([2]))
        measurementlist23.create_dataset("sourceIndex", data=np.array([2]))
        measurementlist23.create_dataset("wavelengthIndex", data=np.array([4]))

        measurementlist24 = nirs_group.create_group(f"measurementList24")
        measurementlist24.create_dataset("dataType", data=np.array([1]))
        measurementlist24.create_dataset("dataTypeIndex", data=np.array([1]))
        measurementlist24.create_dataset("detectorIndex", data=np.array([3]))
        measurementlist24.create_dataset("sourceIndex", data=np.array([2]))
        measurementlist24.create_dataset("wavelengthIndex", data=np.array([4]))

        measurementlist25 = nirs_group.create_group(f"measurementList25")
        measurementlist25.create_dataset("dataType", data=np.array([1]))
        measurementlist25.create_dataset("dataTypeIndex", data=np.array([1]))
        measurementlist25.create_dataset("detectorIndex", data=np.array([1]))
        measurementlist25.create_dataset("sourceIndex", data=np.array([1]))
        measurementlist25.create_dataset("wavelengthIndex", data=np.array([5]))

        measurementlist26 = nirs_group.create_group(f"measurementList26")
        measurementlist26.create_dataset("dataType", data=np.array([1]))
        measurementlist26.create_dataset("dataTypeIndex", data=np.array([1]))
        measurementlist26.create_dataset("detectorIndex", data=np.array([2]))
        measurementlist26.create_dataset("sourceIndex", data=np.array([1]))
        measurementlist26.create_dataset("wavelengthIndex", data=np.array([5]))


        measurementlist27 = nirs_group.create_group(f"measurementList27")
        measurementlist27.create_dataset("dataType", data=np.array([1]))
        measurementlist27.create_dataset("dataTypeIndex", data=np.array([1]))
        measurementlist27.create_dataset("detectorIndex", data=np.array([3]))
        measurementlist27.create_dataset("sourceIndex", data=np.array([1]))
        measurementlist27.create_dataset("wavelengthIndex", data=np.array([5]))

        measurementlist28 = nirs_group.create_group(f"measurementList28")
        measurementlist28.create_dataset("dataType", data=np.array([1]))
        measurementlist28.create_dataset("dataTypeIndex", data=np.array([1]))
        measurementlist28.create_dataset("detectorIndex", data=np.array([1]))
        measurementlist28.create_dataset("sourceIndex", data=np.array([2]))
        measurementlist28.create_dataset("wavelengthIndex", data=np.array([5]))

        measurementlist29 = nirs_group.create_group(f"measurementList29")
        measurementlist29.create_dataset("dataType", data=np.array([1]))
        measurementlist29.create_dataset("dataTypeIndex", data=np.array([1]))
        measurementlist29.create_dataset("detectorIndex", data=np.array([2]))
        measurementlist29.create_dataset("sourceIndex", data=np.array([2]))
        measurementlist29.create_dataset("wavelengthIndex", data=np.array([5]))

        measurementlist30 = nirs_group.create_group(f"measurementList30")
        measurementlist30.create_dataset("dataType", data=np.array([1]))
        measurementlist30.create_dataset("dataTypeIndex", data=np.array([1]))
        measurementlist30.create_dataset("detectorIndex", data=np.array([3]))
        measurementlist30.create_dataset("sourceIndex", data=np.array([2]))
        measurementlist30.create_dataset("wavelengthIndex", data=np.array([5]))

        measurementlist31 = nirs_group.create_group(f"measurementList31")
        measurementlist31.create_dataset("dataType", data=np.array([1]))
        measurementlist31.create_dataset("dataTypeIndex", data=np.array([1]))
        measurementlist31.create_dataset("detectorIndex", data=np.array([1]))
        measurementlist31.create_dataset("sourceIndex", data=np.array([1]))
        measurementlist31.create_dataset("wavelengthIndex", data=np.array([6]))

        measurementlist32 = nirs_group.create_group(f"measurementList32")
        measurementlist32.create_dataset("dataType", data=np.array([1]))
        measurementlist32.create_dataset("dataTypeIndex", data=np.array([1]))
        measurementlist32.create_dataset("detectorIndex", data=np.array([2]))
        measurementlist32.create_dataset("sourceIndex", data=np.array([1]))
        measurementlist32.create_dataset("wavelengthIndex", data=np.array([6]))

        measurementlist33 = nirs_group.create_group(f"measurementList33")
        measurementlist33.create_dataset("dataType", data=np.array([1]))
        measurementlist33.create_dataset("dataTypeIndex", data=np.array([1]))
        measurementlist33.create_dataset("detectorIndex", data=np.array([3]))
        measurementlist33.create_dataset("sourceIndex", data=np.array([1]))
        measurementlist33.create_dataset("wavelengthIndex", data=np.array([6]))

        measurementlist34 = nirs_group.create_group(f"measurementList34")
        measurementlist34.create_dataset("dataType", data=np.array([1]))
        measurementlist34.create_dataset("dataTypeIndex", data=np.array([1]))
        measurementlist34.create_dataset("detectorIndex", data=np.array([1]))
        measurementlist34.create_dataset("sourceIndex", data=np.array([2]))
        measurementlist34.create_dataset("wavelengthIndex", data=np.array([6]))

        measurementlist35 = nirs_group.create_group(f"measurementList35")
        measurementlist35.create_dataset("dataType", data=np.array([1]))
        measurementlist35.create_dataset("dataTypeIndex", data=np.array([1]))
        measurementlist35.create_dataset("detectorIndex", data=np.array([2]))
        measurementlist35.create_dataset("sourceIndex", data=np.array([2]))
        measurementlist35.create_dataset("wavelengthIndex", data=np.array([6]))

        measurementlist36 = nirs_group.create_group(f"measurementList36")
        measurementlist36.create_dataset("dataType", data=np.array([1]))
        measurementlist36.create_dataset("dataTypeIndex", data=np.array([1]))
        measurementlist36.create_dataset("detectorIndex", data=np.array([3]))
        measurementlist36.create_dataset("sourceIndex", data=np.array([2]))
        measurementlist36.create_dataset("wavelengthIndex", data=np.array([6]))


        ###############  Dark  #########################
        measurementlist37 = nirs_group.create_group(f"measurementList37")
        measurementlist37.create_dataset("dataType", data=np.array([1]))
        measurementlist37.create_dataset("dataTypeIndex", data=np.array([1]))
        measurementlist37.create_dataset("detectorIndex", data=np.array([1]))
        measurementlist37.create_dataset("sourceIndex", data=np.array([1]))
        measurementlist37.create_dataset("wavelengthIndex", data=np.array([0]))

        measurementlist38 = nirs_group.create_group(f"measurementList38")
        measurementlist38.create_dataset("dataType", data=np.array([1]))
        measurementlist38.create_dataset("dataTypeIndex", data=np.array([1]))
        measurementlist38.create_dataset("detectorIndex", data=np.array([2]))
        measurementlist38.create_dataset("sourceIndex", data=np.array([1]))
        measurementlist38.create_dataset("wavelengthIndex", data=np.array([0]))

        measurementlist39 = nirs_group.create_group(f"measurementList39")
        measurementlist39.create_dataset("dataType", data=np.array([1]))
        measurementlist39.create_dataset("dataTypeIndex", data=np.array([1]))
        measurementlist39.create_dataset("detectorIndex", data=np.array([3]))
        measurementlist39.create_dataset("sourceIndex", data=np.array([1]))
        measurementlist39.create_dataset("wavelengthIndex", data=np.array([0]))

        measurementlist40 = nirs_group.create_group(f"measurementList40")
        measurementlist40.create_dataset("dataType", data=np.array([1]))
        measurementlist40.create_dataset("dataTypeIndex", data=np.array([1]))
        measurementlist40.create_dataset("detectorIndex", data=np.array([1]))
        measurementlist40.create_dataset("sourceIndex", data=np.array([2]))
        measurementlist40.create_dataset("wavelengthIndex", data=np.array([0]))

        measurementlist41 = nirs_group.create_group(f"measurementList41")
        measurementlist41.create_dataset("dataType", data=np.array([1]))
        measurementlist41.create_dataset("dataTypeIndex", data=np.array([1]))
        measurementlist41.create_dataset("detectorIndex", data=np.array([2]))
        measurementlist41.create_dataset("sourceIndex", data=np.array([2]))
        measurementlist41.create_dataset("wavelengthIndex", data=np.array([0]))

        measurementlist42 = nirs_group.create_group(f"measurementList42")
        measurementlist42.create_dataset("dataType", data=np.array([1]))
        measurementlist42.create_dataset("dataTypeIndex", data=np.array([1]))
        measurementlist42.create_dataset("detectorIndex", data=np.array([3]))
        measurementlist42.create_dataset("sourceIndex", data=np.array([2]))
        measurementlist42.create_dataset("wavelengthIndex", data=np.array([0]))

        meta_group = f.create_group("/nirs/metaDataTags")
        meta_group.create_dataset("HardwareVersion", data=Hardware_Version)
        meta_group.create_dataset("FirmwareVersion", data=Firmware_Version)
        meta_group.create_dataset("NIR_LED_EmitterCurrent", data=NIR_LED_Emitter_Current)
        meta_group.create_dataset("ADC_Gain", data=ADC_Gain)
        meta_group.create_dataset("MeasurementDate", data=date_part_from_filename)
        meta_group.create_dataset("MeasurementTime", data=time_part_from_filename)
        meta_group.create_dataset("VoltageUnit", data='V')
        meta_group.create_dataset("TimeUnit", data='s')  # seconds for time
        meta_group.create_dataset("FrequencyUnit", data='Hz')
        meta_group.create_dataset("dataTimeSeries_Column_names", data=data_new_columns_name)
        meta_group.create_dataset("detectorSource_distance", data=detector_source_distance_data)
        meta_group.create_dataset("detectorSource_distance_unit", data=np.array(['cm'], dtype='S2'))
        

        probe_group = f.create_group("/nirs/probe")
        probe_group.create_dataset("detectorLabels", data=np.array(['DET1', 'DET2', 'DET3'], dtype='S'))
        probe_group.create_dataset("detectorPos3D", data=detpos)
        probe_group.create_dataset("sourceLabels", data=np.array(['LED_A', 'LED_B'], dtype='S'))
        probe_group.create_dataset("sourcePos2D", data=sorpos)
        probe_group.create_dataset("wavelengths", data=wavelen)
    
    

    print(f"SNIRF file created: {snirf_file}")
    return snirf_file, snirf_file_name


# File path to the Excel file
#file_path = '/home/darshana/Documents/Code/create_snirf_file_for_FSM V2/metadata_files/PHANTOM_fsm_data_20241126_151441.xlsx'
# Call the update_data function with the file path
#snirf_file = update_data(file_path)
# Print the resulting SNIRF file path
#print(f'SNIRF file created at: {snirf_file}')