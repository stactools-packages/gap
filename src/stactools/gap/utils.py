import os.path
from typing import Optional

import rasterio
from rasterio.warp import transform_bounds
from shapely.geometry import box
from stactools.core.io import ReadHrefModifier

from stactools.core.utils.convert import cogify
from stactools.gap.constants import DEFAULT_TILE_SIZE

CONUS_BOUNDS = [-128, 23, -66, 52]


def tile(infile, outdir, size=DEFAULT_TILE_SIZE):
    """Tiles the given input to a grid."""
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


def is_conus(href: str,
             read_href_modifier: Optional[ReadHrefModifier] = None) -> bool:
    """Returns true if the raster is inside the Continental United States."""
    if read_href_modifier:
        href = read_href_modifier(href)
    with rasterio.open(href) as dataset:
        bounds = transform_bounds(dataset.crs, "EPSG:4326", *dataset.bounds)
        return box(*CONUS_BOUNDS).contains(box(*bounds))
