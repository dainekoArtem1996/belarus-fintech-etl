import csv
from datetime import datetime
from pathlib import Path
import requests


NBRB_API_URL = 'https://api.nbrb.by/exrates/rates'
CURRENCY_IDS = {
    'USD': 431,
    'EUR': 451,
}


def get_currency_rate(currency_code: str) -> dict:
    cur_id = CURRENCY_IDS[currency_code]
    url = f'{NBRB_API_URL}/{cur_id}'
    headers = {
        "User-Agent": "BelarusFintechETL/1.0 (+https://github.com)",
        "Accept": "application/json",
    }

    response = requests.get(url, headers=headers, timeout=10)
    response.raise_for_status()
    if not response.text.strip():
        raise RuntimeError(
            f"Сервер вернул пустой ответ! Код: {response.status_code}, URL: {response.url}"
        )
    data = response.json()
    
    return {
        'currency': data['Cur_Abbreviation'],
        'rate': data['Cur_OfficialRate'],
        'scale': data['Cur_Scale'],
        'date': data['Date'][:10]
    }


def fetch_all_rates() -> list[dict]:
    rates = []

    for code in CURRENCY_IDS:
        rate_info = get_currency_rate(code)
        rates.append(rate_info)

    first_rate = rates[0]
    today_str = first_rate['date'] if rates else datetime.now().strftime('%Y-%m-%d')

    rates.append({
        'currency': 'BYN',
        'rate': 1.0,
        'scale': 1,
        'date': today_str
    })
    return rates


def save_rates_to_csv(rates: list[dict], filepath: str = 'data/currency_rates.csv') -> None:
    Path(filepath).parent.mkdir(parents=True, exist_ok=True)
    fieldname = ['currency', 'rate', 'scale', 'date']

    with open(filepath, mode='w', newline='', encoding='utf-8') as file:
        write = csv.DictWriter(file, fieldnames=fieldname)
        write.writeheader()
        write.writerows(rates)
    print(f'Готово! Курсы валют ({len(rates)} шт.) сохранены в {filepath}')


if __name__ == '__main__':
    all_rates = fetch_all_rates()
    for r in all_rates:
        print(r)
    save_rates_to_csv(all_rates)




