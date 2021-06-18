# stactools-gap

[![CI](https://github.com/stactools-packages/gap/actions/workflows/continuous-integration.yml/badge.svg)](https://github.com/stactools-packages/gap/actions/workflows/continuous-integration.yml)

[stactools](https://github.com/stac-utils/stactools) package for the [USGS Gap Analysis Project](https://www.usgs.gov/core-science-systems/science-analytics-and-synthesis/gap).

## Installation

Latest stable version:

```bash
pip install stactools-gap
```

Latest development version:

```bash
pip install git+https://github.com/stactools-packages/gap
```

## Usage

GAP data comes as big rasters, either TIFFs or IMG files.
You can tile these large rasters and create a STAC Collection for those tiles using `create-collection`:

```bash
stac gap create-collection --tile-source gap.tif gap.xml tile-directory stac-directory
```

If you just want to create tiles, use the `tile` command:

```bash
stac gap tile gap.tif tile-directory
```

If you already have tiles directory, you can skip the tiling step by omitting the `--tile-source` argument to `create-collection`:

```bash
stac gap create-collection gap.xml tile-directory stac-directory
```

For complete listing of options, use `stac gap --help`.
