import os,sys,inspect
current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

from tools.http import http
from pathlib import Path
from brazilnum.cnpj import format_cnpj
from brazilnum.cpf import format_cpf
import base64
import json
import re


def ixcreqs(request_data, payload=None, output=None):
    base_url = request_data['base_url']
    headers = request_data['headers']
    endpoint = request_data['endpoint']

    req = http(base_url, headers=headers)

    if request_data['method'] == 'POST':
        res = req.post(endpoint=endpoint, output=output, payload=payload)
    if request_data['method'] == 'GET':
        res = req.get(endpoint=endpoint, output=output, payload=payload)

    return res

def data2PDF(request_data, file_name, path_to_file):
    
    full_name = "{}/{}.pdf".format(path_to_file,file_name)

    pdf = open(full_name, "wb")
    pdf.write(request_data)
    pdf.close()

    if Path(full_name).is_file():
        return "{}.pdf".format(file_name)
    else:
        return False
        
def cpfFormater(data):
    data = re.sub('[^A-Za-z0-9]+', '', data)

    if len(data) == 11:
        return format_cpf(data)
    if len(data) == 14:
        return format_cnpj(data)
    