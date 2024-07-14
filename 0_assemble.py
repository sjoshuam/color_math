"""
    TODO
"""
##########==========##########==========##########==========##########==========##########==========
## HEADER

import shutil, os

##########==========##########==========##########==========##########==========##########==========
## DEFINE COMPONENT FUNCTIONS

def import_html(project_name):
    """read in empty html dashboard"""
    return '\n'.join(open(f'io_in/{project_name}.html', 'rt').readlines())


#def inject_stats(html):
#    """Fill in statistics as needed"""
#    stats = open(os.path.join('io_mid', 'STATS.txt'), 'rt').readlines()
#    for j in [i.split(':') for i in stats]:
#        html = html.replace('<insert>' + j[0] + '</insert>', j[1])
#    return html


def inject_div(id, html, div_class):
    find_string = f'<div class="{div_class}"><insert>{id}</insert></div>'
    replace_string = '\n'.join(open(f'io_mid/{id}.div', 'rt').readlines())
    html = html.replace(find_string, replace_string)
    html = html.replace('<div>', f'<div class="{div_class}">')
    return html


def export_html(html, project_name = 'color_math'):
    """
        TODO
    """
    open('io_out/{0}.html'.format(project_name), 'wt').writelines(html)
    shutil.copyfile('io_in/{0}.css'.format(project_name), 'io_out/{0}.css'.format(project_name))
    #shutil.copyfile('io_in/{0}.png'.format(project_name), 'io_out/{0}.png'.format(project_name))
    #for iter_ext in ['html', 'png', 'css']:
    #    shutil.copyfile(
    #        f'io_out/{project_name}.{iter_ext}', f'../portfolio/p/{project_name}.{iter_ext}')
    return None

##########==========##########==========##########==========##########==========##########==========
## DEFINE TOP-LEVEL FUNCTIONS

##########==========##########==========##########==========##########==========##########==========
## TEST CODE

if __name__ == '__main__':
    html = import_html(project_name = 'color_math')
    ##html = inject_stats(html = html)
    html = inject_div(id = 'HUE', html = html, div_class = 'visual' )
    html = inject_div(id = 'HUExSAT', html = html, div_class = 'visual'  )
    html = inject_div(id = 'HUExVAL', html = html, div_class = 'visual')
    export_html(html)

##########==========##########==========##########==========##########==========##########==========