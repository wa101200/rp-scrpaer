from __future__ import annotations

import click

from rp_to_hevy_cli.embedding import embedding
from rp_to_hevy_cli.hevy import hevy
from rp_to_hevy_cli.port import port_rp_workout_to_hevy
from rp_to_hevy_cli.rp import rp


@click.group()
def cli():
    """RP Hypertrophy to STRONG workout data exporter."""


cli.add_command(rp)
cli.add_command(hevy)
cli.add_command(embedding)
cli.add_command(port_rp_workout_to_hevy)

if __name__ == "__main__":
    cli()
