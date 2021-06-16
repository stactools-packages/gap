import os.path

import rasterio

from stactools.core.utils.convert import cogify
from stactools.gap.constants import DEFAULT_TILE_SIZE


def tile(infile, outdir, size=DEFAULT_TILE_SIZE):
    """Tiles the given input to the MGRS grid."""
    with rasterio.open(infile) as dataset:
        tiles = create_tiles(*dataset.bounds, size)
    for tile in tiles:
        tile.subset(infile, outdir)


def create_tiles(left, bottom, right, top, size):
    x = left
    y = bottom
    tiles = []
    while x < right:
        while y < top:
            tile = Tile(x, y, min(x + size, right), min(y + size, top))
            tiles.append(tile)
            y += size
        x += size
        y = bottom
    return tiles


class Tile:
    def __init__(self, left, bottom, right, top):
        self._left = left
        self._bottom = bottom
        self._right = right
        self._top = top

    def subset(self, infile, outdir):
        base = os.path.splitext(os.path.basename(infile))[0]
        outfile = os.path.join(
            outdir, (f"{base}_{str(int(self._left))}_{str(int(self._top))}_"
                     f"{str(int(self._right))}_{str(int(self._bottom))}.tif"))
        extra_args = [
            "-projwin",
            str(self._left),
            str(self._top),
            str(self._right),
            str(self._bottom)
        ]
        return cogify(infile, outfile, extra_args=extra_args)
