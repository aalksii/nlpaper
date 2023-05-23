import os

import click

from configs.huggingface_config import (
    model_checkpoint_hf,
    trained_model_path,
)
from trainer import load_trainer


@click.command
@click.option('--input_model_name', '-in',
              default=model_checkpoint_hf,
              help='Path to model or name on Hugging Face')
@click.option('--output_model_path', '-out',
              default=trained_model_path,
              help='Path to save the trained model')
def train(input_model_name, output_model_path):
    print(f'Input model: {input_model_name}, output model: {output_model_path}')

    trainer = load_trainer(input_model_name, output_model_path)
    trainer.train()

    os.makedirs(output_model_path, exist_ok=True)
    if output_model_path is not None:
        trainer.save_model(output_model_path)
        print(f'Saved model {input_model_name} to {output_model_path}')


if __name__ == '__main__':
    train()
