import click


@click.command()
@click.argument('user-id')
@click.option('-n', '--namespace', type=click.STRING, show_default=True)
@click.option('-e', '--expiry-time')
@click.option('-k', '--secret-key')
@click.pass_obj
def cli(obj, user_id, namespace, expiry_time, secret_key):
    """Create new secret key
    """
    client = obj['client']

    res = client.secret_key.create(user_id=user_id, namespace=namespace, expiry_time=expiry_time, secret_key=secret_key)
    print(res)
