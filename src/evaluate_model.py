import math
import os
import time

import click

from configs.huggingface_config import (
    model_checkpoint_hf,
    eval_metrics_path
)
from trainer import load_trainer


@click.command
@click.option('--input_model_name', '-in',
              default=model_checkpoint_hf,
              help='Path to model or name on Hugging Face')
@click.option('--to_file', '-out',
              default=eval_metrics_path,
              help='Path to save evaluation metrics')
def evaluate(input_model_name, to_file):
    trainer = load_trainer(input_model_name,
                           input_model_name,
                           push_to_hub=False)

    start_time = time.time()
    loss = trainer.evaluate()['eval_loss']
    diff_time = time.time() - start_time
    ppl = math.exp(loss)

    print(f'>>> Loss: {loss:.2f}; '
          f'Perplexity: {ppl:.2f}; '
          f'Time: {diff_time:.2f}; '
          f'Model: {input_model_name}')

    # os.makedirs(to_file, exist_ok=True)
    with open(to_file, 'a+') as file:
        file.write(f'{input_model_name};{loss};{ppl};{diff_time}\n')


if __name__ == '__main__':
    evaluate()
