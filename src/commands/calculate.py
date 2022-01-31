import click
from output import msg
from model import Model


@click.argument(
    "mass",
    type=click.FLOAT,
)
@click.argument(
    "capacity",
    type=click.FLOAT,
)
@click.argument(
    "modelfile",
    type=click.File(mode="r"),
)
@click.command(short_help="Estimate for the flight time.")
def calculate(modelfile, capacity, mass):
    """Calculate an estimate for the flight time of drone using it's flight time model.
    Predicted values are estimated using an average capacity to mass ratio taken from real
    world battery data. If the given battery scores higher than the predicted value it can be
    considered to have "above average" theoretical performance, and vice versa.

    \b
    MODELFILE - the relative file path of the model.json file to test aganst.
    CAPACITY - The capacity of the battery (Ah).
    MASS - The mass of the battery (kg).
    """

    model = Model.load(modelfile.read())
    predicted_mins, predicted_f = model.model(capacity)
    predicted_result = f"PREDICTED\n  - mins: {predicted_mins}\n  - F={predicted_f}"
    actual_mins, actual_f = model.model(capacity, battery_mass=mass)
    actual_result = f"ACTUAL\n  - mins: {actual_mins}\n  - F={actual_f}"
    msg(f"\nFor the given battery capacity:\n{predicted_result}\n{actual_result}")
