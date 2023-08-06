from pnd import Boredom


class Alliances(Boredom):
    def __init__(self, **kwargs):
        super().__init__("alliances", **kwargs)

        self.length = "aa_count"
        self.total = [("total_aa_score", 7, float)]


class Cities(Boredom):
    def __init__(self, **kwargs):
        super().__init__("cities", **kwargs)

        self.length = "city_count"
        self.total = [
            ("total_infrastructure", 5, float),
            ("total_land", 7, float),
            ("oil_pp", 8, int),
            ("coal_pp", 10, int),
            ("nuclear_pp", 11, int),
            ("coal_mines", 12, int),
            ("oil_wells", 13, int),
            ("uranium_mines", 14, int),
            ("iron_mines", 15, int),
            ("lead_mines", 16, int),
            ("bauxite_mines", 17, int),
            ("farms", 18, int),
            ("supermarkets", 23, int),
            ("banks", 24, int),
            ("shopping_malls", 25, int),
            ("stadiums", 26, int),
            ("oil_refineries", 27, int),
            ("aluminum_refineries", 28, int),
            ("steel_mills", 29, int),
            ("munitions_factories", 30, int)
        ]


class Nations(Boredom):
    def __init__(self, **kwargs):
        super().__init__("nations", **kwargs)

        self.total = [
            ("total_score", 9, float),
            ("total_population", 10, int),
            ("beige", 13, int),
            ("cities", 15, int),
            ("soldiers", 23, int),
            ("tanks", 24, int),
            ("aircraft", 25, int),
            ("ships", 26, int),
            ("missiles", 27, int),
            ("nuke", 28, int),
        ]
        self.length = "nation_count"
        self.match = [
            ("gray", 12, "gray"),
            ("blitzkrieg", 30, "Blitzkrieg"),
        ]


class Trades(Boredom):
    def __init__(self, **kwargs):
        super().__init__("nations", **kwargs)

