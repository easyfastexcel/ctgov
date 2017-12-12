import os
import sys
import json
import xmltodict
import datetime
import requests
import urllib.request
from bs4 import BeautifulSoup
from pprint import pprint as ppt # testing


def timestamp_string():
    now = datetime.datetime.now()
    timestamp_date = str(now.year) + '.' + '{:02d}'.format(now.month) + '.' + '{:02d}'.format(now.day)
    timestamp_time = '{:02d}'.format(now.hour) + ':' + '{:02d}'.format(now.minute) + ':' + '{:02d}'.format(now.second)
    timestamp = timestamp_date + ' ' + timestamp_time

    return timestamp


def dir_dl_path_generator():
    dir_temp = os.path.dirname(os.path.dirname(os.path.abspath(__file__))).replace('\\', '/') + '/temp/'
    dir_dldrop = dir_temp + 'dldrop/'
    return dir_dldrop


def check_dir_dl(dirname):
    print('[ ' + timestamp_string() + ' ] ' + 'initiating download')

    try:
        if len(os.listdir(dirname)) >= 1:
            [os.remove(dirname + i) for i in os.listdir(dirname)]
    except Exception as e:
        # if not os.path.exists(dir_dldrop):
        #     os.makedirs(dir_dldrop)
        print('[ERROR - Missing Directory] '+dirname+'\n')
        sys.exit(e)


def basedl_param_builder(down_count=None, down_flds=None, down_fmt=None, down_chunk=None):
    print('[', timestamp_string(), '] building url parameters for download formats ("basedl")...')
    param_basedl = ''
    params = {'down_count':down_count,
              'down_flds':down_flds,
              'down_fmt':down_fmt,
              'down_chunk':down_chunk}

    for param in params:
        if params[param] is None:
            param_basedl = param_basedl + '&' + param + '='
        elif param is 'down_count':
            if params[param] in [10, 100, 1000, 10000, '10', '100', '1000', '10000']:
                param_basedl = param_basedl + '&' + param + '=' + str(params[param])
            else:
                sys.exit('ERROR - basedl_param_builder() - "down_count" value is not 10, 100, 1000, or 10000')
        elif param is 'down_flds':
            if params[param] in ['all', 'default']:
                param_basedl = param_basedl + '&' + param + '=' + str(params[param])
            else:
                sys.exit('ERROR - basedl_param_builder() - "down_flds" value is not "all" or "default"')
        elif param is 'down_fmt':
            if params[param] in ['plain', 'csv', 'tsv', 'xml', 'pdf']:
                param_basedl = param_basedl + '&' + param + '=' + str(params[param])
            else:
                sys.exit('ERROR - basedl_param_builder() - "down_fmt" value is not "plain", "csv", "tsv", "xml", or "pdf"')
        elif param is 'down_chunk':
            if type(params[param]) in [int, str]:
                try:
                    int(params[param])
                except:
                    sys.exit('ERROR - basedl_param_builder() - "down_chunk" value is not a whole number')
                param_basedl = param_basedl + '&' + param + '=' + str(params[param])
            else:
                sys.exit('ERROR - basedl_param_builder() - "down_chunk" value is not a whole number')

    # param_basedl = 'down_count='+down_count+'&down_flds='+down_flds+'&down_fmt='+down_fmt+'&down_chunk='+down_chunk
    return param_basedl


def query_param_builder(param_term=None, param_type=None, param_rslt=None,  param_status=None, param_cond=None,
                        param_intr=None,  param_spons=None, param_phase=None, param_fund=None):

    print('[', timestamp_string(), '] building url parameters for search results ("query")...')
    param_default_list = [('param_term', param_term), ('param_type', param_type),
                          ('param_rslt', param_rslt), ('param_status', param_status),
                          ('param_cond', param_cond), ('param_intr', param_intr),
                          ('param_spons', param_spons), ('param_phase', param_phase),
                          ('param_fund', param_fund)]

    query_param_string = ''

    for param_k, param_v in param_default_list:
        if param_v is None:
            query_param_string = query_param_string+"&"+param_k+"="
        elif param_v is not None:
            if type(param_v) == list:
                for v in param_v:
                    if type(v) == str:
                        v = v.replace(" ", "+")
                    query_param_string = query_param_string + "&" + param_k + "=" + v
            elif type(param_v) == str or type(param_v) == int or type(param_v) == float:
                if type(param_v) == str:
                    param_v = param_v.replace(" ", "+")
                query_param_string = query_param_string + "&" + param_k + "=" + str(param_v)
            else:
                sys.exit('[ERROR] the system encountered an error while building the <url query parameters>; '
                         'type() issue')
        else:
            sys.exit('[ERROR] the system encountered an error while building the <url query parameters>; '
                     '"None" vs "not None"')

    if query_param_string[:1] == "&":
        query_param_string = query_param_string[1:]

    return query_param_string


def url_dl_builder(dict_params):
    param_basedl = basedl_param_builder(down_count=dict_params['basedl_param']['down_count'],
                                        down_flds=dict_params['basedl_param']['down_flds'],
                                        down_fmt=dict_params['basedl_param']['down_fmt'],
                                        down_chunk=dict_params['basedl_param']['down_chunk'])

    param_query = query_param_builder(param_term=dict_params['query_param']['param_term'],
                                      param_type=dict_params['query_param']['param_type'],
                                      param_rslt=dict_params['query_param']['param_rslt'],
                                      param_status=dict_params['query_param']['param_status'],
                                      param_cond=dict_params['query_param']['param_cond'],
                                      param_intr=dict_params['query_param']['param_intr'],
                                      param_spons=dict_params['query_param']['param_spons'],
                                      param_phase=dict_params['query_param']['param_phase'],
                                      param_fund=dict_params['query_param']['param_fund'])

    url_base = 'https://clinicaltrials.gov/ct2/results/download_fields?'

    print('[', timestamp_string(), '] building url for download...')
    url_dl = url_base + param_basedl + '&' + param_query

    return url_dl


def request_xml_data(dict_params):
    print('[', timestamp_string(), '] pinging site for data...')
    print('Query Search and Download Format parameters:')
    for param in list(dict_params.keys()):
        print('====================================\n',
              param,
              '\n------------------------------------')
        ppt(dict_params[param])
        # print('\n')

    with requests.get(url_dl_builder(dict_params)) as r:
        soup = BeautifulSoup(r.content, 'html.parser')

    return soup


def get_list_of_studies_in_xml(dict_params):
    soup = request_xml_data(dict_params)
    search_results = soup.find('search_results')
    list_studies_in_xml = soup.find_all('study')

    print('\nTOTAL SEARCH RESULTS: ', str(search_results['count']))
    print('TOTAL STUDIES EXTRACTED: ', str(len(list_studies_in_xml)), 'of', str(search_results['count']), '\n')
    # [print(study_xml, '\n\n=======================================================\n') for study_xml in list_studies_in_xml]

    return list_studies_in_xml


def get_list_of_studies_in_json(dict_params):
    list_studies_in_xml = get_list_of_studies_in_xml(dict_params)
    list_studies_in_json = [json.loads(json.dumps(xmltodict.parse(str(study))))["study"]
                            for study in list_studies_in_xml]
    return list_studies_in_json


def dl_xml_studies(dl_dirname, url_param_basedl, url_param_query):
    url_base = 'https://clinicaltrials.gov/ct2/results/download_fields?'
    url_dl = url_base + url_param_basedl +'&'+ url_param_query

    # print(dl_dirname+'ctgov_dl.xml')
    urllib.request.urlretrieve(url_dl, dl_dirname+'ctgov_dl.xml')

    print('[ ' + timestamp_string() + ' ] ' + 'download completed')


if __name__ == '__main__':

    dict_params = {
        'basedl_param': {
            'down_count': 10,               # 10, 100, 1000, or 10000
            'down_flds': 'all',             # "all", "default"
            'down_fmt': 'xml',              # "plain", "csv", "tsv", "xml", "pdf"
            'down_chunk': '1'               # (whole number)
        },
        'query_param': {
            'param_term': 'cabozantinib atezolizumab',  # free text; use '+' for spaces
            'param_type': 'Intr',           # (blank), Intr, Obsr, PReg, Expn
            'param_rslt': None,             # (blank), With, Without
            'param_status': None,           # b, a, f, d, g, h, e, i, m, c, j, k, l
            'param_cond': None,             # free text; use '+' for spaces
            'param_intr': None,             # free text; use '+' for spaces
            'param_spons': None,            # free text; use '+' for spaces
            'param_phase': None,            # 4, 0, 1, 2, 3 ("4" is "early phase 1", "0" is "phase 1")
            'param_fund': None}             # 0 (NIH), 1 (Other US), 2 (Industry),
                                            # 3 (all others; individuals, universities, organizations)
    }

    list_studies_in_json = get_list_of_studies_in_json(dict_params)
    ppt(list_studies_in_json)




    # check_dir_dl(dir_dl_path_generator())
    # dl_xml_studies(dl_dirname=dir_dl_path_generator(),
    #                url_param_basedl=param_basedl,
    #                url_param_query=param_query)
    #

