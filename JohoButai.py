import game_message
from actions import RadarScanAction

class RadarModule:
    def __init__(self, game_message):
        team_id = game_message.currentTeamId
        self.other_ships_ids = [shipId for shipId in game_message.shipsPositions.keys() if shipId != team_id]
        self.enemy_ships_info = {ship_id: [None, 0] for ship_id in self.other_ships_ids}
        self.current_index = 0  # To keep track of the current ship to be scanned
        self.all_ships_scanned_once = False  # Flag to indicate if all ships have been scanned once
        self.last_updated = 0;

    def get_next_ship_to_scan(self):
        if self.all_ships_scanned_once:
            return None  # Return None if all ships have been scanned once

        ship_id_to_scan = self.other_ships_ids[self.current_index]
        self.current_index += 1

        if self.current_index >= len(self.other_ships_ids):
            self.current_index = 0  # Reset index
            self.all_ships_scanned_once = True  # Set flag to True after one full cycle
            self.last_updated = 0

        return ship_id_to_scan

    def scan(self, actions):
        to_scan = self.get_next_ship_to_scan()
        if to_scan:
            actions.append(RadarScanAction(self.get_next_ship_to_scan()))
        else:
            raise IndexError("Tous les vaisseaux ont ete scan")

