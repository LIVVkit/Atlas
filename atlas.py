"""
The ISMIP6 initMIP Atlas.
"""

from __future__ import absolute_import, division, print_function, unicode_literals
import six

import os
import warnings
import subprocess

import numpy as np
import matplotlib.pyplot as plt
from netCDF4 import Dataset

import livvkit
from livvkit.util import elements as EL
from livvkit.util import functions as FN

_DEBUG = False
_STRICT = False

def mip_config(mip_name):
    mip_path = os.path.dirname(os.path.abspath(__file__))
    return FN.read_json(os.path.join(mip_path, 'projects', mip_name + '.json'))


def run(mip_name, config):
    """
    Runs ISMIP6 Atlas for the project found in the configuration file.

    Args:
        mip_name: The name of the ISMIP6 project to analyize
        config: A dictionary representation of the MIP configuration

    Returns:
       A LIVVkit book element containing a page element for each group-model in the config file
    """
  
    mip = mip_config(mip_name)
    img_dir = os.path.join(livvkit.output_dir, 'validation', 'imgs', mip_name)
    FN.mkdir_p(img_dir)

    try:
        if config['strict']:
            global _STRICT
            _STRICT = True
    except KeyError:
        pass


    pages = {}
    for group in config['groups']:
        for model in config['groups'][group]:
            tabs = []
            for exp in config['experiments']:
                images = []
                err_msg = []
                data_dir = os.path.join(os.path.abspath(config['data_path']), group, model, exp)
                if not os.path.exists(data_dir):
                    err_msg.append('Could not find {}-{} experiment {} in <br> &emsp; {}'.format(group, model, exp, data_dir))
                else:
                    for var in mip:
                        ice_sheet = mip_name.split('-')[-1]
                        
                        data_name = '_'.join([var, ice_sheet, group, model, exp]) + '.nc'
                        data_file = os.path.relpath(os.path.join(data_dir, data_name), os.getcwd())
                        
                        msg, var_data, nc_var = check_meta(data_file, exp, var, mip)
                        err_msg.extend(msg)
                        
                        if var != 'scalar':
                            img_name = '_'.join([var, ice_sheet, group, model, exp]) + '.png'
                            img_file = os.path.relpath(os.path.join(img_dir, img_name), os.getcwd())
                           
                            if var_data:
                                plot_var(var_data, img_file, exp, var, mip, ice_sheet)
                            images.append(EL.image(var, 
                                                   mip[var]['meta']['standard_name'].replace('_',' '), 
                                                   '/'.join([mip_name, img_name]) ))
                        if nc_var:
                            nc_var.close()

                elements = []
                elements.append(EL.gallery('Var gallery', images))
               
                if not err_msg:
                    err_msg_str = 'None<br><p style="color:green">Everything looks good!</p>'
                else:
                    err_msg_str = '<br>' + '<br><br>'.join(err_msg)
                elements.append(EL.error('Meta check', err_msg_str))
                
                tabs.append(EL.tab(exp, element_list=elements))

            page_name = '-'.join([group, model])
            pages[page_name] = EL.page(page_name, 'A Group-model submission.', tab_list=tabs)

    return EL.book(mip_name, __doc__, page_dict=pages) 


def plot_var(var_data, img_file, exp, var, mip, ice_sheet):
    """
    Plot a variable from a netCDF Dataset following the MIP configuration. 

    Args:
        var_data: NetCDF Dataset class containing the variable's data
        img_file: Path to save the image file to
        exp: Name of the experiment being analyzed 
        var: Name of the variable to plot
        mip: A dictionary representation of the MIP configuration
        ice_sheet: Name of the ice sheet being analyzed

    Returns: N/A
    """
    tstep = mip[var]['timestep'][exp]
    cmap = mip[var]['colormap']

    if not _STRICT and (var_data.shape[0] < tstep + 1):
        tstep = -1

    if "AIS" in ice_sheet:
        fig, ax = plt.subplots(1, 1, figsize=(8, 8), dpi=100)
    else:
        fig, ax = plt.subplots(1, 1, figsize=(5, 8), dpi=100)
    # plt.rc('text', usetex=True)
    plt.rc('font', family='serif')

    if mip[var]['lmode'] == 'auto':
        lvls = None
    elif mip[var]['lmode'] == 'manual':
        lmin = mip[var]['lmin'] 
        lmax = mip[var]['lmax'] 
        lstep = mip[var]['lstep'] 
        lvls = np.arange(lmin, lmax + lstep, lstep)
    elif mip[var]['lmode'] == 'explicit':
        lvls = mip[var]['levels'] 

    # Drop the ResouceWarning for datasets with NaNs
    with warnings.catch_warnings():
        warnings.simplefilter('ignore')
        if len(mip[var]['meta']['dims']) == 2:
            plot_data = var_data[:,:]
        else:
            plot_data = var_data[tstep,:,:]

        if lvls is not None:
            ax.contourf(plot_data, cmap=cmap, levels=lvls)
        else:
            ax.contourf(plot_data, cmap=cmap)
        

    ax.set_title(var)

    fig.tight_layout()
    fig.savefig(img_file, bbox_inches='tight')
    
    plt.close(fig)


def check_meta(data_file, exp, var, mip):
    """
    Chec the attributes of a variable in a netCDF datafile. 

    Args:
        data_file: Path to the NetCDF data file containing the variable's data
        exp: Name of the experiment being analyzed
        var: Name of the variable to check
        config: A dictionary representation of the MIP configuration

    Returns: A list of error messages
    """
    message = []
    if not os.path.exists(data_file):
        msg = '{} file missing: <br> &emsp; {}'.format(var, data_file)
        message.append(msg)
        return (message, None, None)
    else:
        try:
            nc_var = Dataset(data_file, 'r')
        except:
            msg = '{} file could not be read: <br> &emsp; {}'.format(var, data_file)
            message.append(msg)
            return (message, None, None)

    if var == 'scalar':
        for v, details in six.iteritems(mip[var]):
            meta = details['meta']
            meta['timestep'] = None
            msg, var_data = check_var_meta(v, nc_var, data_file, meta)
            message.extend(msg)
    else:
        meta = mip[var]['meta']
        meta['timestep'] = mip[var]['timestep'][exp]
        msg, var_data = check_var_meta(var, nc_var, data_file, meta)
        message.extend(msg)
        
    return (message, var_data, nc_var)


def check_var_meta(var, nc_var, data_file, meta):
    """
    Chec the attributes of the variables in netCDF datafile. 

    Args:
        nc_var: A netCDF Dataset (from python-netCDF) of the scalar variables
        data_file: The path to the netCDF data file
        meta: A dictionary describing the variables metadata as they should appear 

    Returns: A list of error messages
    """
    message = []
    nc_var_actual = [v for v in nc_var.variables]
    if var not in nc_var_actual:
        msg = '{} not found in: <br> &emsp; {}'.format(var, data_file)
        message.append(msg)
        return (message, None)

    var_data = nc_var.variables[var]
    # Drop the ResouceWarning for datasets with NaNs
    with warnings.catch_warnings():
        warnings.simplefilter('ignore')
        if np.isnan(var_data).any():
            message.append('{} contains NaNs in: <br> &emsp; {}'.format(var, data_file))

    ndims = len(var_data.shape)
    if not ndims:
        message.append('{} has no dimensions, data could not be read in: <br> &emsp; {}'.format(var, data_file))
        return (message, None)
    elif ndims != len(meta['dims']):
        message.append('{} has  {} dimensions but it should have {} in: <br> &emsp; {}'.format(
                            var, ndims, len(meta['dims']), data_file))
        return (message, None)

    tsteps = var_data.shape[0]
    if meta['timestep'] is not None:
        if tsteps < meta['timestep']+1:
            message.append(' '.join(['{} should have at least {} time steps but has {} in:',
                                     ' <br> &emsp; {}<br> &emsp; Note: this often happens when',
                                     'the final init timestep has not been included as the initial',
                                     'timestep in the follow-on experiments.']
                                    ).format(var, meta['timestep']+1, tsteps, data_file))
            if _STRICT:
                return (message, None)

    ncattr = var_data.ncattrs()
    if 'standard_name' not in ncattr:
        message.append('{} missing attribute: "standard_name" in: <br> &emsp; {}'.format(var, data_file))
    elif var_data.getncattr('standard_name') != meta['standard_name']:
        message.append('{} standard name is "{}" but  it should be "{}" in: <br> &emsp; {}'.format(
                           var, var_data.getncattr('standard_name'), meta['standard_name'], data_file))
    if 'units' not in ncattr:
        message.append('{} missing attribute: "units" in: <br> &emsp; {}'.format(var, data_file))

    return (message, var_data)



def print_summary(case, summary):
    """
    Print to STDOUT a summary of the analysis results

    Args:
        case: The name of the ISMIP6 project being analyzed
        summary: A dictionary containing a summary of the analysis results

    Returns: N/A
    """
    print('    Ran ISMIP6 Atlas for {}'.format(case))
    for name, smry in six.iteritems(summary):
        print('      Analyzed {} experiments: {}'.format(name, smry['Experiments']))
    print('')


def summarize_result(results_book):
    """
    Provides a summary of the analysis results for the output websites' summary
    page and printing to STDOUT
    
    Args:
        results_book: containing a page element for each group-model analysis

    Returns:
        summary: a dictionary representation of the analysis summary
    """
    if _DEBUG:
        FN.write_json(results_book, './', 'temp_book.json')

    summary = {}
    for page_name in results_book['Data']:
        summary[page_name] = {}
        experiments = []
        for exp in results_book['Data'][page_name]['Data']['Tabs']:
            experiments.append(exp['Title'])
        summary[page_name]['Experiments'] = ', '.join(experiments)

    return summary


def populate_metadata(case, config):
    """
    Describes the expected elements of the analysis summary  
    
    Args:
        case: the ISMIP6 project being analyzed.
        config: A dictionary representation of the MIP configuration
    
    Returns:
        metadata: A dictionary representation of the summary metadata 
    
    """
    metadata = {'Type': 'bookSummary',
                'Title': 'Validation',
                'TableTitle': 'ISMIP6 Atlas',
                'Headers': ['Experiments']}
    return metadata
