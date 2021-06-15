import mgrs
import rasterio
from pyproj import CRS, Transformer


def tile_to_mgrs_grid(infile, outdir):
    """Tiles the given input to the MGRS grid."""
    wgs84 = CRS.from_epsg(4326)
    with rasterio.open(infile) as dataset:
        transformer = Transformer.from_crs(dataset.crs, wgs84, always_xy=True)
        bounds = transformer.transform_bounds(*dataset.bounds)
        print(bounds)
        for tile in mgrs_tiles(*bounds):
            Tile.subset(dataset, outdir)


def mgrs_tiles(left, bottom, right, top):
    m = mgrs.MGRS()
    print(m.toMGRS(bottom, left))
    return []


class Tile:
    pass
