import click


@click.group()
def cli():
    """RP Hypo to STRONG workout data exporter."""


@cli.command()
def extract():
    """Extract workout data from RP Hypo."""
    click.echo("Extract: not yet implemented")


@cli.command()
def transform():
    """Transform extracted data to STRONG format."""
    click.echo("Transform: not yet implemented")


@cli.command()
def export():
    """Run full pipeline: extract, transform, and export to CSV."""
    click.echo("Export: not yet implemented")


@cli.command()
def status():
    """Query Dagster for pipeline run status."""
    click.echo("Status: not yet implemented")


print("CLI loaded")
