import click
import requests

from configs.server_config import rest_api_port


@click.group('cli')
@click.pass_context
@click.argument('text')
def cli(ctx, text):
    ctx.obj = text


@cli.command('fill_mask')
@click.pass_context
def request_fill_mask(ctx):
    x = requests.post(f'http://127.0.0.1:{rest_api_port}/api/fill_mask',
                      json={'x': ctx.obj})
    print('Filling mask:', x.text)


@cli.command('summarize')
@click.pass_context
def request_summarize(ctx):
    x = requests.post(f'http://127.0.0.1:{rest_api_port}/api/summarize',
                      json={'x': ctx.obj})
    print('Summarization:', x.text)


if __name__ == '__main__':
    cli(prog_name='cli')
