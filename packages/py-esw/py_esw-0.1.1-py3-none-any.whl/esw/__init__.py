import requests
import os
import time


class ESWrapper:
    origin_tx = ['account', 'txlist', 0, 99999999, 'asc']

    def __init__(self, network, eth_api):

        self.url = network
        self.api = eth_api

    def get_origin_txn(self, account):
        origin_txn = self._call(*self.origin_tx, account)[0]
        hash = origin_txn['hash']
        block = origin_txn['blockNumber']
        time = origin_txn['timeStamp']
        creator = origin_txn['from']

        return {'hash': hash, 'block': block, 'time': time, 'creator': creator}

    def get_origin_block(self, contract):
        return self.get_origin_txn(contract)['block']

    def get_tx(self, contract, function=None):
        call = self._call('account', 'txlist', start=self.get_origin_block(contract), end=99999999999,
                          account=contract, sort='asc', function=function)
        return call

    def get_from(self, contract, function=None):
        call = self._call('account', 'txlist', start=self.get_origin_block(contract), end=99999999999,
                          account=contract, sort='asc', function=function)
        call = list(set(call[i]['from'] for i in range(len(call))))
        return call

    def _call(self, module, action, start, end, sort, account, function=None):
        result = []
        while True:
            url = f'{self.url}module={module}&action={action}&address={account}&startblock={start}&endblock={end}&sort={sort}' \
                  f'&apikey={self.api}'

            response = requests.get(url).json()['result']

            for r in response:
                if function:
                    if str(r['input']).startswith(function):
                        result.append(r)
                else:
                    result.append(r)

            if len(response) < 10000:
                break
            else:
                start = result[-1]['blockNumber']
                time.sleep(1)

        return result
