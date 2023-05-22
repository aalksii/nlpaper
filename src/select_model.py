import os

import click
import pandas as pd


@click.command
@click.option('--from_files', '-ff',
              help='Path to load evaluation metrics',
              multiple=True)
@click.option('--to_file', '-tf',
              help='Path to save the best model name')
def select(from_files, to_file):
    differences = []

    for from_file in from_files:
        metrics = []
        with open(from_file, 'r') as file:
            strings = file.readlines()
            for s in strings:
                columns = s.split(';')
                metrics.append({
                    'model': columns[0],
                    'loss': float(columns[1]),
                    'ppl': float(columns[2]),
                    'time': float(columns[3])
                })
        differences.append({
            'model': metrics[1]['model'],
            'loss_boost': (metrics[0]['loss']
                           - metrics[1]['loss']) / metrics[0]['loss'],
            'ppl_boost': (metrics[0]['ppl']
                          - metrics[1]['ppl']) / metrics[0]['ppl'],
            'time_boost': (metrics[0]['time']
                           - metrics[1]['time']) / metrics[0]['time'],
            'time': metrics[1]['time']
        })

    df = pd.DataFrame(differences)

    def score(row):
        row['score'] = row['ppl_boost'] + row['time_boost'] + row['time']
        return row

    df = df.apply(score, axis=1)
    print(df)

    os.makedirs(os.path.dirname(to_file), exist_ok=True)
    # df.to_csv(to_file, index=False, sep=';')

    best_model_name = df.iloc[df['score'].argmax()]['model']
    print(f'Best model: {best_model_name}')

    with open(to_file, 'w') as file:
        file.write(best_model_name)


if __name__ == '__main__':
    select()
