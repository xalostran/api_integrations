
class Commands():
    def location_cmd(self):
        locations = {
            "Stockholm": 19,
            "Gothenburg": 21,
            "Malmo": 23
        }
        return locations

    def locks_cmd(self):
        locks = {
            "Stockholm": "closed",
            "Gothenburg": "closed",
            "Malmo": "closed"
        }
        return locks

    def lamps_cmd(self):
        lamps = {
            "Stockholm": "off",
            "Gothenburg": "off",
            "Malmo": "off"
        }
        return lamps