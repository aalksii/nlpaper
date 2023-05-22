import math

import click

from configs.huggingface_config import (
    model_checkpoint_hf,
)
from trainer import load_trainer


@click.command
@click.option('--input_model_name',
              default=model_checkpoint_hf,
              help='Path to model or name on Hugging Face')
def evaluate(input_model_name):
    trainer = load_trainer(input_model_name)

    eval_results = trainer.evaluate()['eval_loss']
    print(f'>>> (before) Loss: {eval_results:.2f}; '
          f'Perplexity: {math.exp(eval_results):.2f}; '
          f'Model: {input_model_name}')


if __name__ == '__main__':
    evaluate()
