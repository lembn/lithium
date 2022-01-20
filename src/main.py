import click
import commands


@click.group(
    help="""
    `lithium` produces models of flight times for drones from the mass and capacity of the drone's battery.
    These models can be compared to measure the flight time performance of a drone, or tested against to estimate
    flight time for a drone with a given battery.
    """
)
def cli():
    pass


if __name__ == "__main__":
    cli.add_command(commands.calculate)  # TODO test
    cli.add_command(commands.edit)  # TODO test
    cli.add_command(commands.estimate)  # TODO test
    cli.add_command(commands.generate)  # TODO TESTING
    cli.add_command(commands.graph)  # TODO test
    cli.add_command(commands.show)  # TODO test
    cli(prog_name="lithium")
