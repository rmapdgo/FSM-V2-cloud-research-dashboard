import dash
from dash import Dash, dcc, html, Input, Output, State, callback
import os
import pandas as pd
import base64
import io
import openpyxl
import dash_daq as daq
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import glob
from snirf.create_snirf import create_snirf
import numpy as np
import plotly.graph_objects as go


# Create the Dash app
app = dash.Dash(__name__, suppress_callback_exceptions=True)
server = app.server

app.layout = html.Div([
    # Header Section
    html.Div(
        style={
            'height': '40px',
            'padding': '15px',
            'background': '#ed6a28',
            'color': 'white',
            'display': 'flex',
            'alignItems': 'center',
            'justifyContent': 'center',
            'fontSize': '30px',
            'fontWeight': '100',
            'boxShadow': '0 4px 8px rgba(0, 0, 0, 0.2)',
            'borderBottom': '5px solid #ed6a28'
        },
        children=[
            html.H1(
                'FetalsenseM 1.5 Dashboard',
                style={'margin': '0', 'margin-left': '10px'}
            )
        ]
    ),
    html.Br(),
    # Flex container for the left and right sections
    html.Div([
        # Left side (1/4th width)
        html.Div([
            # Tabs for General, Data Clean, Data Analysis, and Concentrations
            dcc.Tabs(id='left-tabs', children=[
                dcc.Tab(label='General', children=[
                    # File Upload Section inside the General tab
                    html.Div([
                        html.Div([
                            html.H3('File Upload', style={
                                'background': '#ed6a28',
                                'padding': '15px',
                                'textAlign': 'center',
                                'color': 'white',
                                'fontWeight': 'bold',
                                'fontSize': '48px'
                            }),
                            dcc.Upload(
                                id='upload-data',
                                children=html.Div(['Drag and Drop or ', html.A('Select Files')]),
                                style={'width': '95%', 'height': '70px', 'lineHeight': '70px',
                                       'borderWidth': '1px', 'borderStyle': 'dashed', 'borderRadius': '5px',
                                       'textAlign': 'center', 'margin': '15px', 'fontSize': '24px'},
                                multiple=False,
                            ),
                        ]),
                        html.Div(id='file-names'),
                        dcc.Store(id='store-file-path'),
                        html.Br(),
                        html.Div([
                            html.H3('Download SNIRF', style={
                                'background': '#ed6a28',
                                'padding': '15px',
                                'textAlign': 'center',
                                'color': 'white',
                                'fontWeight': 'bold',
                                'fontSize': '48px'
                            }),
                            html.Button("Download Raw Data SNIRF", id="btn_rawdata_snirf", style={
                                'width': '95%', 'height': '70px', 'lineHeight': '70px',
                                'borderWidth': '1px', 'borderStyle': 'dashed', 'borderRadius': '5px',
                                'textAlign': 'center', 'margin': '15px', 'fontSize': '24px'}),
                            dcc.Download(id="download-file-snirf"),
                        ]),
                        html.Br(),
                        html.Div([
                            html.H3('Resampling Options', style={
                                'textAlign': 'center', 'fontSize': '40px', 'color': '#003f5c'}),
                            dcc.RadioItems(
                                id='resample-option',
                                options=[
                                    {'label': '1Hz Averaging', 'value': 'average'},
                                    {'label': '1Hz Accumulation', 'value': 'accumulation'}
                                ],
                                value=None,  # Default value
                                labelStyle={'display': 'block', 'fontSize': '40px', 'color': '#003f5c'}
                            ),
                        ], style={'textAlign': 'center', 'marginBottom': '20px'}),
                        html.Br(),
                        html.Div([
                            html.H3('View Intensities', style={
                                'background': '#ed6a28',
                                'padding': '15px',
                                'textAlign': 'center',
                                'color': 'white',
                                'fontWeight': 'bold',
                                'fontSize': '48px'
                            }),
                            html.Div([
                                html.H4('Select one or more:', style={
                                    'textAlign': 'left',
                                    'fontSize': '30px',
                                    'marginBottom': '15px',
                                    'color': '#ed6a28',
                                    "font-weight": "100"
                                }),
                                dcc.Dropdown(
                                    id='intensities-options-dropdown',
                                    options=[{'label': option, 'value': option} for option in [
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
                                        'LED_B_DARK_DET1', 'LED_B_DARK_DET2', 'LED_B_DARK_DET3'
                                    ]],
                                    multi=True,
                                    value=[],
                                    style={'borderColor': '#ed6a28', 'fontSize': '24px'}
                                )
                            ]),
                            html.Div(id='intensity-selection-status', children='Select to view', style={
                                'fontFamily': 'Courier New',
                                'fontSize': '20px',
                                'textAlign': 'center',
                                'marginTop': '15px',
                                'color': '#2B2D42'
                            }),
                            html.Br(),
                            html.Div([
                                html.H4('Select Groups', style={
                                    'textAlign': 'left',
                                    'fontSize': '30px',
                                    'marginBottom': '15px',
                                    'color': '#ed6a28',
                                    "font-weight": "100"
                                }),
                                # Group A and Group B selectors placed side by side using flexbox
                                html.Div([
                                    html.Div([
                                        html.H4('GroupA_Detector1', style={'fontSize': '20px', 'color': '#003f5c', "font-weight": "100"}),
                                        daq.BooleanSwitch(
                                            id='groupA_dect1_spectras',
                                            on=False,
                                            style={'transform': 'scale(1.1)'}
                                        )
                                    ], style={'display': 'flex', 'alignItems': 'center', 'flex': '1', 'marginRight': '10px'}),
                                    
                                    html.Div([
                                        html.H4('GroupB_Detector1', style={'fontSize': '20px', 'color': '#003f5c', "font-weight": "100"}),
                                        daq.BooleanSwitch(
                                            id='groupB_dect1_spectras',
                                            on=False,
                                            style={'transform': 'scale(1.1)'}
                                        )
                                    ], style={'display': 'flex', 'alignItems': 'center', 'flex': '1', 'marginLeft': '10px'})
                                ], style={'display': 'flex', 'marginBottom': '10px'}),  # Flexbox for side-by-side
                                # Similarly for other detectors...
                                html.Div([
                                    html.Div([
                                        html.H4('GroupA_Detector2', style={'fontSize': '20px', 'color': '#003f5c', "font-weight": "100"}),
                                        daq.BooleanSwitch(
                                            id='groupA_dect2_spectras',
                                            on=False,
                                            style={'transform': 'scale(1.1)'}
                                        )
                                    ], style={'display': 'flex', 'alignItems': 'center', 'flex': '1', 'marginRight': '10px'}),
                                    
                                    html.Div([
                                        html.H4('GroupB_Detector2', style={'fontSize': '20px', 'color': '#003f5c', "font-weight": "100"}),
                                        daq.BooleanSwitch(
                                            id='groupB_dect2_spectras',
                                            on=False,
                                            style={'transform': 'scale(1.1)'}
                                        )
                                    ], style={'display': 'flex', 'alignItems': 'center', 'flex': '1', 'marginLeft': '10px'})
                                ], style={'display': 'flex', 'marginBottom': '10px'}),
                                # And similarly for GroupA/GroupB Detector 3...
                                html.Div([
                                    html.H4('Select All', style={'fontSize': '20px', 'color': '#cc4c0c', "font-weight": "100"}),
                                    daq.BooleanSwitch(
                                        id='select_all_switch',
                                        on=False,
                                        style={'transform': 'scale(1.1)', 'padding': '10px'}
                                    )
                                ], style={'display': 'flex', 'alignItems': 'center', 'marginBottom': '10px'}),
                            ]),
                            dbc.Button('View Intensity Over Time ', id='view-graph-btn', color='primary', style={
                                'padding': '15px', 'width': '100%', 'margin': '15px 0', 'fontSize': '22px'}),
                            html.Div(id='select-intensities', children='Select one or multiple groups', style={
                                'fontFamily': 'Courier New',
                                'fontSize': '20px',
                                'textAlign': 'center',
                                'marginTop': '15px',
                                'color': '#2B2D42'
                            }),
                            html.Br(),
                            html.Div(children=[
                                html.H3('Raw Data Quality Check', style={
                                    'background': '#ed6a28',
                                    'padding': '15px',
                                    'textAlign': 'center',
                                    'color': 'white',
                                    'fontWeight': 'bold',
                                    'fontSize': '48px',
                                }),
                                # Alert and button styles updated for clearer and larger font
                                dbc.Alert(
                                    html.Div([
                                        html.H4('Signal Noise Ratio', style={'color': '#ed6a28', 'marginLeft': '40px', 'textAlign': 'left', 'fontSize': '28px', 'fontWeight': 'lighter'}),
                                        html.Button('×', id='close-snr-alert', n_clicks=0, style={'background': 'none', 'border': 'none', 'color': 'black', 'fontSize': '28px', 'cursor': 'pointer', 'float': 'right', 'color': '#ed6a28'})
                                    ]),
                                    id='snr-alert',
                                    is_open=True,
                                    dismissable=True,
                                    style={'marginTop': '15px', 'boxShadow': '0 4px 6px rgba(0, 0, 0, 0.1)'}
                                ),
                                dbc.Button('Check Raw Data Quality', id='check-data-quality-btn', color='primary', style={
                                    'padding': '15px', 'width': '100%', 'margin': '15px 0', 'fontSize': '22px'}),
                                html.Div(id='check-raw-data-quality-desc', children='Check data quality', style={
                                    'fontFamily': 'Courier New',
                                    'fontSize': '20px',
                                    'textAlign': 'center',
                                    'marginTop': '15px',
                                    'color': '#2B2D42'
                                })
                            ]),
                        ]),
                    ]),
                ]),
                # Data Clean Tab
                dcc.Tab(label='Data Clean', children=[
                    html.Div([
                        html.H3('Data Cleaning', style={
                            'background': '#ed6a28',
                            'padding': '12px',
                            'textAlign': 'center',
                            'color': '#ECF0F1',
                            'fontWeight': 'bold',
                            'fontSize': '38px',
                            'borderRadius': '8px',
                        }),
                        html.P("This tab will contain data cleaning functionalities."),
                        html.Br(),
                        html.Div(
                                            style={
                                                'background': '#ffffff',
                                                'padding': '20px',
                                                'boxShadow': '0 4px 10px rgba(0, 0, 0, 0.5)',
                                                'marginBottom': '20px'
                                            },
                                            children=[
                                                html.Br(),
                                                # Subtract Dark Section
                html.Br(),
                html.Div('Subtract Dark', style={
                    'background': '#003f5c',
                    'padding': '10px',
                    'textAlign': 'center',
                    'color': 'white',
                    'fontWeight': 'bold',
                    'fontSize': '30px'
                }),
                html.Br(),
                html.Div(
                    children=[
                        dcc.Checklist(
                            id='preprocessing-options-subtract-dark',
                            options=[{'label': 'Subtract Dark', 'value': 'subtract-dark'}],
                            style={'textAlign': 'Center', 'fontSize': '28px', 'marginBottom': '10px', 'color': '#003f5c'},
                            inputStyle={'transform': 'scale(1.5)', 'marginRight': '10px'}
                        ),
                        html.Div('Subtract Noise', style={'fontFamily': 'Courier New', 'fontSize': '16px', 'textAlign': 'center', 'color': '#2B2D42'}),
                        html.Br()
                    ]
                ),
                html.Br(),
                        html.Br(),
                                                html.Div('Median Filtering', style={
                                                    'background': '#003f5c',
                                                    'padding': '10px',
                                                    'textAlign': 'center',
                                                    'color': 'white',
                                                    'fontWeight': 'bold',
                                                    'fontSize': '30px'
                                                }),
                                                html.Br(),
                                                html.Div(
                                                    children=[
                                                        dcc.Checklist(
                                                            id='preprocessing-options-median',
                                                            options=[
                                                                {'label': 'Median Filtering', 'value': 'median'},
                                                            ],
                                                            className='alignment-settings-section',
                                                            style={
                                                                'textAlign': 'Center',
                                                                'fontSize': '28px',
                                                                'marginBottom': '10px',
                                                                'color': '#003f5c',
                                                                "font-weight": "100",
                                                                'alignItems': 'center'
                                                            },
                                                            inputStyle={
                                                                'transform': 'scale(1.5)',  # Adjust this value to make the checkbox larger or smaller
                                                                'marginRight': '10px',  # Optional: add space between the checkbox and the label
                                                            }
                                                        ),
                                                        html.Br(),
                                                        html.Div(
                                                            style={'display': 'flex', 'alignItems': 'center', 'justifyContent': 'space-between'},
                                                            children=[
                                                                html.Div(
                                                                    className='app-controls-name',
                                                                    children='Filter Size',
                                                                    style={
                                                                        'textAlign': 'left',
                                                                        'fontSize': '26px',
                                                                        'marginBottom': '10px',
                                                                        'color': '#003f5c',
                                                                        "font-weight": "100",
                                                                        'marginLeft': '30px'
                                                                    }
                                                                ),
                                                                dcc.Input(
                                                    id='median-filter-size-input',
                                                    type='number',
                                                    min=1,
                                                    max=100,
                                                    step=1,
                                                    value=1,
                                                    style={
                                                        'width': '30%',
                                                        'padding': '5px',
                                                        'height': '24px',  # Increased height to fit the larger font
                                                        'textAlign': 'center',
                                                        'borderColor': '#003f5c',
                                                        'marginRight': '30px',
                                                        'fontSize': '24px'  # Increased font size for the number
                                                        }
                                                        )]
                                                        ),
                                                        html.Div(
                                                            children='Set Filter Size for Median Filtering',
                                                            style={
                                                                'fontFamily': 'Courier New',
                                                                'fontSize': '16px',
                                                                'textAlign': 'center',
                                                                'marginTop': '10px',
                                                                'color': '#2B2D42'
                                                            }
                                                        ),
                                                        html.Br(),
                    ]),
                ]),
                ]),
                ]),
                # Data Analysis Tab
                dcc.Tab(label='Data Analysis', children=[
                    html.Div([
                        html.H3('Data Analysis', style={
                            'background': '#ed6a28',
                            'padding': '12px',
                            'textAlign': 'center',
                            'color': '#ECF0F1',
                            'fontWeight': 'bold',
                            'fontSize': '38px',
                            'borderRadius': '8px',
                        }),
                        html.P("This tab will contain data analysis functionalities."),
                    ]),
                ]),
                # Concentrations Tab
                dcc.Tab(label='Concentrations', children=[
                    html.Div([
                        html.H3('Concentrations', style={
                            'background': '#ed6a28',
                            'padding': '12px',
                            'textAlign': 'center',
                            'color': '#ECF0F1',
                            'fontWeight': 'bold',
                            'fontSize': '38px',
                            'borderRadius': '8px',
                        }),
                        html.P("This tab will display concentration-related data."),
                    ]),
                ]),
            ])
        ], style={'width': '25%', 'padding': '15px', 'boxSizing': 'border-box'}),

        # Right side (3/4th width for Plot Section)
        html.Div([
            html.H3('Plot Section', style={
                'background': '#ed6a28',
                'padding': '12px',
                'textAlign': 'center',
                'color': '#ECF0F1',
                'fontWeight': 'bold',
                'fontSize': '38px',
                'borderRadius': '8px',
            }),
            dcc.Tabs(id='tabs', children=[
                dcc.Tab(label='Intensity vs Time', children=[
                    html.Div(id='intensity-time-plot'),
                ]),
            ]),
        ], style={'width': '75%', 'padding': '10px', 'boxSizing': 'border-box', 'borderLeft': '2px solid #3498DB'})
    ], style={'display': 'flex', 'height': '100vh'}),
])

import os

# Define the output directory
output_dir = '/home/darshana/Documents/Code/FSM-V2/src/output_files/'

# Create the directory if it doesn't exist
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

def read_group_data(filepath):
    try:
        # Use pandas to read the Excel file
        data = pd.read_excel(filepath, engine="openpyxl")
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
        Time = data['Time']
        
        # Group mappings
        GroupA_Detector1 = ['LED_A_784_DET1', 'LED_A_800_DET1', 'LED_A_818_DET1', 'LED_A_835_DET1', 'LED_A_851_DET1', 'LED_A_881_DET1', 'LED_A_DARK_DET1']
        GroupA_Detector2 = ['LED_A_784_DET2', 'LED_A_800_DET2', 'LED_A_818_DET2', 'LED_A_835_DET2', 'LED_A_851_DET2', 'LED_A_881_DET2', 'LED_A_DARK_DET2']
        GroupA_Detector3 = ['LED_A_784_DET3', 'LED_A_800_DET3', 'LED_A_818_DET3', 'LED_A_835_DET3', 'LED_A_851_DET3', 'LED_A_881_DET3', 'LED_A_DARK_DET3']
    
        GroupB_Detector1 = ['LED_B_784_DET1', 'LED_B_800_DET1', 'LED_B_818_DET1', 'LED_B_835_DET1', 'LED_B_851_DET1', 'LED_B_881_DET1', 'LED_B_DARK_DET1']
        GroupB_Detector2 = ['LED_B_784_DET2', 'LED_B_800_DET2', 'LED_B_818_DET2', 'LED_B_835_DET2', 'LED_B_851_DET2', 'LED_B_881_DET2', 'LED_B_DARK_DET2']
        GroupB_Detector3 = ['LED_B_784_DET3', 'LED_B_800_DET3', 'LED_B_818_DET3', 'LED_B_835_DET3', 'LED_B_851_DET3', 'LED_B_881_DET3', 'LED_B_DARK_DET3']
    
        return data, Time, GroupA_Detector1, GroupA_Detector2, GroupA_Detector3, GroupB_Detector1, GroupB_Detector2, GroupB_Detector3
    except Exception as e:
        print(f"Error reading the file: {e}")
        return None, None, None, None, None, None, None, None

def resample_data(df, option):
    if option == 'average':
        resampled_df = df.resample('1S', on='Time').mean().reset_index()
    elif option == 'accumulation':
        resampled_df = df.resample('1S', on='Time').sum().reset_index()

    # Convert Time from milliseconds to seconds (resample already adjusts)
    resampled_df['Time'] = (resampled_df['Time'] - resampled_df['Time'].min()).dt.total_seconds()
    print('resampled_df[Time]', resampled_df['Time'])
    return resampled_df



import pandas as pd
import os

@callback(
    [Output('store-file-path', 'data'),
     Output('file-names', 'children')],
    [Input('upload-data', 'filename'),
     Input('upload-data', 'contents'),
     Input('resample-option', 'value')],
    prevent_initial_call=True
)
def upload_and_resample_data(filename, contents, selected_option):
    if filename and contents:
        # Decode the uploaded file's contents
        content_type, content_string = contents.split(',')
        decoded = base64.b64decode(content_string)

        # Prepare the file path and save the file
        directory = "src/uploads"  # Using relative path
        files = glob.glob(os.path.join(directory, "*"))
        for f in files:
            os.remove(f)  # Clear old files before saving the new one

        filepath = os.path.join(directory, filename)

        with open(filepath, 'wb') as f:
            f.write(decoded)
        
        # Read the file (assuming the function `read_group_data` is defined elsewhere)
        voltages, Time, GroupA_Detector1, GroupA_Detector2, GroupA_Detector3, GroupB_Detector1, GroupB_Detector2, GroupB_Detector3 = read_group_data(filepath)
        
        # Convert the voltages dataframe to a DataFrame for resampling
        voltages_df = pd.DataFrame(voltages)
        
        # Ensure 'Time' column exists and is in Time format
        voltages_df['Time'] = pd.to_datetime(voltages_df['Time'])

        # Apply the resampling based on the selected option
        if selected_option:
            resampled_df = resample_data(voltages_df, selected_option)
        else:
            resampled_df = voltages_df  # No resampling if no option is selected

        # Create a new directory for resampled data if it doesn't exist
        resampled_directory = '/home/darshana/Desktop/FSM_v2-dashboard/src/resampled_data'
        os.makedirs(resampled_directory, exist_ok=True)

        # Remove old files in the resampled folder
        files = glob.glob(os.path.join(resampled_directory, "*"))
        for f in files:
            os.remove(f)

        # Prepare the file name and path for the resampled data (as Excel)
        resampled_filename = filename.replace('.csv', '_resampled_data.xlsx')
        resampled_filepath = os.path.join(resampled_directory, resampled_filename)

        # Save the resampled data to Excel
        resampled_df.to_excel(resampled_filepath, index=False)

        # Return the path of the resampled file and update the UI with the file name
        return resampled_filepath, f'File Uploaded and Saved as Excel: {resampled_filename}'

    return None, 'No file uploaded yet'



@callback(
    Output('download-file-snirf', 'data'),  # Make sure 'data' is the output, not 'contents'
    Input('btn_rawdata_snirf', 'n_clicks'),
    Input('upload-data', 'filename'),
    prevent_initial_call=True
)
def rawdata_snirf_download(n_clicks, filename):
    if n_clicks and filename:
        print('Button clicked to download')
        
        # Generate SNIRF file
        directory = "src/uploads"  # Path for file
        filepath = os.path.join(directory, filename)
        print('filepath', filepath)

        # Assuming snirf_file is a function that returns the file in the required format
        snirf_file, snirf_file_name = create_snirf(filepath)  # Replace with actual file creation logic
        return dcc.send_file(snirf_file)
    return None

# Function to create the intensity figure
def create_intensity_figure(voltages, spectra_list, title, time_unit='ms'):
    data = []
    y_max = 0  # Variable to track the maximum y value across all spectra
    for spectrum in spectra_list:
        if spectrum in voltages.columns:
            y = voltages[spectrum].values
            y_max = max(y_max, max(y, default=0))  # Update y_max if current y has a higher value
            x = np.arange(len(y))
            trace = go.Scatter(x=x, y=y, mode='lines', name=spectrum)
            data.append(trace)
    
    layout = go.Layout(
        title={'text': title, 'font_size': 24},  # Title font size
        xaxis={'title': f'Time ({time_unit})', 'range': [0, len(x)], 'title_font_size': 20, 'tickfont_size': 20},  # Axis labels and ticks font size
        yaxis={'title': 'Voltage (V)', 'range': [0, y_max], 'title_font_size': 20, 'tickfont_size': 20},  # Axis labels and ticks font size
        legend={'font_size': 16},  # Legend font size
        height=1300
    )
    
    return go.Figure(data=data, layout=layout)



# Function to calculate Noise Equivalent Power (NEP)
def calculate_nep(voltages, dark_detectors):
    nep_values = {}
    for i, dark_detector in enumerate(dark_detectors):
        nep_values[f'detector_{i + 1}_nep'] = np.std(voltages[dark_detector])
    return nep_values

# Helper function to calculate SNR for a signal and its corresponding dark measurement
def calculate_snr(signal_data, dark_data):
    if dark_data.size == 0:
        return 0  # Avoid division by zero if dark_data is empty
    signal = np.mean(signal_data)
    dark_mean = np.mean(dark_data)
    noise = np.std(dark_data)
    return (signal - dark_mean) / noise  # SNR calculation

# Function to create SNR histogram and bar chart
def create_snr_histogram(voltages):
    snr_values = []  # List to store calculated SNR values

    # Define intensity and corresponding dark detectors
    intensity_detectors = [
        'LED_A_784_DET1', 'LED_A_784_DET2', 'LED_A_784_DET3', 
        'LED_A_800_DET1', 'LED_A_800_DET2', 'LED_A_800_DET3', 
        'LED_A_818_DET1', 'LED_A_818_DET2', 'LED_A_818_DET3', 
        'LED_A_835_DET1', 'LED_A_835_DET2', 'LED_A_835_DET3',
        'LED_A_851_DET1', 'LED_A_851_DET2', 'LED_A_851_DET3', 
        'LED_A_881_DET1', 'LED_A_881_DET2', 'LED_A_881_DET3', 
        'LED_B_784_DET1', 'LED_B_784_DET2', 'LED_B_784_DET3', 
        'LED_B_800_DET1', 'LED_B_800_DET2', 'LED_B_800_DET3', 
        'LED_B_818_DET1', 'LED_B_818_DET2', 'LED_B_818_DET3', 
        'LED_B_835_DET1', 'LED_B_835_DET2', 'LED_B_835_DET3',
        'LED_B_851_DET1', 'LED_B_851_DET2', 'LED_B_851_DET3', 
        'LED_B_881_DET1', 'LED_B_881_DET2', 'LED_B_881_DET3'
    ]
    
    dark_detectors = [
        'LED_A_DARK_DET1', 'LED_A_DARK_DET2', 'LED_A_DARK_DET3',
        'LED_B_DARK_DET1', 'LED_B_DARK_DET2', 'LED_B_DARK_DET3'
    ]

    # Calculate SNR for each intensity detector
    for i, intensity_detector in enumerate(intensity_detectors):
        # Corresponding dark detector for each intensity detector
        dark_detector = dark_detectors[i % 3]  # Choose dark detectors cyclically
        
        # Get the intensity and dark data from voltages
        signal_data = voltages[intensity_detector].values
        dark_data = voltages[dark_detector].values
        
        # Calculate and store SNR value
        snr = calculate_snr(signal_data, dark_data)
        snr_values.append(snr)

    # Plot 1: Histogram of SNR for all intensities
    fig1 = go.Figure(data=[go.Histogram(
        x=intensity_detectors,  # Set intensity detectors on the x-axis
        y=snr_values,  # Set the SNR values on the y-axis
        histfunc='sum',  # Sum the values for each intensity detector
        nbinsx=30  # You can adjust this to suit your needs
    )])

    # Update the layout for the histogram plot
    fig1.update_layout(
        title="SNR of Intensities",
        xaxis_title="Intensities (Detector Names)",
        yaxis_title="SNR",
        xaxis={'tickangle': 45},  # Rotate x-axis labels for better readability
        showlegend=False  # Optional: Hide legend as it's not needed for a histogram
    )

    # Calculate and plot the average SNR for each group
    groups = {
        "GroupA_Detector1": ['LED_A_784_DET1', 'LED_A_800_DET1', 'LED_A_818_DET1', 'LED_A_835_DET1', 'LED_A_851_DET1', 'LED_A_881_DET1'],
        "GroupA_Detector2": ['LED_A_784_DET2', 'LED_A_800_DET2', 'LED_A_818_DET2', 'LED_A_835_DET2', 'LED_A_851_DET2', 'LED_A_881_DET2'],
        "GroupA_Detector3": ['LED_A_784_DET3', 'LED_A_800_DET3', 'LED_A_818_DET3', 'LED_A_835_DET3', 'LED_A_851_DET3', 'LED_A_881_DET3'],
        "GroupB_Detector1": ['LED_B_784_DET1', 'LED_B_800_DET1', 'LED_B_818_DET1', 'LED_B_835_DET1', 'LED_B_851_DET1', 'LED_B_881_DET1'],
        "GroupB_Detector2": ['LED_B_784_DET2', 'LED_B_800_DET2', 'LED_B_818_DET2', 'LED_B_835_DET2', 'LED_B_851_DET2', 'LED_B_881_DET2'],
        "GroupB_Detector3": ['LED_B_784_DET3', 'LED_B_800_DET3', 'LED_B_818_DET3', 'LED_B_835_DET3', 'LED_B_851_DET3', 'LED_B_881_DET3']
    }

    group_avg_snr = {}  # Dictionary to store average SNR for each group
    for group, detectors in groups.items():
        group_snr_values = []
        for detector in detectors:
            # Get the intensity and dark data from voltages
            signal_data = voltages[detector].values
            dark_data = voltages[dark_detectors[detectors.index(detector) % len(dark_detectors)]].values
            group_snr_values.append(calculate_snr(signal_data, dark_data))
        group_avg_snr[group] = np.mean(group_snr_values)

    # Plot 2: Bar chart for the average SNR of each group
    fig2 = go.Figure(data=[go.Bar(
        x=list(group_avg_snr.keys()),
        y=list(group_avg_snr.values()),
        name='Average SNR of Groups',
        marker=dict(color='rgba(255, 99, 132, 0.6)')
    )])

    # Update the layout for the bar chart plot
    fig2.update_layout(
        title="Average SNR of Groups",
        xaxis_title="Groups",
        yaxis_title="Average SNR",
        xaxis={'tickangle': 45},  # Rotate x-axis labels for better readability
        showlegend=False  # Optional: Hide legend if not needed
    )

    # Calculate NEP values for each detector
    nep_values = calculate_nep(voltages, dark_detectors)

    # Plot 3: Bar chart for NEP values
    nep_fig = go.Figure(data=[go.Bar(
        x=list(nep_values.keys()),
        y=list(nep_values.values()),
        name='NEP of Detectors',
        marker=dict(color='rgba(99, 255, 132, 0.6)')
    )])

    # Update the layout for the NEP bar chart
    nep_fig.update_layout(
        title="NEP of Detectors",
        xaxis_title="Detectors",
        yaxis_title="NEP",
        xaxis={'tickangle': 45},  # Rotate x-axis labels for better readability
        showlegend=False  # Optional: Hide legend if not needed
    )

    # Return all the figures
    return fig1, fig2, nep_fig


@callback(
    Output('tabs', 'children'),
    Input('view-graph-btn', 'n_clicks'),
    Input('check-data-quality-btn', 'n_clicks'),
    State('groupA_dect1_spectras', 'on'),
    State('groupA_dect2_spectras', 'on'),
    State('groupB_dect1_spectras', 'on'),
    State('groupB_dect2_spectras', 'on'),
    State('select_all_switch', 'on'),
    State('intensities-options-dropdown', 'value'),
    State('store-file-path', 'data'),
    prevent_initial_call=True
)
def update_tabs_and_plots(view_intensity_n_clicks, check_data_quality_n_clicks, groupA1_on, groupA2_on, groupB1_on, groupB2_on, select_all_on, selected_spectra, filepath):
    ctx = dash.callback_context
    if not ctx.triggered:
        return []

    button_id = ctx.triggered[0]['prop_id'].split('.')[0]
    print(f"Triggered by {button_id}")
    # Other logic for updating tabs and plots
    
    if button_id == 'view-graph-btn' and filepath:
        voltages, Time, GroupA_Detector1, GroupA_Detector2, GroupA_Detector3, GroupB_Detector1, GroupB_Detector2, GroupB_Detector3 = read_group_data(filepath)
        
        tabs = []
        if select_all_on:
            groupA1_on = groupA2_on = groupA3_on = True
            groupB1_on = groupB2_on = groupB3_on = True

        if groupA1_on:
            tabs.append(dcc.Tab(label='GroupA_Detector1', value='GroupA_Detector1', children=[
                dcc.Graph(figure=create_intensity_figure(voltages, GroupA_Detector1, 'GroupA_Detector1'))
            ]))
        if groupA2_on:
            tabs.append(dcc.Tab(label='GroupA_Detector2', value='GroupA_Detector2', children=[
                dcc.Graph(figure=create_intensity_figure(voltages, GroupA_Detector2, 'GroupA_Detector2'))
            ]))
        if groupA3_on:
            tabs.append(dcc.Tab(label='GroupA_Detector3', value='GroupA_Detector3', children=[
                dcc.Graph(figure=create_intensity_figure(voltages, GroupA_Detector3, 'GroupA_Detector3'))
            ]))
        if groupB1_on:
            tabs.append(dcc.Tab(label='GroupB_Detector1', value='GroupB_Detector1', children=[
                dcc.Graph(figure=create_intensity_figure(voltages, GroupB_Detector1, 'GroupB_Detector1'))
            ]))
        if groupB2_on:
            tabs.append(dcc.Tab(label='GroupB_Detector2', value='GroupB_Detector2', children=[
                dcc.Graph(figure=create_intensity_figure(voltages, GroupB_Detector2, 'GroupB_Detector2'))
            ]))
        if groupB3_on:
            tabs.append(dcc.Tab(label='GroupB_Detector3', value='GroupB_Detector3', children=[
                dcc.Graph(figure=create_intensity_figure(voltages, GroupB_Detector3, 'GroupB_Detector3'))
            ]))

        if selected_spectra:
            tabs.append(dcc.Tab(label='Selected Intensities', value='Selected_Intensities', children=[
                dcc.Graph(figure=create_intensity_figure(voltages, selected_spectra, 'Selected Intensities'))
            ]))

        return tabs

    elif check_data_quality_n_clicks and filepath:
        voltages, Time, GroupA_Detector1, GroupA_Detector2, GroupA_Detector3, GroupB_Detector1, GroupB_Detector2, GroupB_Detector3 = read_group_data(filepath)

        # Create SNR histogram and bar chart figures
        snr_histogram, snr_bar_chart, nep_fig = create_snr_histogram(voltages)

        # Create a single tab with two rows (first row for histogram, second for bar chart)
        return [
            dcc.Tab(
                label='Check Raw Data Quality',
                value='check_raw_data_quality',
                children=[
                    html.Div(
                        children=[
                            # First Row: SNR Histogram
                            html.Div(
                                dcc.Graph(figure=snr_histogram),
                                style={'width': '100%', 'display': 'inline-block', 'margin-bottom': '20px'}
                            ),
                            # Second Row: SNR Bar Chart
                            html.Div(
                                dcc.Graph(figure=snr_bar_chart),
                                style={'width': '100%', 'display': 'inline-block'}
                            ),
                            # Third Row: NEP Bar Chart
                        html.Div(
                            dcc.Graph(figure=nep_fig),
                            style={'width': '100%', 'display': 'inline-block'}
                        )

                        ]
                    )
                ]
            )
        ]
    
    return []

if __name__ == '__main__':
    app.run_server(debug=True) 
