import functools
from pathlib import Path
from typing import Union, List, Dict, Optional, Callable, Tuple

import yaml
import requests


def get_ssl_files(cloud_directory: Path):
    if (cloud_path := cloud_directory / 'cloud_config.yaml').exists():
        with open(cloud_path) as cloud_file:
            cloud_config = yaml.safe_load(cloud_file)
        cloud_name = cloud_config["cloud"]["cloud_name"]
        cert_subpath = f'cloud-{cloud_name}/crypto/sysop.crt'
        key_subpath = f'cloud-{cloud_name}/crypto/sysop.key'
        ca_subpath = f'cloud-{cloud_name}/crypto/sysop.ca'
    else:
        cert_subpath = 'sysop.crt'
        key_subpath = 'sysop.key'
        ca_subpath = 'sysop.ca'
    return (cloud_directory / subpath for subpath in
        (cert_subpath, key_subpath, ca_subpath)
    )

def get_service(
        url: str,
        cloud_directory: Path,
):
    *certkey, ca_path = get_ssl_files(cloud_directory)
    resp = requests.get(url, cert=certkey, verify=ca_path)
    return resp

def post_service(
        url: str,
        cloud_directory: Path,
        json: Union[Dict, List] = None,
        text: str = ''
):
    *certkey, ca_path = get_ssl_files(cloud_directory)
    if json:
        resp = requests.post(url, json=json, cert=certkey, verify=ca_path)
    elif text:
        resp = requests.post(url, text=text, cert=certkey, verify=ca_path)
    else:
        resp = requests.post(url, cert=certkey, verify=ca_path)
    return resp

def delete_service(
        url: str,
        cloud_directory: Path,
        params: Optional[Dict[str, str]] = None,
):
    *certkey, ca_path = get_ssl_files(cloud_directory)

    resp = requests.delete(url, params=params, cert=certkey, verify=ca_path)
    return resp
