import os
import json
from collections import defaultdict

DATA_FILE = 'finances.json'

def analyze(data):

    income_total = 0
    expense_total = 0
    categories = defaultdict(float)

    for item in data:
        if item['type'] == 'income':
            income_total += item['amount']
        elif item['type'] == 'outcome':
            expense_total += abs(item['amount'])
            categories[item['description']] += abs(item['amount'])

    print(f"💰 Income: {income_total}")
    print(f"💸 Outcome: {expense_total}")
    print(f"📉 Balance: {income_total - expense_total}\n")

    print("📊 Top categories from outcome:")
    for category, total in sorted(categories.items(), key = lambda x: x[1], reverse=True)[:3]:
        print(f'- {category}: {total} $.')



def load_file():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

def save_data(data):
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def calculate_balance(data):
    return sum(item['amount'] for item in data)

def show_history(data):
    if not data:
        print('No data yet.')
        return
    for item in data:
        print(f"{item['type']}: {item['amount']} $ | {item['description']}")

def add_record(data):
    while True:
        record_type = input('Type the name of operation (income/outcome): ').strip().lower()
        if record_type in ['income', 'outcome']:
            break
        print('Error. Type "income" or "outcome".')

    try:
        amount = float(input('Put down an amount: '))
        if record_type == 'outcome':
            amount = -abs(amount)
    except ValueError:
        print('Error. Put down the correct amount.')
        return

    description = input('Comment: ').strip()
    data.append({
        'type': record_type,
        'amount': amount,
        'description': description
    })
    save_data(data)
    print('Updated!')

def main():
    data = load_file()
    print('Welcome to Your Finances!')

    while True:
        print('\nChoose the operation: ')
        print('1. Add record.')
        print('2. Show balance.')
        print('3. Show history.')
        print('4. Analyze expenses.')
        print('5. Leave.')

        choice = input('Your choice is ')

        if choice == '1':
            add_record(data)
        elif choice == '2':
            balance = calculate_balance(data)
            print(f'Your current balance is {balance} $.')
        elif choice == '3':
            show_history(data)
        elif choice == '4':
            analyze(data)
        elif choice == '5':
            print('Bye!')
            break
        else:
            print('Wrong code of operation. Try again.')


if __name__ == '__main__':
    main()



