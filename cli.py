import click


@click.command()
# @click.option('--filename', prompt="file name", help='file name of the resume')
@click.option('--filename', help='file name of the resume')
def parse(filename):
  click.echo('Parsing %s!' % filename)


if __name__ == '__main__':
  parse()
