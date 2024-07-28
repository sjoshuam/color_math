""" draw_hue_grid() draws an interactive visualization that shows how a color hue might with
different levels of saturation and brightness.
"""

##########==========##########==========##########==========##########==========##########==========
## HEADER

## import libraries
import sys, os
if not sys.prefix.endswith('.venv'): raise Exception('Virtual environment not detected')
import pandas as pd
import plotly.graph_objects as go

## set parameters
params = dict(num_colors=4)

##########==========##########==========##########==========##########==========##########==========
## COMPONENT FUNCTIONS


def make_hue_grid(hue=210, params=params) -> pd.DataFrame:
    """generates permutations of a color hue with different brightness and saturation variations
    Inputs:
        hue = hue coordinate for color will be drawn.  Default is Azure (210°)
        sat_n = Number of different saturation points to be generated.
        val_n = Number of different value points to be generated.
    Notes:
        sat_n x val_n equals the total number of variations of the hue that will be shown.
    """

    ## generate color
    sat_n, val_n = params['num_colors'], params['num_colors']
    sat = pd.Series(data=[i / (sat_n-1) for i in range(0, sat_n)], name='sat')
    val = pd.Series(data=[i / (val_n-1) for i in range(0, val_n)], name='val')
    hue_grid = pd.DataFrame(val).merge(sat, how = 'cross')
    hue_grid['hue'] = hue
    hue_grid['color'] = 'hsv(' + hue_grid['hue'].astype(str).str.zfill(3) + ','
    hue_grid['color'] += hue_grid['sat'].round(2).astype(str) + ','
    hue_grid['color'] += hue_grid['val'].round(2).astype(str) + ')'
    del hue, sat, val

    ## generate color xy coordinates
    val_n, sat_n = 1 / (val_n-1),  1 / (sat_n-1)
    hue_grid['val_top'] = (hue_grid['val'] + val_n).astype(str)
    hue_grid['sat_top'] = (hue_grid['sat'] + sat_n).astype(str)
    hue_grid['left_high']  = list(zip(hue_grid['val'],     hue_grid['sat_top']))
    hue_grid['right_high'] = list(zip(hue_grid['val_top'], hue_grid['sat_top']))
    hue_grid['left_low']   = list(zip(hue_grid['val'],     hue_grid['sat']))
    hue_grid['right_low']  = list(zip(hue_grid['val_top'], hue_grid['sat']))
    hue_grid['polygon'] = list(zip(
        hue_grid['left_high'], hue_grid['right_high'], hue_grid['right_low'], hue_grid['left_low']))
    hue_grid = hue_grid[['hue','sat','val','polygon', 'color']]

    return hue_grid


def make_hue_traces(traces:dict, hue_grid:pd.DataFrame, visible=False) -> dict:
    """ Converts hue_grid data into plotly traces
    Inputs: hue_grid = output from make_hue_grid().  Coordinates and colors needed to draw grid.
    """
    for iter_row in hue_grid.index:
        color_iter = hue_grid.at[iter_row, 'color']

        ## generate color squares
        traces[color_iter] = go.Scatter(
            x=[i[0] for i in hue_grid.at[iter_row, 'polygon']],
            y=[i[1] for i in hue_grid.at[iter_row, 'polygon']],
            fill='toself',
            fillcolor=color_iter,
            text=color_iter,
            name='',
            hovertemplate="%{text}<extra></extra>",
            mode='lines',
            line = dict(color='hsv(0,0,0.5)', width=1),
            textposition='middle center',
            visible = visible
        )

    return traces


def make_slider(hue_traces:dict) -> list:
    """Make a slider bar to control the hue of the SATxVAL figure"""

    ## package visibility information in step format
    visible = list()
    for iter in range(0,12):
        iter_hue = 'hsv(' + str(iter*30).zfill(3)
        visible.append(
            dict(method= 'update', label = str(iter*30)+'°',
            args = [dict(visible=[i.startswith(iter_hue) for i in hue_traces.keys()])]
            ))

    ## package visibility information in slider format
    slider = [dict(
        font = dict(size = 10, color = 'hsv(0,0,0)'),
        currentvalue=dict(font = dict(size = 12), prefix='Hue: '),
        active = 11, steps = visible, pad = dict(b=0, l=8, r=8, t=0)
        )]
    return slider


def write_figure(hue_traces:dict, slider:list[dict], params=params) -> None:
    """Incorporate plotly traces intoa figure object and write to disk"""

    axis_ticktext = [i / (params['num_colors']-1) for i in range(0, params['num_colors'])]
    axis_tickvals = [i + 0.5 / (params['num_colors']-1) for i in axis_ticktext]
    axis_ticktext = [str(round(i,2)) for i in axis_ticktext]

    ## make plotly figure object
    space = '<br>'*0
    max_range = params['num_colors'] / (params['num_colors']-1)
    fig = go.Figure()
    fig = fig.update_layout(
        width=500-5, height=500-5,
        showlegend=False,
        plot_bgcolor='hsv(0,0,1)',
        margin=dict(r=0,l=0, t=00, b=0), dragmode=False,
        xaxis=dict(visible=True, range=[-0.01,max_range+0.01], title=space+'--- Vibrancy -->',
                   tickvals=axis_tickvals, ticktext=axis_ticktext, side='top'),
        yaxis=dict(visible=True, range=[-0.01,max_range+0.01], title=space+'<-- Saturation ---',
                   tickvals=axis_tickvals, ticktext=axis_ticktext),
        sliders=slider
    )

    ##
    fig = fig.add_traces([hue_traces[i] for i in hue_traces.keys()])

    ## write plotly figure object to disk
    fig.write_html(os.path.join('io_mid', 'SATxVAl.div'), full_html=False, include_plotlyjs=False)
    fig.write_html(os.path.join('io_mid', 'SATxVAl.html'), full_html=True, include_plotlyjs=True)


##########==========##########==========##########==========##########==========##########==========
## MAIN FUNCTION


def generate_hue_grid() -> None:
    """TODO"""

    hue_traces = dict()
    for i in range(0, 12):
        hue_grid = make_hue_grid(hue=i*30)
        hue_grid.to_excel('~/Desktop/'+str(i)+'.xlsx')
        hue_traces = make_hue_traces(traces=hue_traces, hue_grid=hue_grid, visible=i==11)
    slider = make_slider(hue_traces)
    write_figure(hue_traces=hue_traces, slider=slider)
    return None


##########==========##########==========##########==========##########==========##########==========
## TEST FUNCTION

if __name__ == '__main__':
    generate_hue_grid()

##########==========##########==========##########==========##########==========##########==========
