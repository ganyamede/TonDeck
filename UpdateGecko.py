from server.App.Web3.tonapi import GeckoRequest
from server.App.utils.format_num import format_number
from server.App.utils.get_find_key import find_key
import asyncio
import json

async def update_info():
    '''
    Due to API limitations, we will update information continuously every 300 seconds.

    We write information to Storage/data.json of all top tokens and then work with them
    '''
    while True:
        array = []
        for indexPage in range(1, 11):
            for index, data in enumerate(GeckoRequest().gecko_get_pools(indexPage)['data']): # get all token in pools
                # gecko
                attributes = data['attributes']
                address = attributes['address'] # get address
                result = GeckoRequest().get_info_jetton(address) # get other info, for image/supply/etc.
                img = find_key(result, 'image') # get image
                total_supply = find_key(result, 'total_supply') # get supplay
                name = attributes['name'] # get jetton name
                if name.replace(' ', '').split('/')[1] == 'TON': # skip interest pools, we are interested in tokens

                    array.append({
                        "jettonVolumeStringAll": attributes['volume_usd']['h24'], # Valume, example: 35.93m
                        "jettonLiqStringAll": attributes['reserve_in_usd'], # Liq, example: 35.93m
                        "jettonFDVStringAll": attributes['fdv_usd'], # market cuo, example: 35.93m
                        "jettonSupplyAll": total_supply, # All coins of the token
                        "jettonVolume": format_number(attributes['volume_usd']['h24']), # the same as the previous one but the full number, example: 35930239
                        "jettonLiq": format_number(attributes['reserve_in_usd']), # the same as the previous one but the full number
                        "jettonFDV": format_number(attributes['fdv_usd']), # the same as the previous one but the full number
                        "jettonPrice": str(attributes['base_token_price_usd'])[:7], #price token
                        "jettonH24": attributes['price_change_percentage']['h24'],  #Token statistics for 24 hours in percentage
                        "jettonAddress": attributes['address'], # token address to switch to another tab
                        "jettonName": attributes['name'], # token names
                        "jettonColor": 'red' if '-' in attributes['price_change_percentage']['h24'] else 'green', #We set the color depending on the trade, red - in Minsk, green - in the plus
                        'jettonImage': 'https://upload.wikimedia.org/wikipedia/commons/d/d6/Gold_coin_icon.png' if
                        img == 'missing.png' else img, # token image
                        "resultJetton": result # other information
                    })

                await asyncio.sleep(1)
            print(indexPage, True)

        with open('server/App/Storage/data.json', 'w', encoding='utf-8') as file:
            json.dump(array, file, ensure_ascii=False, indent=4)

        await asyncio.sleep(500)


async def main():
    await update_info()

asyncio.run(main())

