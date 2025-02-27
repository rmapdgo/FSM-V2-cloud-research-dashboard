voltages, Time, GroupA_Detector1, GroupA_Detector2, GroupA_Detector3, GroupB_Detector1, GroupB_Detector2, GroupB_Detector3 = read_group_data(filepath)
        
# Define the function to calculate SNR
def calculate_snr(signal_data, dark_data):
    signal = np.mean(signal_data)
    dark_mean = np.mean(dark_data)
    noise = np.std(dark_data)
    snr = (signal - dark_mean) / noise
    return snr

# Initialize an empty dictionary to store the SNR values
snr_dict = {}

# Define the signal-dark dictionary (as you provided)
signal_dark_dictionary = {
    'LED_A_784_DET1':'LED_A_DARK_DET1', 'LED_A_800_DET1':'LED_A_DARK_DET1', 'LED_A_818_DET1':'LED_A_DARK_DET1', 'LED_A_835_DET1':'LED_A_DARK_DET1', 'LED_A_851_DET1':'LED_A_DARK_DET1', 'LED_A_881_DET1':'LED_A_DARK_DET1',
    'LED_A_784_DET2':'LED_A_DARK_DET2', 'LED_A_800_DET2':'LED_A_DARK_DET2', 'LED_A_818_DET2':'LED_A_DARK_DET2', 'LED_A_835_DET2':'LED_A_DARK_DET2', 'LED_A_851_DET2':'LED_A_DARK_DET2', 'LED_A_881_DET2':'LED_A_DARK_DET2',
    'LED_A_784_DET3':'LED_A_DARK_DET3', 'LED_A_800_DET3':'LED_A_DARK_DET3', 'LED_A_818_DET3':'LED_A_DARK_DET3', 'LED_A_835_DET3':'LED_A_DARK_DET3', 'LED_A_851_DET3':'LED_A_DARK_DET3', 'LED_A_881_DET3':'LED_A_DARK_DET3',
    'LED_B_784_DET1':'LED_B_DARK_DET1', 'LED_B_800_DET1':'LED_B_DARK_DET1', 'LED_B_818_DET1':'LED_B_DARK_DET1', 'LED_B_835_DET1':'LED_B_DARK_DET1', 'LED_B_851_DET1':'LED_B_DARK_DET1', 'LED_B_881_DET1':'LED_B_DARK_DET1',
    'LED_B_784_DET2':'LED_B_DARK_DET2', 'LED_B_800_DET2':'LED_B_DARK_DET2', 'LED_B_818_DET2':'LED_B_DARK_DET2', 'LED_B_835_DET2':'LED_B_DARK_DET2', 'LED_B_851_DET2':'LED_B_DARK_DET2', 'LED_B_881_DET2':'LED_B_DARK_DET2',
    'LED_B_784_DET3':'LED_B_DARK_DET3', 'LED_B_800_DET3':'LED_B_DARK_DET3', 'LED_B_818_DET3':'LED_B_DARK_DET3', 'LED_B_835_DET3':'LED_B_DARK_DET3', 'LED_B_851_DET3':'LED_B_DARK_DET3', 'LED_B_881_DET3':'LED_B_DARK_DET3'
}

# Loop over each entry in the signal-dark dictionary and calculate SNR for each pair
for signal_col in signal_dark_dictionary:
    dark_col = signal_dark_dictionary[signal_col]
    snr_value = calculate_snr(voltages[signal_col], voltages[dark_col])
    
    # Store the SNR value in the snr_dict dictionary with the column name as key
    snr_dict[signal_col] = snr_value

# The resulting snr_dict contains column names as keys and corresponding SNR values as values
print(snr_dict)


# Group all the groups together for easier iteration
groups = {
    "GroupA_Detector1": GroupA_Detector1,
    "GroupA_Detector2": GroupA_Detector2,
    "GroupA_Detector3": GroupA_Detector3,
    "GroupB_Detector1": GroupB_Detector1,
    "GroupB_Detector2": GroupB_Detector2,
    "GroupB_Detector3": GroupB_Detector3
}

# Initialize a dictionary to store the average SNR for each group
group_snr = {}

# Iterate over each group and calculate the average SNR
for group_name, group in groups.items():
    snr_values = []
    
    # Iterate over each detector pair in the group
    for i in range(0, len(group) - 1, 2):  # Step by 2 to get the signal and dark pair
        signal_col = group[i]
        dark_col = group[i + 1]
        snr_value = calculate_snr(data[signal_col], data[dark_col])
        snr_values.append(snr_value)
    
    # Calculate the average SNR for the group
    average_snr = np.mean(snr_values)
    
    # Store the average SNR in the group_snr dictionary
    group_snr[group_name] = average_snr

# The resulting group_snr dictionary contains the average SNR for each group
print(group_snr)

# Histogram Plot for SNR of all columns
def plot_snr_histogram(snr_dict):
    plt.figure(figsize=(10, 6))
    plt.hist(list(snr_dict.values()), bins=20, edgecolor='black', color='skyblue')
    plt.title('Histogram of SNR for All Columns')
    plt.xlabel('SNR')
    plt.ylabel('Frequency')
    plt.grid(True)
    plt.show()

# 1. Plot Histogram for SNR values
def plot_snr_histogram(snr_dict):
    plt.figure(figsize=(14, 8))
    plt.bar(snr_dict.keys(), snr_dict.values(), color='skyblue')
    
    plt.title('Histogram of SNR for All Columns')
    plt.xlabel('Columns')
    plt.ylabel('SNR')
    plt.xticks(rotation=90)  # Rotate x-axis labels to prevent overlap
    plt.grid(True)
    plt.tight_layout()
    plt.show()

def plot_snr_gauge(group_snr):
    # Create a Plotly figure with 6 indicators
    fig = go.Figure()

    # Define the colors and labels for each group
    colors = {
        'Good': 'green',
        'Moderate': 'blue',
        'Poor': 'red'
    }

    # Iterate over groups to add indicators
    for idx, (group_name, avg_snr) in enumerate(group_snr.items()):
        # Assign color based on the SNR value
        if avg_snr >= 5:
            color = colors['Good']
        elif 1 <= avg_snr < 5:
            color = colors['Moderate']
        else:
            color = colors['Poor']

        # Add the indicator for the current group
        fig.add_trace(go.Indicator(
            mode="gauge+number+delta",
            value=avg_snr,
            title={'text': group_name},
            domain={'x': [0.1, 0.9], 'y': [1 - (idx + 1) * 0.15, 1 - idx * 0.15]},  # Adjust y-domain to stay within range [0, 1]
            gauge={
                'axis': {'range': [None, 10]},
                'steps': [
                    {'range': [0, 1], 'color': 'red'},
                    {'range': [1, 5], 'color': 'blue'},
                    {'range': [5, 10], 'color': 'green'}
                ],
                'threshold': {
                    'line': {'color': "black", 'width': 4},
                    'thickness': 0.75,
                    'value': avg_snr
                }
            }
        ))

    fig.update_layout(
        title="Average SNR for Each Group",
        template="plotly_dark",
        height=2000)
    
    fig.show()

    