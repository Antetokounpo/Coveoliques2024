from JohoButai import RadarModule
from game_message import *
from actions import *
import random
import itertools
from typing import Tuple
from shooting import Shooting
from math import degrees

class Bot:
    def __init__(self):
        print("Initializing your super mega duper bot")
        self.crew_member_assigned_to_cannon: Tuple[CrewMember, TurretStation] = None
        self.current_index = 0  # To keep track of the current ship to be scanned
        self.all_ships_scanned_once = False  # Flag to indicate if all ships have been scanned once
        self.last_updated = 0;

    def distance_from_station(self, crew_member: CrewMember, station: Station) -> float:
        distances_from_stations = crew_member.distanceFromStations
        all_distances_from_stations = distances_from_stations.turrets + distances_from_stations.shields + distances_from_stations.radars + distances_from_stations.helms

        # distance from the selected station
        distance = [s for s in all_distances_from_stations if s.stationId == station.id]

        return distance[0].distance if distance else 99999

    def scan_ships(self, game_message: GameMessage):
        other_ships_ids = [shipId for shipId in game_message.shipsPositions.keys() if shipId != game_message.currentTeamId]
        if self.all_ships_scanned_once:
            return None  # Return None if all ships have been scanned once

        ship_id_to_scan = other_ships_ids[self.current_index]
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

    def init_crew_member_assigned_to_cannon(self, game_message):
        if self.crew_member_assigned_to_cannon is not None:
            return
        my_ship = game_message.ships.get(game_message.currentTeamId)
        crew = my_ship.crew

        turrets = my_ship.stations.turrets
        normal_cannons = [t for t in turrets if t.turretType == TurretType.Normal]

        crew_member_cannon_product = list(itertools.product(crew, normal_cannons))
        crew_member_cannon = min(crew_member_cannon_product, key=lambda x: self.distance_from_station(*x))

        self.crew_member_assigned_to_cannon = crew_member_cannon

    def shoot_meteor(self, game_message):
        cannon = self.crew_member_assigned_to_cannon[1]
        cannon_position = cannon.worldPosition
        cannon_position = Vector(cannon_position.x, cannon_position.y)
        rocket_speed = game_message.constants.ship.stations.turretInfos[TurretType.Normal].rocketSpeed

        meteors = game_message.debris
        print(meteors)

        meteor_position = Vector(meteors[0].position.x, meteors[0].position.y)
        meteor_velocity = Vector(meteors[0].velocity.x, meteors[0].velocity.y)

        shooting_angle = -Shooting().get_shooting_angle(cannon_position, rocket_speed, meteor_position, meteor_velocity)
        rotation_angle = degrees(shooting_angle)-cannon.orientationDegrees

        #actions.append(TurretRotateAction(cannon.id, rotation_angle))
        #actions.append(TurretShootAction(cannon.id))
    def get_next_move(self, game_message: GameMessage):
        """
        Here is where the magic happens, for now the moves are not very good. I bet you can do better ;)
        """
        actions = []

        team_id = game_message.currentTeamId
        my_ship = game_message.ships.get(team_id)
        other_ships_ids = [shipId for shipId in game_message.shipsPositions.keys() if shipId != team_id]


        print(other_ships_ids)
        crew = my_ship.crew

        #helm_id = crew[0].distanceFromStations.helms[0].stationId
        #helm = [s for s in my_ship.stations.helms if s.id == helm_id][0]
        #if helm.operator is None:
        #    actions.append(CrewMoveAction(crewMemberId=crew[0].id, destination=helm.gridPosition))
        #else:
        #    #other_ships = [s for s in game_message.ships.values() if (s.teamId != team_id)]
        #    print(game_message.shipsPositions[other_ships_ids[0]])
        #    print(my_ship.worldPosition)
        #    print(my_ship.orientationDegrees)
        #    actions.append(ShipLookAtAction(game_message.shipsPositions[other_ships_ids[0]]))
        #    #actions.append(ShipLookAtAction(Vector(0, 0)))

        shield_id = crew[1].distanceFromStations.shields[0].stationId
        shield = [s for s in my_ship.stations.shields if s.id == shield_id][0]
        if shield.operator is None:
            actions.append(CrewMoveAction(crewMemberId=crew[1].id, destination=shield.gridPosition))
        
        occupied_turrets = []
        for crew_member in crew[1:]:
            if crew_member.currentStation is None:
                accessible_turrets = [t for t in crew_member.distanceFromStations.turrets if t.stationId not in occupied_turrets][::-1]
                turret = accessible_turrets[0]
                turret = [t for t in my_ship.stations.turrets if turret.stationId == t.id][0]

                actions.append(CrewMoveAction(crewMemberId=crew_member.id, destination=turret.gridPosition))
                occupied_turrets.append(turret.id)
            else:
                occupied_turrets.append(crew_member.currentStation)
                actions.append(TurretShootAction(crew_member.currentStation))
        


        turrets = my_ship.stations.turrets
        print([turret.turretType for turret in turrets])

        #self.init_crew_member_assigned_to_cannon(game_message)

        # Move the cannon operator to the cannon
        #if self.crew_member_assigned_to_cannon[1].operator is None:
        #    actions.append(CrewMoveAction(crewMemberId=self.crew_member_assigned_to_cannon[0].id, destination=self.crew_member_assigned_to_cannon[1].gridPosition))




        # You can clearly do better than the random actions above! Have fun!
        print(game_message.constants.ship.stations.turretInfos)
        print(game_message.shipsPositions.get(other_ships_ids[0]))
        return actions
