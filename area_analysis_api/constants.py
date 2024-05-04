"""
Landscape types in GEE
https://zenodo.org/records/4723921
"""
landscape_types = {
    0: "Unknown. No or not enough satellite data available.",
    20: "Shrubs. Woody perennial plants with persistent and woody stems\nand without any defined main stem being less than 5 m tall. The\nshrub foliage can be either evergreen or deciduous.\n",
    30: "Herbaceous vegetation. Plants without persistent stem or shoots above ground\nand lacking definite firm structure. Tree and shrub cover is less\nthan 10 %.\n",
    40: "Cultivated and managed vegetation / agriculture. Lands covered with temporary crops followed by harvest\nand a bare soil period (e.g., single and multiple cropping systems).\nNote that perennial woody crops will be classified as the appropriate\nforest or shrub land cover type.\n",
    50: "Urban / built up. Land covered by buildings and other man-made structures.",
    60: "Bare / sparse vegetation. Lands with exposed soil, sand, or rocks and never has\nmore than 10 % vegetated cover during any time of the year.\n",
    70: "Snow and ice. Lands under snow or ice cover throughout the year.",
    80: "Permanent water bodies. Lakes, reservoirs, and rivers. Can be either fresh or salt-water bodies.",
    90: "Herbaceous wetland. Lands with a permanent mixture of water and herbaceous\nor woody vegetation. The vegetation can be present in either salt,\nbrackish, or fresh water.\n",
    100: "Moss and lichen.",
    111: "Closed forest, evergreen needle leaf. Tree canopy >70 %, almost all needle leaf trees remain\ngreen all year. Canopy is never without green foliage.\n",
    112: "Closed forest, evergreen broad leaf. Tree canopy >70 %, almost all broadleaf trees remain\ngreen year round. Canopy is never without green foliage.\n",
    113: "Closed forest, deciduous needle leaf. Tree canopy >70 %, consists of seasonal needle leaf\ntree communities with an annual cycle of leaf-on and leaf-off\nperiods.\n",
    114: "Closed forest, deciduous broad leaf. Tree canopy >70 %, consists of seasonal broadleaf\ntree communities with an annual cycle of leaf-on and leaf-off periods.\n",
    115: "Closed forest, mixed.",
    116: "Closed forest, not matching any of the other definitions.",
    121: "Open forest, evergreen needle leaf. Top layer- trees 15-70 % and second layer- mixed of shrubs\nand grassland, almost all needle leaf trees remain green all year.\nCanopy is never without green foliage.\n",
    122: "Open forest, evergreen broad leaf. Top layer- trees 15-70 % and second layer- mixed of shrubs\nand grassland, almost all broadleaf trees remain green year round.\nCanopy is never without green foliage.\n",
    123: "Open forest, deciduous needle leaf. Top layer- trees 15-70 % and second layer- mixed of shrubs\nand grassland, consists of seasonal needle leaf tree communities with\nan annual cycle of leaf-on and leaf-off periods.\n",
    124: "Open forest, deciduous broad leaf. Top layer- trees 15-70 % and second layer- mixed of shrubs\nand grassland, consists of seasonal broadleaf tree communities with\nan annual cycle of leaf-on and leaf-off periods.\n",
    125: "Open forest, mixed.",
    126: "Open forest, not matching any of the other definitions.",
    200: "Oceans, seas. Can be either fresh or salt-water bodies."
}


landscape_types_details = [
    {
        "id": 0,
        "name": "Unknown",
        "details": "Unknown. No or not enough satellite data available.",
        "suitable": False
    },
    {
        "id": 20,
        "name": "Shrubs",
        "details": "Shrubs. Woody perennial plants with persistent and woody stems and without any defined main stem "
                   "being less than 5 m tall. The shrub foliage can be either evergreen or deciduous.",
        "suitable": False
    },
    {
        "id": 30,  # ?
        "name": "Herbaceous vegetation",
        "details": "Herbaceous vegetation. Plants without persistent stem or shoots above ground and lacking definite "
                   "firm structure. Tree and shrub cover is less than 10 %.",
        "suitable": True
    },
    {
        "id": 40,
        "name": "Crops",
        "details": "Cultivated and managed vegetation / agriculture. Lands covered with temporary crops followed by "
                   "harvest and a bare soil period (e.g., single and multiple cropping systems). Note that perennial "
                   "woody crops will be classified as the appropriate forest or shrub land cover type.",
        "suitable": True
    },
    {
        "id": 50,
        "name": "Urban",
        "details": "Urban / built up. Land covered by buildings and other man-made structures.",
        "suitable": False
    },
    {
        "id": 60,
        "name": "Bare / sparse vegetation",
        "details": "Bare / sparse vegetation. Lands with exposed soil, sand, or rocks and never has more than 10 % "
                   "vegetated cover during any time of the year.",
        "suitable": True
    },
    {
        "id": 70,
        "name": "Snow and ice",
        "details": "Snow and ice. Lands under snow or ice cover throughout the year.",
        "suitable": False
    },
    {
        "id": 80,
        "name": "Permanent water bodies",
        "details": "Permanent water bodies. Lakes, reservoirs, and rivers. Can be either fresh or salt-water bodies.",
        "suitable": False
    },
    {
        "id": 90,
        "name": "Herbaceous wetland",
        "details": "Herbaceous wetland. Lands with a permanent mixture of water and herbaceous or woody vegetation. "
                   "The vegetation can be present in either salt, brackish, or fresh water.",
        "suitable": False
    },
    {
        "id": 100,
        "name": "Moss and lichen.",
        "details": "Moss and lichen.",
        "suitable": True
    },
    {
        "id": 111,
        "name": "Closed forest",
        "details": "Closed forest, evergreen needle leaf. Tree canopy >70 %, almost all needle leaf trees remain "
                   "green all year. Canopy is never without green foliage.",
        "suitable": False
    },
    {
        "id": 112,
        "name": "Closed forest",
        "details": "Closed forest, evergreen broad leaf. Tree canopy >70 %, almost all broadleaf trees remain green "
                   "year round. Canopy is never without green foliage.",
        "suitable": False
    },
    {
        "id": 113,
        "name": "Closed forest",
        "details": "Closed forest, deciduous needle leaf. Tree canopy >70 %, consists of seasonal needle leaf tree "
                   "communities with an annual cycle of leaf-on and leaf-off periods.",
        "suitable": False
    },
    {
        "id": 114,
        "name": "Closed forest",
        "details": "Closed forest, deciduous broad leaf. Tree canopy >70 %, consists of seasonal broadleaf "
                   "tree communities with an annual cycle of leaf-on and leaf-off periods.",
        "suitable": False
    },
    {
        "id": 115,
        "name": "Closed forest, mixed.",
        "details": "Closed forest, mixed.",
        "suitable": False
    },
    {
        "id": 116,
        "name": "Closed forest",
        "details": "Closed forest, not matching any of the other definitions.",
        "suitable": False
    },
    {
        "id": 121,
        "name": "Open forest",
        "details": "Open forest, evergreen needle leaf. Top layer- trees 15-70 % and second layer- mixed of shrubs and "
                   "grassland, almost all needle leaf trees remain green all year."
                   "Canopy is never without green foliage.",
        "suitable": False
    },
    {
        "id": 122,
        "name": "Open forest, evergreen broad leaf",
        "details": "Open forest, evergreen broad leaf. Top layer- trees 15-70 % and second layer- mixed of shrubs "
                   "and grassland, almost all broadleaf trees remain green year round. "
                   "Canopy is never without green foliage.",
        "suitable": False
    },
    {
        "id": 123,
        "name": "Open forest, deciduous needle leaf",
        "details": "Open forest, deciduous needle leaf. Top layer- trees 15-70 % and second layer- mixed of shrubs "
                   "and grassland, consists of seasonal needle leaf tree communities with "
                   "an annual cycle of leaf-on and leaf-off periods.",
        "suitable": False
    },
    {
        "id": 124,
        "name": "Open forest, deciduous needle leaf",
        "details": "Open forest, deciduous broad leaf. Top layer- trees 15-70 % and second layer- mixed of shrubs and "
                   "grassland, consists of seasonal broadleaf tree communities with "
                   "an annual cycle of leaf-on and leaf-off periods.",
        "suitable": False
    },
    {
        "id": 125,
        "name": "Open forest, mixed.",
        "details": "Open forest, mixed.",
        "suitable": False
    },
    {
        "id": 126,
        "name": "Open forest",
        "details": "Open forest, not matching any of the other definitions.",
        "suitable": False
    },
    {
        "id": 200,
        "name": "Oceans, seas",
        "details": "Oceans, seas. Can be either fresh or salt-water bodies.",
        "suitable": False
    },
]

FILTERING_AREAS_SCALE = 100
FILTERING_AREAS_SCALE_MIN = 50
FILTERING_AREAS_SCALE_MAX = 200

SUITABLE_TYPES = [30, 40, 60, 100]

# https://www.solargarden.com.ua/ru/kakaya-ploschad-nuzhna-dlya-solnechnoy-elektrostantsii/
# km^2
MIN_POLYGON_AREA = 0.000475
