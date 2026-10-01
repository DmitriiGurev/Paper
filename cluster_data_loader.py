import requests
import tarfile 
from datetime import datetime
import os
from urllib.request import urlopen
from urllib.parse import urlencode

def unpack_tar(file_name, data_directory):
    with tarfile.open(file_name) as tar:
        file_name = tar.getnames()
        tar.extractall(data_directory)
    
cluster_archive_url = 'https://csa.esac.esa.int/csa-sl-tap/data'
cluster_login_url = 'https://csa.esac.esa.int/csa-sl-tap/login'

request_time_format = '%Y-%m-%dT%H:%M:%SZ'

def download_dataset(data_id: str,
                     start_date: datetime,
                     end_date: datetime,
                     delivery_format: str = 'CEF',
                     delivery_interval: str = 'Daily',
                     *,
                     data_directory: str =''):
    print('Downloading', data_id, 'from', start_date, 'to', end_date, '...')
    
    start_str = start_date.strftime(request_time_format)
    end_str = end_date.strftime(request_time_format)

    query_params = {'RETRIEVAL_TYPE': 'product',
                    'DATASET_ID': data_id,
                    'START_DATE': start_str,
                    'END_DATE': end_str,
                    'DELIVERY_FORMAT': delivery_format,
                    'DELIVERY_INTERVAL': delivery_interval}

    tar_name = 'dataset_' + data_id + '_' + \
        str(start_str).replace(':', '.') + '_' + \
        str(end_date).replace(':', '.') + '.tar'

    url = cluster_archive_url + '?'
    for parameter, value in query_params.items():
        url += parameter + '=' + value + '&'
    url = url[:-1]

    print(url)

    resp = urlopen(url)
    respHtml = resp.read()
    binfile = open(tar_name, "wb")
    binfile.write(respHtml)
    binfile.close()

    unpack_tar(tar_name, data_directory)
    os.remove(tar_name)