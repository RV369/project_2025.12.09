import argparse
import csv
from collections import defaultdict

from tabulate import tabulate


def main():
    parser = argparse.ArgumentParser(
        description='Generate performance report from employee CSV files.',
    )
    parser.add_argument(
        '--files',
        nargs='+',
        required=True,
        help='List of CSV files to process',
    )
    parser.add_argument(
        '--report',
        required=True,
        help='Name of the report (for display purposes)',
    )
    args = parser.parse_args()
    # Словарь для накопления данных: position -> список performance
    position_performance = defaultdict(list)
    # Чтение всех указанных файлов
    for filename in args.files:
        try:
            with open(filename, mode='r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    position = row['position']
                    performance = float(row['performance'])
                    position_performance[position].append(performance)
        except FileNotFoundError:
            print(f'Warning: File {filename} not found. Skipping.')
        except KeyError as e:
            print(
                f'Warning: Missing expected column {e} in file {filename}. '
                f'Skipping row(s).',
            )
        except ValueError as e:
            print(
                f'Warning: Invalid performance value in file {filename}: {e}. '
                f'Skipping row(s).',
            )
    # Вычисление средней эффективности по каждой позиции
    report_data = []
    for position, performances in position_performance.items():
        avg_performance = sum(performances) / len(performances)
        report_data.append([position, round(avg_performance, 2)])
    # Сортировка по средней эффективности по убыванию
    report_data.sort(key=lambda x: x[1], reverse=True)
    # Вывод отчёта
    print(f'\nReport: {args.report}')
    print(
        tabulate(
            report_data,
            headers=['Position', 'Average Performance'],
            tablefmt='grid',
        ),
    )


if __name__ == '__main__':
    main()
