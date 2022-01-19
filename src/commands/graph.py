import os
from data.model import Model
import click
from console import info


@click.argument("modelpaths", nargs=-1, type=click.Path(exists=True))
@click.option(
    "--dpi", default=100, help="DPI of graph iamge", type=click.FLOAT, show_default=True
)
@click.option(
    "--format",
    default="png",
    help="File format of the graph image",
    type=click.Choice(["png", "pdf", "svg"], case_sensitive=False),
    show_default=True,
)
@click.option(
    "--transparent",
    help="A flag to represent if the graph image should have a transparent background",
    is_flag=True,
    type=click.BOOL,
    show_default=True,
)
@click.command(short_help="Creates graphs for models")
def graph(
    modelpaths: tuple[str],
    dpi: float,
    format: str,
    transparent: bool,
):
    "Creates graphs for all the models specified in MODELPATHS"

    for modelpath in modelpaths:
        model = Model.load(modelpath)
        outfile = os.path.dirname(f"{modelpath}/model.png")
        model.save_graph(outfile, dpi, format, transparent)
        info(f"Saved to {outfile}")
