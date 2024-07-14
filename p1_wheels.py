"""
    TODO
"""
##########==========##########==========##########==========##########==========##########==========
## header

## import packages
import os
import pandas as pd
import numpy as np
import plotly.graph_objects as go

## set parameters
params = dict(
    bgcolor = 'hsv(0,0,1)',
    fgcolor = 'hsv(0,0,0)',
    width = 500 - 5,
    height = 500 - 5
)
params['color_names'] = {
    'Red': 0, 'Orange': 30, 'Yellow': 60,
    'Chartreuse': 90, 'Green': 120, 'Spring Green': 150,
    'Cyan': 180, 'Azure': 210, 'Blue': 240,
    'Violet': 270, 'Magenta': 300, 'Rose': 330
    }

##########==========##########==========##########==========##########==========##########==========
## formulate colors


def make_wheel(h = 12, sv = 5, which = 'HUE'):
    """
        TODO
    """
    theta = pd.DataFrame({'theta':np.linspace(360 - (360 / h), 0, h)}).astype(int)
    radial = pd.DataFrame({'radial':np.linspace(1, 0, sv)})
    wheel = theta.merge(radial, how = 'cross').round(3).astype(str)
    if which == 'HUExVAL':
        wheel['color'] = 'hsv(' + wheel['theta'] + ',0.8,' + wheel['radial'] + ')'
    elif which == 'HUExSAT':
        wheel['color'] = 'hsv(' + wheel['theta'] + ',' + wheel['radial'] + ',0.8)'
    elif which == 'HUE':
        wheel['color'] = 'hsv(' + wheel['theta'] + ',0.8,0.8)'
    else: raise Exception('Invalid which argument')
    wheel = wheel.astype({'theta':float, 'radial': float}).sort_values(['radial', 'theta'])
    wheel['width'] = (360 / h)
    wheel['r'] = 1 / sv
    return wheel


def make_grid(h = 330, sv = 5):
    """
        TODO
    """
    the_grid = pd.DataFrame({'sat': np.linspace(0, 1, sv)})
    the_grid = the_grid.merge(pd.DataFrame({'val': np.linspace(0, 1, sv)}), how = 'cross')
    the_grid = the_grid.round(3).astype(str)
    the_grid['color'] = 'hsv(' + str(h) + ','
    the_grid['color'] += the_grid['sat'] + ',' + the_grid['val'] + ')'
    the_grid = the_grid.astype({'sat': float, 'val': float})
    the_grid['hue'] = h
    return the_grid


##########==========##########==========##########==========##########==========##########==========
## draw polar figures


def make_polar_figure(params = params):
    """
        TODO
    """
    tick_text = params['color_names']
    tick_text = [str(tick_text[i]) + '°<br>' + i for i in tick_text.keys()]
    fig = go.Figure()
    fig = fig.update_layout(
        width = params['width'], height = params['height'],
        polar = dict(bgcolor = params['bgcolor']),
        polar_angularaxis = dict(
            direction = 'clockwise',
            ticktext = tick_text,
            tickvals = list(params['color_names'].values()),
            tickmode = 'array'
            ),
        polar_radialaxis = dict(
            angle = -15,
            ),
        showlegend = False
        )
    return fig


def draw_color_wheel(trace_dict, wheel):
    """
        TODO
    """
    for iter in sorted(list(set(wheel['radial']))):
        idx = wheel['radial'] == iter
        trace_dict[iter] = go.Barpolar(
            theta = wheel.loc[idx, 'theta'],
            width = wheel.loc[idx, 'width'],
            r = wheel.loc[idx, 'r'],
            marker_color = wheel.loc[idx, 'color'],
            marker_line = dict(color = 'white', width = 1),
            customdata = wheel.loc[idx, 'color'],
            hovertemplate = '%{customdata}<extra></extra>',
        )
    return trace_dict

##########==========##########==========##########==========##########==========##########==========
## draw polar figures


def make_grid_figure():
    """
        TODO
    """
    fig = go.Figure()
    fig = fig.update_layout(
        width = params['width'], height = params['height'],
        showlegend = False
        )
    return fig


def draw_grid(trace_dict, grid):
    """
        TODO
    """
    print(grid)



##########==========##########==========##########==========##########==========##########==========
## execute functions in sequence and write result to disk


def write_color_wheel(wheel_type = 'h'):
    """
        TODO
    """
    ## value write 
    wheel = make_wheel(which = wheel_type)
    fig = make_polar_figure()
    trace_dict = dict()
    trace_dict = draw_color_wheel(trace_dict = trace_dict, wheel = wheel)
    fig.add_traces([trace_dict[i] for i in trace_dict.keys()])
    fig.write_html(
        os.path.join('io_mid', wheel_type + '.html'), full_html = True, include_plotlyjs = True)
    fig.write_html(
        os.path.join('io_mid', wheel_type + '.div'), full_html = False, include_plotlyjs = False)


##########==========##########==========##########==========##########==========##########==========
## test code


if __name__ == '__main__':
    write_color_wheel(wheel_type = 'HUE')
    write_color_wheel(wheel_type = 'HUExSAT')
    write_color_wheel(wheel_type = 'HUExVAL')
    grid = make_grid()
    draw_grid(grid = grid, trace_dict = dict())


##########==========##########==========##########==========##########==========##########==========
