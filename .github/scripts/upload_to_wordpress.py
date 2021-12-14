#!/usr/bin/env python3

import base64
import os
import requests
import sys


def create_headers(authorization):
    headers = requests.structures.CaseInsensitiveDict()
    headers["Authorization"] = "Basic " + base64.b64encode(authorization.encode("ASCII")).decode("ASCII")
    return headers


def get_media(base_url, authorization):
    headers = create_headers(authorization)

    r = requests.get(f"https://{base_url}/wp-json/wp/v2/media", headers=headers)
    return r.json()


def delete_media(base_url, authorization, id):
    headers = create_headers(authorization)

    r = requests.delete(f"https://{base_url}/wp-json/wp/v2/media/{id}", headers=headers, data={"force": True})
    return r.json()


def upload_media(base_url, authorization, local_file, remote_name):
    headers = create_headers(authorization)
    headers["Content-Disposition"] = f"form-data; filename={remote_name}"
    headers["Content-Type"] = "application/x-www-form-urlencoded"

    with open(local_file, "rb") as f:
        data = f.read()

    r = requests.post(f"https://{base_url}/wp-json/wp/v2/media", headers=headers, data=data)
    return r.json()


if __name__ == "__main__":
    base_url = sys.argv[1]
    local_file = sys.argv[2]
    remote_name = sys.argv[3]

    authorization = os.environ["AUTHORIZATION"]

    media = get_media(base_url, authorization)
    its_id = [_["id"] for _ in media if _["source_url"] == f"https://{base_url}/wp-content/uploads/{remote_name}"]
    if its_id:
        delete_media(base_url, authorization, its_id[0])
    upload_media(base_url, authorization, local_file, remote_name)
