# -*- coding: utf8 -*-
import pytest


from ethereum import utils
from ethereum import tester
from ethereum.utils import sha3, privtoaddr
from ethereum.tester import TransactionFailed

library_path = "raiden/smart_contracts/IterableMappingCMC.sol"

registry_path = "raiden/smart_contracts/Registry.sol"


def test_registry():
    s = tester.state()
    assert s.block.number < 1150000
    s.block.number = 1158001
    assert s.block.number > 1150000
    lib_c = s.abi_contract(None, path=library_path, language="solidity")
    c = s.abi_contract(None, registry_path, language="solidity", libraries={'IterableMappingCMC': lib_c.address.encode('hex')})

    c.addAsset(sha3('asset')[:20])
    c.addAsset(sha3('address')[:20])
    # if address already exists, throw
    with pytest.raises(TransactionFailed):
        c.addAsset(sha3('asset')[:20])

    cmc = c.channelManagerByAsset(sha3('asset')[:20])
    assert cmc == sha3('asset')[:20].encode('hex')
    # if address does not exist, throw
    with pytest.raises(TransactionFailed):
        c.channelManagerByAsset(sha3('mainz')[:20])

    adrs = c.assetAddresses()
    assert len(adrs) == 2
    assert adrs[0] == sha3('asset')[:20].encode('hex')
    assert adrs[1] == sha3('address')[:20].encode('hex')
