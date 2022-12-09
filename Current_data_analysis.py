import plotly.graph_objects as go
import numpy as np
import pandas as pd

data = pd.read_csv('current_data.csv') #Change the file name accordingly

#adding column names to the data
data.columns = ['Time (H:M:S:mS)', 'Voltage (V)', 'Current (I/uA)', 'Solution']

current = data['Current (I/uA)']
volts = data['Voltage (V)']
time = data['Time (H:M:S:mS)']

print(data.head())

def combo():
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=time,
        y=current,
        mode='lines+markers',
        name='Current (uA) vs Time (s)',
        line=dict(color='black', width=2)
        )
    )

    #Adding axis labels to my plotly graph
    fig.update_xaxes(title_text='Time (H:M:S:mS)')
    fig.update_yaxes(title_text='Current (uA)')

    #Adding a title to my plotly graph
    fig.update_layout(
        title={
            'text': "Current (uA) vs Time (s)"})
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


    #Changing the style of the plot
    #fig.update_layout(template="plotly_white")
    #['ggplot2', 'seaborn', 'simple_white', 'plotly', 'plotly_white', 'plotly_dark', 'presentation', 'xgridoff', 'ygridoff', 'gridon', 'none']

    #Plotting on the same graph
    fig.add_trace(go.Scatter(
        x=time,
        y=volts,
        mode='lines+markers',
        name='Voltage (V) vs Time (s)',
        line=dict(color='red', width=2),

        )
    )

    #plotting a vertical line when there is a change in the voltage
    condition = None
    volt = volts.round(2)
    for i in range(len(volts)):
        #excluding the first value
        if i == 0:
            continue
        if volt[i] != volt[i-1]:
            condition = True
        else:
            condition = False

        if condition == True:
            fig.add_vline(x=time[i], line_width=3, line_dash="dash", line_color="green")
            fig.add_annotation(
                x=time[i],
                y=volts[i],
                text="Voltage: " + str(volts[i]) + "V",
                showarrow=True,
                arrowhead=1,
                ax=0,
                ay=-40
            )
    #plotting a vertical line when there is a change in solution
    solution = data['Solution']
    for i in range(len(solution)):
        #excluding the first value
        if i == 0:
            continue
        if solution[i] != solution[i-1]:
            condition = True
        else:
            condition = False

        if condition == True:
            fig.add_vline(x=time[i], line_width=3, line_dash="dash", line_color="orange")
            fig.add_annotation(
                x=time[i],
                y=volts[i],
                text="Solution: " + str(solution[i]),
                showarrow=True,
                arrowhead=1,
                ax=0,
                ay=-200
            )
    # adding a legend to the plot
    fig.update_layout(legend=dict(
        yanchor="top",
        y=0.99,
        xanchor="right",
        x=0.01
    ))
    # adding the orange and green lines to the legend
    fig.add_trace(go.Scatter(
        x=[None],
        y=[None],
        mode='lines',
        line=dict(color='green', width=3),
        name='Voltage Change'
    ))
    fig.add_trace(go.Scatter(
        x=[None],
        y=[None],
        mode='lines',
        line=dict(color='orange', width=3),
        name='Solution Change'
    ))

    fig.show()

def I_vs_t():
    fig2 = go.Figure()
    fig2.add_trace(go.Scatter(
        x=time,
        y=current,
        mode='lines+markers',
        name='Current (uA) vs Time (s)',
        line=dict(color='black', width=2)
    )
    )

    # Adding axis labels to my plotly graph
    fig2.update_xaxes(title_text='Time (H:M:S:mS)')
    fig2.update_yaxes(title_text='Current (uA)')

    # Adding a title to my plotly graph
    fig2.update_layout(
        title={
            'text': "Current (uA) vs Time (s)"})
    # aligning the title to the center
    fig2.update_layout(title_x=0.5)

    # changing the size of the title
    fig2.update_layout(title_font_size=30)

    # changing the size of the axis labels
    fig2.update_xaxes(title_font_size=20)
    fig2.update_yaxes(title_font_size=20)

    # changing the font of the axis labels
    fig2.update_xaxes(title_font_family="Arial")
    fig2.update_yaxes(title_font_family="Arial")

    # making the title bold
    fig2.update_layout(title_font_family="Arial Bold")

    # Underline the title
    fig2.update_layout(title_font_family="Arial Bold Underline")

    # underline the axis labels
    fig2.update_xaxes(title_font_family="Arial Underline")
    fig2.update_yaxes(title_font_family="Arial Underline")

    # Changing the style of the plot
    # fig.update_layout(template="plotly_white")
    # ['ggplot2', 'seaborn', 'simple_white', 'plotly', 'plotly_white', 'plotly_dark', 'presentation', 'xgridoff', 'ygridoff', 'gridon', 'none']

    # plotting a vertical line when there is a change in the voltage
    condition = None
    volt = volts.round(2)
    for i in range(len(volts)):
        # excluding the first value
        if i == 0:
            continue
        if volt[i] != volt[i - 1]:
            condition = True
        else:
            condition = False

        if condition == True:
            fig2.add_vline(x=time[i], line_width=3, line_dash="dash", line_color="green")
            fig2.add_annotation(
                x=time[i],
                y=current[i],
                text="Voltage: " + str(volts[i]) + "V",
                showarrow=True,
                arrowhead=1,
                ax=0,
                ay=-40
            )

    # plotting a vertical line when there is a change in solution
    solution = data['Solution']
    for i in range(len(solution)):
        # excluding the first value
        if i == 0:
            continue
        if solution[i] != solution[i - 1]:
            condition = True
        else:
            condition = False

        if condition == True:
            fig2.add_vline(x=time[i], line_width=3, line_dash="dash", line_color="orange")
            fig2.add_annotation(
                x=time[i],
                y=volts[i],
                text="Solution: " + str(solution[i]),
                showarrow=True,
                arrowhead=1,
                ax=0,
                ay=-200
            )
    # adding a legend to the plot
    fig2.update_layout(legend=dict(
        yanchor="top",
        y=0.99,
        xanchor="right",
        x=0.01
    ))
    # adding the orange and green lines to the legend
    fig2.add_trace(go.Scatter(
        x=[None],
        y=[None],
        mode='lines',
        line=dict(color='green', width=3),
        name='Voltage Change'
    ))
    fig2.add_trace(go.Scatter(
        x=[None],
        y=[None],
        mode='lines',
        line=dict(color='orange', width=3),
        name='Solution Change'
    ))
    fig2.show()


def V_vs_t():
    fig3 = go.Figure()
    fig3.add_trace(go.Scatter(
        x=time,
        y=volts,
        mode='lines+markers',
        name='Voltage (V) vs Time (s)',
        line=dict(color='red', width=2),
    )
    )

    # Adding axis labels to my plotly graph
    fig3.update_xaxes(title_text='Time (H:M:S:mS)')
    fig3.update_yaxes(title_text='Voltage (V)')

    # Adding a title to my plotly graph
    fig3.update_layout(
        title={
            'text': "Voltage (V) vs Time (s)"})
    # aligning the title to the center
    fig3.update_layout(title_x=0.5)

    # changing the size of the title
    fig3.update_layout(title_font_size=30)

    # changing the size of the axis labels
    fig3.update_xaxes(title_font_size=20)
    fig3.update_yaxes(title_font_size=20)

    # changing the font of the axis labels
    fig3.update_xaxes(title_font_family="Arial")
    fig3.update_yaxes(title_font_family="Arial")

    # making the title bold
    fig3.update_layout(title_font_family="Arial Bold")

    # Underline the title
    fig3.update_layout(title_font_family="Arial Bold Underline")

    # underline the axis labels
    fig3.update_xaxes(title_font_family="Arial Underline")
    fig3.update_yaxes(title_font_family="Arial Underline")

    # Changing the style of the plot
    # fig.update_layout(template="plotly_white")
    # ['ggplot2', 'seaborn', 'simple_white', 'plotly', 'plotly_white', 'plotly_dark', 'presentation', 'xgridoff', 'ygridoff', 'gridon', 'none']

    # plotting a vertical line when there is a change in the voltage
    condition = None
    volt = volts.round(1)
    for i in range(len(volts)):
        # excluding the first value
        if i == 0:
            continue
        if volt[i] != volt[i - 1]:
            condition = True
        else:
            condition = False

        if condition == True:
            fig3.add_vline(x=time[i], line_width=3, line_dash="dash", line_color="green")
            #adding a label to each plotted vertical line
            fig3.add_annotation(
                x=time[i],
                y=volts[i],
                text="Voltage: " + str(volts[i]) + "V",
                showarrow=True,
                arrowhead=1,
                ax=0,
                ay=-40
            )
    # plotting a vertical line when there is a change in solution
    solution = data['Solution']
    for i in range(len(solution)):
        # excluding the first value
        if i == 0:
            continue
        if solution[i] != solution[i - 1]:
            condition = True
        else:
            condition = False

        if condition == True:
            fig3.add_vline(x=time[i], line_width=3, line_dash="dash", line_color="orange")
            fig3.add_annotation(
                x=time[i],
                y=volts[i],
                text="Solution: " + str(solution[i]),
                showarrow=True,
                arrowhead=1,
                ax=0,
                ay=-200
            )
    #adding a legend to the plot
    fig3.update_layout(legend=dict(
        yanchor="top",
        y=0.99,
        xanchor="right",
        x=0.01
    ))
    #adding the orange and green lines to the legend
    fig3.add_trace(go.Scatter(
        x=[None],
        y=[None],
        mode='lines',
        line=dict(color='green', width=3),
        name='Voltage Change'
    ))
    fig3.add_trace(go.Scatter(
        x=[None],
        y=[None],
        mode='lines',
        line=dict(color='orange', width=3),
        name='Solution Change'
    ))

    fig3.show()




I_vs_t()
V_vs_t()
combo()


