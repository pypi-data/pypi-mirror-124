#!/usr/local/bin/python3

# SPDX-FileCopyrightText: 2021 Joshua Mulliken <joshua@mulliken.net>
#
# SPDX-License-Identifier: GPL-3.0-only

from appdirs import user_config_dir
import os
import hashlib
import sys
import argparse
import json
from argparse import Namespace
from pathlib import Path
import requests
import select

APP_NAME = "sh_paste"
CONFIG_DIR = user_config_dir(APP_NAME)
CONFIG_FILE = "source_hut_token"
SR_HT_PASTE_URL = "https://paste.sr.ht/query"


class NoTokenException(Exception):
    pass


class BadTokenException(Exception):
    pass


def get_username(token):
    response = requests.post(SR_HT_PASTE_URL, headers={
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }, json={
        "query": "{ me { canonicalName } }"
    })

    if response.status_code != 200:
        raise BadTokenException("The token cannot be validated")

    return response.json().get("data").get("me").get("canonicalName")


def write_token(token):
    config_path = Path(CONFIG_DIR)

    if not config_path.exists():
        os.makedirs(config_path)

    config_file = Path(os.path.join(config_path, CONFIG_FILE))

    with open(config_file, "w") as token_file:
        token_file.write(token)


def read_token() -> str:
    config_path = Path(CONFIG_DIR)

    if not config_path.exists():
        os.makedirs(config_path)

    config_file = Path(os.path.join(config_path, CONFIG_FILE))

    if config_file.exists():
        with open(config_file, "r") as token_file:
            token = token_file.read()
            username = get_username(token)

            return token, username
    else:
        raise NoTokenException("The token was not found in your config." +
                               " Please login. See the --help command")


def login(args: Namespace):
    if args.token:
        get_username(args.token)

        write_token(args.token)
    else:
        print("Please navigate to: https://meta.sr.ht/oauth2/personal-token" +
              " to generate a personal auth token")
        print("Grant string: \"paste.sr.ht/PROFILE paste.sr.ht/PASTES:RW\"")

        token = input(": ")
        get_username(token)

        write_token(token)


def upload(args: Namespace):
    token, username = read_token()

    file_text = ""
    while sys.stdin in select.select([sys.stdin], [], [], 0)[0]:
        file_line = sys.stdin.readline()
        if file_line:
            file_text += file_line
        else:
            break
    else:
        print("No input from stdin. Exiting...")
        exit(1)

    if args.filename:
        file_name = args.filename
    else:
        hash = hashlib.sha1()
        hash.update(file_text.encode('utf-8'))
        file_name = hash.hexdigest()[:7]

    visibility = "UNLISTED"
    if args.visibility:
        if "PUBLIC" == args.visibility.upper():
            visibility = "PUBLIC"
        elif "PRIVATE" == args.visibility.upper():
            visibility = "PRIVATE"

    headers = {
        "Authorization": f"Bearer {token}",
    }
    query = {
        "query": """
        mutation create($file: Upload!, $visibility: Visibility!){
            create( files: [$file], visibility: $visibility ) {
                id
                created
                visibility
            }
        }
        """,
        "variables": {
            "file": None,
            "visibility": visibility
        }
    }
    files = {
        "operations": (None, json.dumps(query)),
        "map": (None, json.dumps({
            "0": ["variables.file"]
        })),
        "0": (file_name, file_text, "text/plain")
    }

    response = requests.post(SR_HT_PASTE_URL, headers=headers,
                             files=files)

    if response.status_code != 200:
        print(f"Failed to upload file: {response.json()}")
        print(response.request.body)
        exit(2)

    file_id = response.json().get("data").get("create").get("id")

    print(f"https://paste.sr.ht/{username}/{file_id}")


def cli():
    parser = argparse.ArgumentParser(description='paste.sr.ht' +
                                     ' command line utility')
    parser.add_argument('-f', '--filename', help='Optional filename')
    parser.add_argument('-v', '--visibility', help="PUBLIC, PRIVATE, or UNLISTED")
    parser.set_defaults(func=upload)
    subparsers = parser.add_subparsers()

    # Add additional commands for the tool
    login_parser = subparsers.add_parser('login')
    login_parser.description = 'Login to paste.sr.ht with your personal' + \
                               ' access token'
    login_parser.add_argument('-t', '--token', help='personal access token' +
                              ' from https://meta.sr.ht/oauth2')
    login_parser.set_defaults(func=login)

    args = parser.parse_args()
    args.func(args)