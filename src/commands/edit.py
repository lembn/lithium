import json
from tkinter import E
import output

import click
from model import Model


@click.command(short_help="Edit a model")
@click.argument("modelfile", type=click.File(mode="r"))
def edit(modelfile: click.File):
    """Edit the model specified by MODELFILE. All the model's files will be updated to reflect these changes"""

    model = Model.load(modelfile.read())
    title = f"# Editing {model.name}@{modelfile.name}:"
    text = click.edit(f"\n\n{title}\n{model}")
    if text is not None:
        text = text.replace("\n", "")
        text = text.replace("    ", "")
        text = text.replace(title, "")
        try:
            model = Model.load(text)
            model.save()
        except KeyError as e:
            output.msg(
                f"invalid modelfile - failed to locate '{e}'\nRolling back...",
                "ERROR",
                "red",
            )
