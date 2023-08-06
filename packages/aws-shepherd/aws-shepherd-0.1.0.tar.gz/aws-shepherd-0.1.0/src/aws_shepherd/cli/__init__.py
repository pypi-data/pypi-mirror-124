import os
from zipfile import ZipFile

import boto3
import argparse
import tempfile
from os import path
from pyngrok import ngrok
from sys import argv
from pathlib import Path
from rich import print


script_dir = path.dirname(path.realpath(__file__))

_verbose: bool = False


def _debug(msg):
    if _verbose:
        print(f'[bold green]DEBUG[/bold green] {msg}')


def _info(msg):
    print(f'[bold blue]INFO[/bold blue] {msg}')


def mount(args):
    client = boto3.client('lambda')
    waiter = client.get_waiter('function_updated')

    # create new lambda handler
    with tempfile.TemporaryDirectory() as tmpdir:
        lambda_path = path.join(tmpdir, 'lambda.zip')

        _debug("Creating lambda zip file")
        with ZipFile(lambda_path, 'w') as zip:
            lambda_content = Path(path.join(script_dir, '../lambda/index.py')).read_text()
            zip.writestr('index.py', lambda_content)

        lambda_zip_bytes = Path(lambda_path).read_bytes()

        _info('Updating function code')
        client.update_function_code(
            FunctionName=args.function_name,
            ZipFile=lambda_zip_bytes
        )

        _debug('Waiting for code to have been updated')
        waiter.wait(
            FunctionName=args.function_name
        )

        _info('Updating function configuration')
        client.update_function_configuration(
            FunctionName=args.function_name,
            Handler='index.handler'
        )


def start(args):
    client = boto3.client('lambda')
    waiter = client.get_waiter('function_updated')

    # start ngrok tunnel
    _debug('Connecting to ngrok')
    http_tunnel = ngrok.connect(addr=args.port)

    _info(f'Pointing the lambda at our tunnel [underline]{http_tunnel.public_url}[/underline]')
    existing_configuration = client.get_function_configuration(
        FunctionName=args.function_name
    )
    lambda_env = existing_configuration['Environment']['Variables']
    lambda_env['NGROK_URL'] = http_tunnel.public_url
    client.update_function_configuration(
        FunctionName=args.function_name,
        Environment={
            'Variables': lambda_env
        }
    )

    waiter.wait(
        FunctionName=args.function_name
    )

    _debug('Loading handler')
    os.environ['SHEPHERD_MODULE'] = args.python_handler

    from aws_shepherd.local import app

    _info('Loading lambda handler')
    app.run(host='0.0.0.0', port=args.port)


parser = argparse.ArgumentParser()
parser.add_argument('-v', '--verbose', default=False, help='Show debug logs', action='store_true')

command_parsers = parser.add_subparsers()

mount_parser = command_parsers.add_parser('mount')
mount_parser.set_defaults(func=mount)
mount_parser.add_argument('function_name')

start_parser = command_parsers.add_parser('start')
start_parser.set_defaults(func=start)
start_parser.add_argument('-p', '--port', default=8888)
start_parser.add_argument('function_name')
start_parser.add_argument('python_handler')


def main():
    args = parser.parse_args(argv[1:])

    global _verbose
    _verbose = args.verbose

    args.func(args)


if __name__ == '__main__':
    main()
