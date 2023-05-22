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
    trainer.train()


if __name__ == '__main__':
    train()
