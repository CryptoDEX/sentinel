import pytest
import sys
import os
import re
os.environ['SENTINEL_ENV'] = 'test'
os.environ['SENTINEL_CONFIG'] = os.path.normpath(os.path.join(os.path.dirname(__file__), '../test_sentinel.conf'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'lib'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
import config

from cryptodexd import CryptoDexDaemon
from cryptodex_config import CryptoDexConfig


def test_cryptodexd():
    config_text = CryptoDexConfig.slurp_config_file(config.cryptodex_conf)
    network = 'mainnet'
    is_testnet = False
    genesis_hash = u'000005ece8d1964dc550f050f35c45398a4b9dda3158040e0519b9c230b91ed6'
    for line in config_text.split("\n"):
        if line.startswith('testnet=1'):
            network = 'testnet'
            is_testnet = True
            genesis_hash = u'000002731816bccf90ab744347dc894cf484e3826b19f967b8d5f028c204a4f0'

    creds = CryptoDexConfig.get_rpc_creds(config_text, network)
    cryptodexd = CryptoDexDaemon(**creds)
    assert cryptodexd.rpc_command is not None

    assert hasattr(cryptodexd, 'rpc_connection')

    # CryptoDex testnet block 0 hash == 000002731816bccf90ab744347dc894cf484e3826b19f967b8d5f028c204a4f0
    # test commands without arguments
    info = cryptodexd.rpc_command('getinfo')
    info_keys = [
        'blocks',
        'connections',
        'difficulty',
        'errors',
        'protocolversion',
        'proxy',
        'testnet',
        'timeoffset',
        'version',
    ]
    for key in info_keys:
        assert key in info
    assert info['testnet'] is is_testnet

    # test commands with args
    assert cryptodexd.rpc_command('getblockhash', 0) == genesis_hash
