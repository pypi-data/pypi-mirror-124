import click


@click.command()
@click.argument('user-id')
@click.option('-n', '--namespace', type=click.STRING, show_default=True)
@click.pass_obj
def cli(obj, user_id, namespace):
    """Get a users secret key
    """
    client = obj['client']

    res = client.secret_key.get(user_id=user_id, namespace=namespace)
    print(res)
