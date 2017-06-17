"""
The ISMIP6 initMIP Atlas.
"""

from __future__ import absolute_import, division, print_function, unicode_literals
import six

import os
import subprocess

from netCDF4 import Dataset

import livvkit
from livvkit.util import elements as EL
from livvkit.util import functions as FN

_DEBUG = False


def mip_config(mip_name):
    mip_path = os.path.dirname(os.path.abspath(__file__))
    return FN.read_json(os.path.join(mip_path, mip_name + '.json'))


def run(mip_name, config):
    """
    Runs the analysis.

    Args:
        mip_name: The name of the test
        config: A dictionary representation of the configuration file

    Returns:
       The result of elements.book with the list of pages to display
    """
  
    mip = mip_config(mip_name)
    img_dir = os.path.join(livvkit.output_dir, 'validation', 'imgs', mip_name)
    FN.mkdir_p(img_dir)

    pages = {}
    for group in config['groups']:
        for model in config['groups'][group]['models']:
            tabs = []
            for exp in config['experiments']:
                images = []
                err_msg = []
                for var in mip:
                    ice_sheet = mip_name.split('-')[-1]
                    
                    data_dir = os.path.join(os.path.abspath(config['data_path']), group, model, exp)
                    data_name = '_'.join([var, ice_sheet, group, model, exp]) + '.nc'
                    data_file = os.path.relpath(os.path.join(data_dir, data_name), os.getcwd())

                    err_msg.extend(check_meta(data_file, var, mip))
                    
                    if var != 'scalar':
                        img_name = '_'.join([var, ice_sheet, group, model, exp]) + '.png'
                        img_file = os.path.relpath(os.path.join(img_dir, img_name), os.getcwd())
                      
                        plot_var(config['plot_script'], data_file, img_file, exp, var, mip)
                        images.append(EL.image(var, '', '/'.join([mip_name, img_name]) ))

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
        message.extend(check_scalar_meta(nc_var, mip[var]))
    else:
        meta = mip[var]['meta']
        var_data = nc_var.variables[var] 
        ncattr = var_data.ncattrs()
        if 'standard_name' not in ncattr:
            message.append('{} missing attribute: "standard_name" '.format(var))
        elif var_data.getncattr('standard_name') != meta['standard_name']:
            message.append('{} standard name is "{}" but  it should be "{}" '.format(
                               var, var_data.getncattr('standard_name'), meta['standard_name']))

        if 'units' not in ncattr:
            message.append('{} missing attribute: "units" '.format(var))

        ndims = len(var_data[:].shape)
        if ndims != len(meta['dims']):
            message.append('{} has  {} dimensions but it should have {} '.format(var, ndims, len(meta['dims'])))

    return message


def check_scalar_meta(nc_var, scalars):
    message = []
    for var, details in six.iteritems(scalars):
        meta = details['meta']
        var_data = nc_var.variables[var] 
        ncattr = var_data.ncattrs()
        if 'standard_name' not in ncattr:
            message.append('scalar {} missing attribute: "standard_name" '.format(var))
        elif var_data.getncattr('standard_name') != meta['standard_name']:
            message.append('scalar {} standard name is "{}" but  it should be "{}" '.format(
                               var, var_data.getncattr('standard_name'), meta['standard_name']))

        if 'units' not in ncattr:
            message.append('scalar {} missing attribute: "units" '.format(var))

        ndims = len(var_data[:].shape)
        if ndims != len(meta['dims']):
            message.append('scalar {} has  {} dimensions but it should have {} '.format(var, ndims, len(meta['dims'])))

    return message



def print_summary(case, summary):
    """
    Print out a summary generated by this module's summarize_result method
    """
    print('    Ran ISMIP6 Atlas for {}'.format(case))
    for name, smry in six.iteritems(summary):
        print('      {} experiments found: {}'.format(name, smry['Experiments']))
    print('')


def summarize_result(results_book):
    """
    Provides a snapshot of the results of the analysis to be provided
    to the sumamry as well as being printed out in this module's
    print_summary method
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
    Generates the metadata responsible for telling the summary what
    is done by this module's run method
    """
    metadata = {'Type': 'bookSummary',
                'Title': 'Validation',
                'TableTitle': 'ISMIP6 Atlas',
                'Headers': ['Experiments']}
    return metadata
