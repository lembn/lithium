from io import BufferedReader, BufferedWriter
from itertools import chain
from pathlib import Path
import pickle
from typing import Generator
from data.battery import Battery

# TODO: do we still need this module?

SAVE_DIR: str = "store"
SAVE_FILE: str = "batteries.pickle"
SAVE_LOCATION: str = f"{SAVE_DIR}/{SAVE_FILE}"

saving: bool = False
outfile: BufferedWriter = None

# TODO: add bz2 compression


def open_save() -> None:
    global saving
    global outfile

    saving = True
    Path(SAVE_DIR).mkdir(parents=True, exist_ok=True)
    outfile = open(SAVE_LOCATION, "wb")


def close() -> None:
    global saving

    saving = False
    if outfile:
        outfile.close()


def save(item: chain) -> None:
    pickle.dump(item, outfile)


def load() -> Generator[Battery, None, None]:
    def load_gen(infile: BufferedReader):
        while True:
            try:
                yield pickle.load(infile)
            except EOFError:
                break
        infile.close()

    try:
        infile = open(SAVE_LOCATION, "rb")
        return load_gen(infile)
    except FileNotFoundError:
        return None
