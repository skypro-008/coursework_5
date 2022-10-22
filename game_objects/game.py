from exceptions import SomethingWentWrong
from game_objects.ai import AI
from game_objects.battle import Battle
from game_objects.units import BaseHero
from game_objects.arena import Arena
from game_objects.stats import get_verbose_stats, get_unit_stats


class GamePlayerVsAI:

    def __init__(self, arena: Arena, player: BaseHero, robot: BaseHero):
        self.player = player
        self.enemy = robot
        self.battle = Battle(arena, player, robot)

    def game_start(self, *args, **kwargs) -> str:
        """
        Can be used to equip characters, if not equipped elsewhere. Kwargs are:
        equipment: EquipmentList, a list of available equipment
        player_weapon: str
        player_armor: str
        enemy_weapon: str
        enemy_armor: str
        """
        if equipment_list := kwargs.get('equipment', None):
            if player_weapon := kwargs.get('player_weapon', None):
                self.player.equip(weapon=equipment_list.weapon(player_weapon))
            if player_armor := kwargs.get('player_armor', None):
                self.player.equip(armor=equipment_list.armor(player_armor))
            if enemy_weapon := kwargs.get('enemy_weapon', None):
                self.enemy.equip(weapon=equipment_list.weapon(enemy_weapon))
            if enemy_armor := kwargs.get('enemy_armor', None):
                self.enemy.equip(armor=equipment_list.armor(enemy_armor))

        return "Бой начался!"

    def make_turn(self, action: str) -> str:
        """
        Player attacks, enemy responds (if able).
        Return: formatted string with turn results
        """
        result = []
        try:
            result.append(self.battle.actions[action]())
        except SomethingWentWrong as e:
            result.append(str(e))
        self.battle.restore_stamina()

        if not self.battle.someone_died:
            self.battle.swap_units()
            result.append(AI.robot_action(self.battle))
            self.battle.swap_units()
            self.battle.restore_stamina()

        return ' '.join(result)

    def get_player_stats(self) -> dict:
        return get_unit_stats(self.player)

    def get_enemy_stats(self) -> dict:
        return get_unit_stats(self.enemy)

    def get_full_description(self) -> dict:
        return {"player": get_verbose_stats(self.player),
                "enemy": get_verbose_stats(self.enemy)}

    def game_end(self) -> str:
        return "Бой окончен!"
