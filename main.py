import asyncio
import platform
import logging
import sys
from datetime import datetime, timedelta

import aiohttp


today = datetime.now()
today = today.strftime("%d.%m.%Y")

urls = [f'https://api.privatbank.ua/p24api/exchange_rates?json&date={today}', ]

def urls_adder():
    try:
        amount = int(sys.argv[1])
        day = datetime.now()
        if amount > 10:
            print('You can see maximum 10 days. Please write 10 or less.')
        elif amount > 1:
            while amount > 1:
                previous_day = day - timedelta(days=amount-1)
                previous_day = previous_day.strftime("%d.%m.%Y")
                url = f'https://api.privatbank.ua/p24api/exchange_rates?json&date={previous_day}'
                urls.append(url)
                amount -= 1
    except ValueError:
        print(f'{sys.argv[1]} is not a number. Please try again.')
    except IndexError:
        pass

def format_showing(today, currency, sale, purchase):
    return {f"{today}": {f"{currency}": {"sale": f"{sale}", "purchase": f"{purchase}"}}}

async def main():
    async with aiohttp.ClientSession() as session:
        for url in urls:
            logging.info(f'Starting: {url}')
            try:
                async with session.get(url) as response:
                    if response.status == 200:
                        html = await response.json()
                        for item in html['exchangeRate']:
                            if item['currency'] in ('USD', 'EUR'):
                                print(format_showing(html['date'], item['currency'],
                                                     item['saleRate'], item['purchaseRate']))

                    else:
                        logging.error(f"Error status {response.status} for {url}")
            except aiohttp.ClientConnectorError as e:
                logging.error(f"Connection error {url}: {e}")


if __name__ == "__main__":
    if platform.system() == 'Windows':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    urls_adder()
    r = asyncio.run(main())


