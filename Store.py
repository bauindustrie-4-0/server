from redis import StrictRedis


class Store:
    def __init__(self, url):
        self.redis = StrictRedis.from_url(url)
        self.initialise(self.redis)

    def initialise(self, redis):
        pass

    def get_beacon_info(self, beacon_id):
        return self.redis.get("beacon_"+beacon_id)

    def set_beacon_info(self, beacon_id, data):
        self.redis.set("beacon_"+beacon_id, data)

    def set_current_beacons(self, beacon_data):
        self.redis.set("current_beacons", beacon_data)

    def get_current_beacons(self):
        return self.redis.get("current_beacons")

    def get_nearest_beacon(self):
        # TODO
        raise Exception("Not Implemented")

    def get_all_beacons(self):
        keys = self.redis.keys("beacon_*")
        return keys

