import ast
import json
import requests
from datetime import datetime
from ..utils.format_num import format_number
from ..utils.get_find_key import find_key
from server.App.Storage.config import TON_IO_API, TON_CENTER_API

class GeckoRequest:
    def gecko_get_pools(self, page):
        """
        get a list of all tokens by page

        there are 20 tokens in the page
        maximum 10 pages
        """
        with requests.Session() as session:
            response = session.get(f'https://api.geckoterminal.com/api/v2/networks/ton/pools?page={page}')
            return response.json()

    def get_gecko_jetton(self, address):
        """We get from jetton address -> jetton master and from it we get information about the token and other things"""
        with requests.Session() as session:
            response_address = session.get(f'https://api.geckoterminal.com/api/v2/networks/ton/pools/{address}/info')
            req = response_address.json()['data']
            for responseData in req:
                if responseData['attributes']['address'] != 'EQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAM9c': #skip usdt
                    address = responseData['attributes']['address'] # we found the right address and complete the cycle
                    break
            response = session.get(f'https://api.geckoterminal.com/api/v2/networks/ton/tokens/{address}/pools?page=1')
            return response.json()

    def get_info_jetton(self, address):
        """unpack the address in the format 0:... to get information about the photo, this is necessary for getting photos, etc."""
        with requests.Session() as toncenter_session:
            toncenter_session.headers.update({
                "Authorization": f"Bearer {TON_CENTER_API}"
            })
            request_unpack = toncenter_session.get(
                url=f'https://toncenter.com/api/v2/unpackAddress?address={address}'
            )
            unpacked_address = request_unpack.json().get('result')

        with requests.Session() as tonapi_session:
            tonapi_session.headers.update({
                "Authorization": f"Bearer {TON_IO_API}"
            })
            result = tonapi_session.get(
                url=f"https://tonapi.io/v2/jettons/{unpacked_address}"
            )
            return result.json()

class TonAPI(GeckoRequest):
    async def get_pools(self, page):
        return self.gecko_get_pools(page=page)

    def get_gecko_jetton_info(self, address):
        """
        get information about the selected token,

        localhost/JettonView/<address>
        """
        result = self.get_gecko_jetton(address)
        array = []

        for data in result['data']:
            attributes = data['attributes']

            price_change_percentage = ast.literal_eval(find_key(data, 'price_change_percentage'))
            result_two = self.get_info_jetton(address)
            img = find_key(result_two, 'image')
            total_supply = find_key(result_two, 'total_supply')
            is_scam = find_key(result_two, 'is_scam')
            delta = datetime.strptime(attributes['pool_created_at'], "%Y-%m-%dT%H:%M:%SZ") - datetime.utcnow()

            array.append({
                "jettonVolumeStringAll": attributes['volume_usd']['h24'],
                "jettonLiqStringAll": attributes['reserve_in_usd'],
                "jettonFDVStringAll": attributes['fdv_usd'],
                "jettonSupplyAll": total_supply,
                'jettonAddressString': address[:6] + "...." + address[-6:],

                "jettonIsScam": is_scam,
                "jettonVolume": format_number(attributes['volume_usd']['h24']),
                "jettonLiq": format_number(attributes['reserve_in_usd']),
                "jettonFDV": format_number(attributes['fdv_usd']),
                "jettonPrice": str(attributes['base_token_price_usd'])[:7],
                "jettonH24": attributes['price_change_percentage']['h24'],
                "jettonCreated": abs(delta.days),
                "jettonAddress": attributes['address'],
                "jettonName": attributes['name'],
                "jettonColor": 'red' if '-' in attributes['price_change_percentage']['h24'] else 'green',
                'jettonImage': 'https://upload.wikimedia.org/wikipedia/commons/d/d6/Gold_coin_icon.png' if img == 'missing.png' else img,
                "resultJetton": result_two,
                "jettonStatic": price_change_percentage,
                "jettonStaticColor": {key: 'green' if float(value) > 0 else 'red' for key, value in price_change_percentage.items()}

            })
            break

        return array

    def get_pool(self, sort=None):
        '''
        sort by selected categories

        example url: https://zelya.xyz/getPage/<sort>
        sort: [jettonVolumeStringAll, jettonFDVStringAll, jettonLiqStringAll, jettonSupplyAll, jettonPrice]
        '''
        with open('server/App/Storage/data.json', 'r', encoding='utf-8') as file:
            data = json.load(file)

            if sort in ['jettonVolumeStringAll', 'jettonFDVStringAll', 'jettonLiqStringAll', 'jettonSupplyAll', 'jettonPrice']:
                return sorted(
                    data,
                    key=lambda x: float(x[sort]) if x.get(sort) is not None else 0,
                    reverse=True
                )
        return data