import math

import click

from configs.huggingface_config import (
    model_checkpoint_hf,
    trained_model_path,
)
from trainer import load_trainer


@click.command
@click.option('--input_model_name',
              default=model_checkpoint_hf,
              help='Path to model or name on Hugging Face')
@click.option('--output_model_name',
              default=trained_model_path,
              help='Path to save the trained model')
def train(input_model_name, output_model_name):
    print(input_model_name, output_model_name)

    trainer = load_trainer(input_model_name)

    eval_results = trainer.evaluate()['eval_loss']
    print(f'>>> (before) Loss: {eval_results:.2f}; '
          f'Perplexity: {math.exp(eval_results):.2f}')

    trainer.train()

    eval_finetuned_results = trainer.evaluate()['eval_loss']
    print(f'>>> (finetuned) Loss: {eval_finetuned_results:.2f}; '
          f'Perplexity: {math.exp(eval_finetuned_results):.2f}')

    div = math.exp(eval_results) / math.exp(eval_finetuned_results)
    print(f'>>> It\'s  {div:.2f} times better!')

    if trained_model_path is not None:
        trainer.save_model(output_model_name)
        print(f'Model {input_model_name} saved to {output_model_name}')


if __name__ == '__main__':
    train()
