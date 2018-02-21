#!/usr/bin/env python3

# python setup.py sdist --format=zip,gztar

from setuptools import setup
import os
import sys
import platform
import imp
import argparse

with open('contrib/requirements/requirements.txt') as f:
    requirements = f.read().splitlines()

with open('contrib/requirements/requirements-hw.txt') as f:
    requirements_hw = f.read().splitlines()

version = imp.load_source('version', 'lib/version.py')

if sys.version_info[:3] < (3, 4, 0):
    sys.exit("Error: Electrum requires Python version >= 3.4.0...")

data_files = ['contrib/requirements/' + r for r in ['requirements.txt', 'requirements-hw.txt']]

if platform.system() in ['Linux', 'FreeBSD', 'DragonFly']:
    parser = argparse.ArgumentParser()
    parser.add_argument('--root=', dest='root_path', metavar='dir', default='/')
    opts, _ = parser.parse_known_args(sys.argv[1:])
    usr_share = os.path.join(sys.prefix, "share")
    if not os.access(opts.root_path + usr_share, os.W_OK) and \
       not os.access(opts.root_path, os.W_OK):
        if 'XDG_DATA_HOME' in os.environ.keys():
            usr_share = os.environ['XDG_DATA_HOME']
        else:
            usr_share = os.path.expanduser('~/.local/share')
    data_files += [
        (os.path.join(usr_share, 'applications/'), ['electrum-arg.desktop']),
        (os.path.join(usr_share, 'pixmaps/'), ['icons/electrum-arg.png'])
    ]

setup(
    name="Electrum-Argentum",
    version=version.ELECTRUM_VERSION,
    install_requires=requirements,
    extras_require={
        'hardware': requirements_hw,
    },
    packages=[
        'electrum_arg',
        'electrum_arg_gui',
        'electrum_arg_gui.qt',
        'electrum_arg_plugins',
        'electrum_arg_plugins.audio_modem',
        'electrum_arg_plugins.cosigner_pool',
        'electrum_arg_plugins.email_requests',
        'electrum_arg_plugins.hw_wallet',
        'electrum_arg_plugins.keepkey',
        'electrum_arg_plugins.labels',
        'electrum_arg_plugins.ledger',
        'electrum_arg_plugins.trezor',
        'electrum_arg_plugins.digitalbitbox',
        'electrum_arg_plugins.trustedcoin',
        'electrum_arg_plugins.virtualkeyboard',
    ],
    package_dir={
        'electrum_arg': 'lib',
        'electrum_arg_gui': 'gui',
        'electrum_arg_plugins': 'plugins',
    },
    package_data={
        'electrum_arg': [
            'servers.json',
            'servers_testnet.json',
            'currencies.json',
            'checkpoints.json',
            'checkpoints_testnet.json',
            'www/index.html',
            'wordlist/*.txt',
            'locale/*/LC_MESSAGES/electrum.mo',
        ]
    },
    scripts=['electrum-arg'],
    data_files=data_files,
    description="Lightweight Argentum Wallet",
    author="Thomas Voegtlin",
    author_email="thomasv@electrum.org",
    license="MIT Licence",
    url="http://www.github.com/argentumproject/electrum-arg",
    long_description="""Lightweight Argentum Wallet"""
)
