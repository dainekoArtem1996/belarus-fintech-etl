import csv
import random
import uuid
from datetime import datetime, timedelta
from pathlib import Path


CURRENCIES = ['BYN', 'USD', 'EUR']
MERCHANTS = ['Wildberries_BY', 'Ozon_BY', '21vek', 'Euroopt', 'Yandex_Go']
STATUSES = ['SUSSESS', 'FAILED', 'PENDING']


def generate_one_transaction(
        event_time: datetime,
        custom_user_id: int | None = None,
        is_fraud: bool = False
) -> dict:
    user_id: int | None = custom_user_id if custom_user_id is not None else random.randint(1000, 1500)
    amount = round(random.uniform(5.0, 500.0), 2)
    if not is_fraud and random.random() < 0.05:
        error_type = random.choice(['negative_amount', 'missing_user'])
        if error_type == 'negative_amount':
            amount = -amount
        elif error_type == 'missing_user':
            user_id = None
    return {
        'transaction_id': str(uuid.uuid4()),
        'user_id': random.randint(1000, 1500),
        'amount': round(random.uniform(5.0, 500.0), 2),
        'currency': random.choices(CURRENCIES, weights=[0.7, 0.2, 0.1])[0],
        'merchant': random.choice(MERCHANTS),
        'status': 'SUSSESS' if is_fraud else random.choices(STATUSES, weights = [0.85, 0.10, 0.05])[0],
        'event_time': datetime.now().isoformat(),

    }


def generate_dataset(num_records: int = 1000) -> list[dict]:
    records = []
    current_time = datetime.now() - timedelta(hours=2)
    for _ in range(num_records):
        start_time = datetime.now() - timedelta(hours=2)
        current_time = start_time
        tx = generate_one_transaction(current_time)
        records.append(tx)
        if random.random() < 0.03:
            records.append(tx.copy())
    fraud_time = start_time + timedelta(minutes=30)
    for step in range(8):
        tx_time = fraud_time + timedelta(seconds=step * 5)
        fraud_tx = generate_one_transaction(tx_time, custom_user_id=9999, is_fraud=True)
        records.append(fraud_tx)
    random.shuffle(records)
    return records


def save_to_csv(records: list[dict], filepath: str = 'data/raw_transactions.csv') -> None:
    Path(filepath).parent.mkdir(parents=True, exist_ok=True)
    fieldnames = list(records[0].keys())

    with open(filepath, mode='w', newline='', encoding='utf-8') as file:
        write = csv.DictWriter(file, fieldnames=fieldnames)
        write.writeheader()
        write.writerows(records)

    print(f'Готово! Сохранено {len(records)} записей в файл {filepath}')

if __name__ == '__main__':
    dataset = generate_dataset(1000)
    save_to_csv(dataset)