import click


@click.command()
@click.argument('user-id')
@click.option('-n', '--namespace', type=click.STRING, show_default=True)
@click.option('-k', '--secret-key')
@click.pass_obj
def cli(obj, user_id, namespace, secret_key):
    """Deletes secret key
    """
    client = obj['client']

    res = client.secret_key.delete(user_id=user_id, namespace=namespace, secret_key=secret_key)
    print(res)
