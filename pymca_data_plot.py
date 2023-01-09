import plotly.graph_objects as go
import numpy as np
import pandas as pd
import plotly.io as pio

data = pd.read_csv('Cd_on_Au_CV_0.4--0.2.csv')
data_2 = pd.read_csv('Cd_on_Au_CV_0.4--0.4.csv')
data_3 = pd.read_csv('Cd_on_Au_CV_0.4--0.65.csv')
#data_4 = pd.read_csv('Cd_on_Au_CV_0.4--0.8.csv')
#data_5 = pd.read_csv('S_on_Au_CV_-1--0.55.csv')


#adding column names to the data
data.columns = ['Voltage (V)', 'Current (I/uA)']
current = data['Current (I/uA)']
volts = data['Voltage (V)']

data_2.columns = ['Voltage (V)', 'Current (I/uA)']
current_2 = data_2['Current (I/uA)']
volts_2 = data_2['Voltage (V)']

data_3.columns = ['Voltage (V)', 'Current (I/uA)']
current_3 = data_3['Current (I/uA)']
volts_3 = data_3['Voltage (V)']
'''
data_4.columns = ['Voltage (V)', 'Current (I/uA)']
current_4 = data_4['Current (I/uA)']
volts_4 = data_4['Voltage (V)']
'''
'''
data_5.columns = ['Voltage (V)', 'Current (I/uA)']
current_5 = data_5['Current (I/uA)']
volts_5 = data_5['Voltage (V)']
'''

def data_plot():
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=volts,
        y=current,
        mode='lines',
        name='Cd on Au CV (0.40 V to -0.20 V to 0.40 V)',
        line=dict(color='black', width=2)
        )
    )

    #Adding axis labels to my plotly graph
    fig.update_xaxes(title_text='Potential/V vs. (Ag/AgCl)')
    fig.update_yaxes(title_text='Current (\u03BCA)')

    '''
    #Adding a title to my plotly graph
    fig.update_layout(
        title={
            'text': "Voltage (V) vs Current (uA)"})
    
    '''
    #aligning the title to the center
    fig.update_layout(title_x=0.5)

    #changing the size of the title
    fig.update_layout(title_font_size=30)

    #changing the size of the axis labels
    fig.update_xaxes(title_font_size=20)
    fig.update_yaxes(title_font_size=20)

    #changing the font of the axis labels
    fig.update_xaxes(title_font_family="Arial")
    fig.update_yaxes(title_font_family="Arial")

    #making the title bold
    fig.update_layout(title_font_family="Arial Bold")

    #Underline the title
    fig.update_layout(title_font_family="Arial Bold Underline")

    #underline the axis labels
    fig.update_xaxes(title_font_family="Arial Underline")
    fig.update_yaxes(title_font_family="Arial Underline")

    #changing the theme of the figure
    fig.update_layout(template="plotly_white")

    fig.add_trace(go.Scatter(
        x=volts_2,
        y=current_2,
        mode='lines',
        name='Cd on Au CV (0.40 V to -0.40 V to 0.40 V)',
        line=dict(color='red', width=2)
    )
    )

    fig.add_trace(go.Scatter(
        x=volts_3,
        y=current_3,
        mode='lines',
        name='Cd on Au CV (0.40 V to -0.65 V to 0.40 V)',
        line=dict(color='blue', width=2)
    )
    )
    '''
    fig.add_trace(go.Scatter(
        x=volts_4,
        y=current_4,
        mode='lines',
        name='S on Au CV (-1.00 V to -0.50 V to -1.00 V)',
        line=dict(color='green', width=2)
    )
    )
    '''
    '''
    fig.add_trace(go.Scatter(
        x=volts_5,
        y=current_5,
        mode='lines+markers',
        name='S on Au CV (-1.00 V to -0.55 V to -1.00 V)',
        line=dict(color='yellow', width=2)
    )
    )
    '''
    #adding a legend to my plotly graph
    fig.update_layout(legend=dict(
        yanchor="top",
        y=0.99,
        xanchor="left",
        x=0.01
    ))

    fig.show()

data_plot()






