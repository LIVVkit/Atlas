"""
The ISMIP6 initMIP Atlas.
"""

from __future__ import absolute_import, division, print_function, unicode_literals
import six

import os
import warnings
import subprocess

import numpy as np
from netCDF4 import Dataset

import livvkit
from livvkit.util import elements as EL
from livvkit.util import functions as FN

_DEBUG = False


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

    pages = {}
    for group in config['groups']:
        for model in config['groups'][group]:
            tabs = []
            for exp in config['experiments']:
                images = []
                err_msg = []
                data_dir = os.path.join(os.path.abspath(config['data_path']), group, model, exp)
                if not os.path.exists(data_dir):
                    err_msg.append('Could not find {}-{} experiment {} in <br> &emsp; {}'.format(group, model, data_dir))
                    continue

                for var in mip:
                    ice_sheet = mip_name.split('-')[-1]
                    
                    data_name = '_'.join([var, ice_sheet, group, model, exp]) + '.nc'
                    data_file = os.path.relpath(os.path.join(data_dir, data_name), os.getcwd())

                    err_msg.extend(check_meta(data_file, var, mip))
                    
                    if var != 'scalar':
                        img_name = '_'.join([var, ice_sheet, group, model, exp]) + '.png'
                        img_file = os.path.relpath(os.path.join(img_dir, img_name), os.getcwd())
                      
                        plot_var(config['plot_script'], data_file, img_file, exp, var, mip)
                        images.append(EL.image(var, 
                                               mip[var]['meta']['standard_name'], 
                                               '/'.join([mip_name, img_name]) ))

                elements = []
                if not err_msg:
                    err_msg_str = 'None<br><p style="color:black">Everything looks good!</p>'
                else:
                    err_msg_str = '<br>' + '<br><br>'.join(err_msg)
                elements.append(EL.error('Meta check', err_msg_str))
                
                elements.append(EL.gallery('Var gallery', images))
               
                tabs.append(EL.tab(exp, element_list=elements))

            page_name = '-'.join([group, model])
            pages[page_name] = EL.page(page_name, 'A Group-model submission.', tab_list=tabs)

    return EL.book(mip_name, __doc__, page_dict=pages) 


def plot_var(plot_script, data_file, img_file, exp, var, mip):
    """
    Use an external NCL plot script to plot a variable from a data file. 

    Args:
        plot_script: Path to the NCL plot script
        data_file: Path to the NetCDF data file containing the variable's data
        img_file: path to save the image file to
        exp: Name of the experiment being analyzed 
        var: Name of the variable to plot
        config: A dictionary representation of the MIP configuration

    Returns: N/A
    """
    ncl_command = ' '.join(["ncl", "-Q",
                            "'afile=\"{}\"'".format(data_file),
                            "'ofile=\"{}\"'".format(img_file),
                            "'aexp=\"{}\"'".format(exp),
                            "'avar=\"{}\"'".format(var),
                            "'atsp={}'".format(mip[var]['timestep'][exp]),
                            "'apal=\"{}\"'".format(mip[var]['palette']),
                            "'amod={}'".format(mip[var]['levelmode']),
                            "'amin={}'".format(mip[var]['lmin']),
                            "'amax={}'".format(mip[var]['lmax']),
                            "'alsp={}'".format(mip[var]['lstep']),
                            "'alvl={}'".format(mip[var]['levels']),
                            plot_script])
                            
    proc = subprocess.Popen(ncl_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    pout, perr = proc.communicate()
    # NOTE: ncl prints errors to stdout because of course it does.
    if _DEBUG:
        with open(ncl_errors.txt, 'a') as f:
            f.write(ncl_command)
            f.write(pout)  


def check_meta(data_file, var, mip):
    """
    Chec the attributes of a variable in a netCDF datafile. 

    Args:
        data_file: Path to the NetCDF data file containing the variable's data
        var: Name of the variable to check
        config: A dictionary representation of the MIP configuration

    Returns: A list of error messages
    """
    message = []
    if not os.path.exists(data_file):
        msg = '{} file missing: <br> &emsp; {}'.format(var, data_file)
        message.append(msg)
        return message
    else:
        try:
            nc_var = Dataset(data_file, 'r')
        except:
            msg = '{} file could not be read: <br> &emsp; {}'.format(var, data_file)
            message.append(msg)
            return message

    if var == 'scalar':
        for var, details in six.iteritems(mip[var]):
            meta = details['meta']
            message.extend(check_var_meta(var, nc_var, data_file, meta))
    else:
        meta = mip[var]['meta']
        message.extend(check_var_meta(var, nc_var, data_file, meta))
        
    return message


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
        return message

    var_data = nc_var.variables[var]
    with warnings.catch_warnings():
        warnings.simplefilter('ignore')
        if np.isnan(var_data).any():
            message.append('{} contains NaNs in: <br> &emsp; {}'.format(var, data_file))

    ncattr = var_data.ncattrs()
    if 'standard_name' not in ncattr:
        message.append('{} missing attribute: "standard_name" in: <br> &emsp; {}'.format(var, data_file))
    elif var_data.getncattr('standard_name') != meta['standard_name']:
        message.append('{} standard name is "{}" but  it should be "{}" in: <br> &emsp; {}'.format(
                           var, var_data.getncattr('standard_name'), meta['standard_name'], data_file))

    if 'units' not in ncattr:
        message.append('{} missing attribute: "units" in: <br> &emsp; {}'.format(var, data_file))

    ndims = len(var_data.shape)
    if not ndims:
        message.append('{} has no dimentions, data could not be read in: <br> &emsp; {}'.format(var, data_file))
    elif ndims != len(meta['dims']):
        message.append('{} has  {} dimensions but it should have {} in: <br> &emsp; {}'.format(
                            var, ndims, len(meta['dims']), data_file))

    return message



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
        print('      {} experiments found: {}'.format(name, smry['Experiments']))
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
