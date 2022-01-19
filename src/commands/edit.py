import click
from data.model import Model
import json


@click.command()
@click.argument("modelfile", type=click.File(mode="r"))
def edit(modelpath: tuple[str]):
    """Edit the model specified by MODELFILE"""

    model = Model.load(modelfile.read())
    title = f"# Editing MODEL@{modelpath}:"
    message = click.edit(f"\n\n{title}\n{model}")
    if message is not None:
        model_json = json.loads(message.split(title, 1)[0].strip("\n"))
        model = Model.load(model_json)
