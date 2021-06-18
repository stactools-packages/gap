from pystac import Provider

DEFAULT_TILE_SIZE = 300000  # meters
KEYWORDS = ["land cover", "vegetation", "ecology", "wildlife habitat"]
PROVIDERS = [
    Provider(
        "U.S. Geological Survey Gap Analaysis Program",
        ("Alexa McKerrow\n218 David Clark Labs\nRaleigh, NC 27695-7617\n"
         "571-218-5474\namckerrow@usgs.gov"),
        ["licensor", "producer", "processor", "host"],
        "https://www.usgs.gov/core-science-systems/science-analytics-and-synthesis/gap"
    )
]
