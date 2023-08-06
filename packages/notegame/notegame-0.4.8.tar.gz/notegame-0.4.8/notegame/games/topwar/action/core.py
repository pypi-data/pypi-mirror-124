import json

from notegame.games.topwar.core.db import PlayerBaseInfo
from notegame.games.topwar.entity import ActionInterface, ActionResponse
from notegame.games.topwar.utils import merge_info


class PrintAction(ActionInterface):
    def __init__(self):
        super(PrintAction, self).__init__()

    def run(self, response: ActionResponse):
        print(response)


class MapInfoAction(ActionInterface):
    def __init__(self):
        self.player_db = PlayerBaseInfo()
        super(MapInfoAction, self).__init__()

    def run(self, response: ActionResponse):
        if response.cid == 901:
            self.load_point(response.data)

    def load_point(self, point_json):
        for point in point_json['pointList']:
            point_type = point['pointType']

            if point_type == 1:
                properties = merge_info(json.loads(point['p']['playerInfo']))
                properties = merge_info(point['p'], properties=properties)
                properties = merge_info(point, properties=properties)

                self.player_db.add_player(properties=properties)
            else:
                pass
