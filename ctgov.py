import os
import sys
import json
import xmltodict
import datetime
import requests
import urllib.request
from bs4 import BeautifulSoup
from pprint import pprint as ppt


def timestamp_string(option='default'):
    now = datetime.datetime.now()

    if option == 'default':     # e.g. yyyy.mm.dd hh:mm:ss
        timestamp_date = str(now.year) + '.' + '{:02d}'.format(now.month) + '.' + '{:02d}'.format(now.day)
        timestamp_time = '{:02d}'.format(now.hour) + ':' + '{:02d}'.format(now.minute) + \
                         ':' + '{:02d}'.format(now.second)
        timestamp = timestamp_date + ' ' + timestamp_time
    elif option == 'filename':  # e.g. yyyymmdd_hhmmss
        timestamp_date = str(now.year) + '{:02d}'.format(now.month) + '{:02d}'.format(now.day)
        timestamp_time = '{:02d}'.format(now.hour) + '{:02d}'.format(now.minute) + '{:02d}'.format(now.second)
        timestamp = timestamp_date + '_' + timestamp_time
    else:
        print('error in "def timestamp_string(option)"')
        sys.exit('ERROR - entered "option" is not accepted')

    return timestamp


def dir_dl_path_generator(option):

    if option == 'Downloads':
        dir_dldrop = os.path.expanduser('~').replace('\\', '/')+'/Downloads/'
    elif option == 'Dev':
        dir_temp = os.path.dirname(os.path.dirname(os.path.abspath(__file__))).replace('\\', '/') + '/temp/'
        dir_dldrop = dir_temp + 'dldrop/'
    else:
        print('An unacceptable "option" was entered')
        sys.exit('error at "def dir_dl_path_generator()"')

    return dir_dldrop


def check_dir_dl(option):
    print('[ ' + timestamp_string() + ' ] ' + 'initiating download')

    dirname = dir_dl_path_generator(option)

    if option == 'Downloads':
        if os.path.exists(dirname):
            print(dirname, 'exists')
        else:
            sys.exit('ERROR - "'+dirname+'" not found')
    elif option == 'Dev':
        try:
            if len(os.listdir(dirname)) >= 1:
                [os.remove(dirname + i) for i in os.listdir(dirname)]
        except Exception as e:
            print('[ERROR - Missing Directory] ' + dirname + '\n')
            sys.exit(e)
    else:
        print('error at "def check_dir_dl(option):"')
        sys.exit('ERROR - entered "option" is not accepted')


class DataExtract:

    def __init__(self, down_count=10, down_flds='default', down_fmt='xml', down_chunk=1,
                 param_term=None, param_type=None, param_rslt=None, param_status=None, param_cond=None,
                 param_intr=None, param_spons=None, param_phase=None, param_fund=None):

        self.dict_params = {
            'basedl_param': {
                'down_count': down_count,       # 10, 100, 1000, or 10000
                'down_flds': down_flds,         # "all", "default"
                'down_fmt': down_fmt,           # "plain", "csv", "tsv", "xml", "pdf"
                'down_chunk': down_chunk        # (whole number)
            },
            'query_param': {
                'param_term': param_term,       # free text; use '+' for spaces
                'param_type': param_type,       # (blank), Intr, Obsr, PReg, Expn
                'param_rslt': param_rslt,       # (blank), With, Without
                'param_status': param_status,   # b, a, f, d, g, h, e, i, m, c, j, k, l
                'param_cond': param_cond,       # free text; use '+' for spaces
                'param_intr': param_intr,       # free text; use '+' for spaces
                'param_spons': param_spons,     # free text; use '+' for spaces
                'param_phase': param_phase,     # 4, 0, 1, 2, 3 ("4" is "early phase 1", "0" is "phase 1")
                'param_fund': param_fund}       # 0 (NIH), 1 (Other US), 2 (Industry), 3 (all others; univ, indiv, org)
        }
        self.timestamp_filename = timestamp_string(option='filename')
        self.soup_xml_data = self.request_xml_data()

    def basedl_param_builder(self):
        print('[', timestamp_string(), '] building url parameters for download formats ("basedl")...')
        param_basedl = ''
        params = {'down_count': self.dict_params['basedl_param']['down_count'],
                  'down_flds': self.dict_params['basedl_param']['down_flds'],
                  'down_fmt': self.dict_params['basedl_param']['down_fmt'],
                  'down_chunk': self.dict_params['basedl_param']['down_chunk']}

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
                    sys.exit('ERROR - basedl_param_builder() - '
                             '"down_fmt" value is not "plain", "csv", "tsv", "xml", or "pdf"')
            elif param is 'down_chunk':
                if type(params[param]) in [int, str]:
                    try:
                        int(params[param])
                    except Exception as e:
                        print(e)
                        sys.exit('ERROR - basedl_param_builder() - "down_chunk" value is not a whole number')
                    param_basedl = param_basedl + '&' + param + '=' + str(params[param])
                else:
                    sys.exit('ERROR - basedl_param_builder() - "down_chunk" value is not a whole number')

        return param_basedl

    def query_param_builder(self):

        print('[', timestamp_string(), '] building url parameters for search results ("query")...')
        param_default_list = [('param_term', self.dict_params['query_param']['param_term']),
                              ('param_type', self.dict_params['query_param']['param_type']),
                              ('param_rslt', self.dict_params['query_param']['param_rslt']),
                              ('param_status', self.dict_params['query_param']['param_status']),
                              ('param_cond', self.dict_params['query_param']['param_cond']),
                              ('param_intr', self.dict_params['query_param']['param_intr']),
                              ('param_spons', self.dict_params['query_param']['param_spons']),
                              ('param_phase', self.dict_params['query_param']['param_phase']),
                              ('param_fund', self.dict_params['query_param']['param_fund'])]

        query_param_string = ''

        for param_k, param_v in param_default_list:
            if param_v is None:
                query_param_string = query_param_string+"&"+param_k+"="
            elif param_v is not None:
                if type(param_v) == list:
                    for v in list(param_v):
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

    def url_dl_builder(self):
        url_base = 'https://clinicaltrials.gov/ct2/results/download_fields?'
        param_basedl = self.basedl_param_builder()
        param_query = self.query_param_builder()

        print('[', timestamp_string(), '] building url for data extract...')
        url_dl = url_base + param_basedl + '&' + param_query

        return url_dl

    def request_xml_data(self):
        print('[', timestamp_string(), '] pinging site for data...')
        print('\nQUERY SEARCH AND DOWNLOAD FORMAT PARAMETERS:')
        for param in list(self.dict_params.keys()):
            print('===========================================================\n',
                  param,
                  '\n-----------------------------------------------------------')
            ppt(self.dict_params[param])
        print('')

        url = self.url_dl_builder()
        print('[', timestamp_string(), '] extracting data...')
        # with requests.get(url) as r:
        #     print('[', timestamp_string(), '] parsing extracted data...')
        #     soup = BeautifulSoup(r.content, 'html.parser')
        r = requests.get(url)
        print('[', timestamp_string(), '] parsing extracted data...')
        soup = BeautifulSoup(r.content, 'html.parser')
        print('[', timestamp_string(), '] done!')

        search_results = soup.find('search_results')
        print('\nTOTAL SEARCH RESULTS: ', str(search_results['count']))
        list_studies_in_xml = soup.find_all('study')
        print('TOTAL STUDIES EXTRACTED: ', str(len(list_studies_in_xml)), 'of', str(search_results['count']), '\n')

        return soup

    def get_list_of_studies_in_xml(self):
        list_studies_in_xml = self.soup_xml_data.find_all('study')
        return list_studies_in_xml

    def get_list_of_studies_in_json(self):
        list_studies_in_json = [json.loads(json.dumps(xmltodict.parse(str(study))))["study"]
                                for study in self.get_list_of_studies_in_xml()]
        return list_studies_in_json

    def dl_xml_studies(self, option='Downloads'):
        dirname = dir_dl_path_generator(option)
        if option == 'Dev':
            check_dir_dl(option)
        urllib.request.urlretrieve(str(self.url_dl_builder()),
                                   str(dirname)+'ctgov_dl_'+str(self.timestamp_filename)+'.xml')
        print('[ ' + timestamp_string() + ' ] ' + 'download completed...'
                                                  'the file has been downloaded into "'+dirname+'"')

# def main():
#     data_ctgov = DataExtract()
#     print('[', timestamp_string(), ']', 'starting.....')
#     ppt(data_ctgov.get_list_of_studies_in_json())
#     print('[', timestamp_string(), ']', 'ran!')
#
# if __name__ == '__main__':
#     main()
