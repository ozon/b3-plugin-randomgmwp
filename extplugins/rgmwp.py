# -*- coding: utf-8 -*-

# Random GunMaster WeaponPreset Plugin for BigBrotherBot(B3)
# Copyright (c) 2013 Harry Gabriel <rootdesign@gmail.com>

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

__author__ = 'ozon'
__version__ = '0.1.0'

import b3
from b3.plugin import Plugin
import b3.events
from b3.parsers.bf3 import GUNMASTER_WEAPONS_PRESET_BY_INDEX, GUNMASTER_WEAPONS_PRESET_BY_NAME, MAP_NAME_BY_ID, GAME_MODES_NAMES
from b3.parsers.frostbite2.protocol import CommandFailedError
from random import randrange
from ConfigParser import NoOptionError

class RgmwpPlugin(Plugin):
    _adminPlugin = None
    _random_enabled = True

    def onLoadConfig(self):
        self._load_settings()

    def onStartup(self):
        # check if bf3 game
        if self.console.game.gameName != 'bf3':
            self.error('This plugin only works with Battlefield3 (bf3).')
            return False

        # try to load admin plugin
        self._adminPlugin = self.console.getPlugin('admin')
        if not self._adminPlugin:
            self.error('Could not find admin plugin')
            return False

        # register our command
        self._register_commands()

        # register events
        self.registerEvent(b3.events.EVT_GAME_ROUND_PLAYER_SCORES)

    def onEvent(self, event):
        if event.type == b3.events.EVT_GAME_ROUND_PLAYER_SCORES and self._random_enabled:
            if self._get_rounds_left() > 0 or self.get_nextMap()[1] == 'GunMaster0':
                _new_preset = self.setRandomRandomGunMasterWeaponPreset()
                self.debug('Set weapon preset: %s' % _new_preset)

    def cmd_gmwp(self, data, client, cmd=None):
        """\
        <random|show> - manage the GunMaster WeaponPreset
        """

        if not data:
            _current_preset = self.console.getCvar('gunMasterWeaponsPreset').getInt()
            client.message('Current GunMaster Preset: %s' % GUNMASTER_WEAPONS_PRESET_BY_INDEX[_current_preset][0])
        else:
            try:
                args = self._adminPlugin.parseUserCmd(data)
                if args[0].isdigit():
                    new_preset_name = self.setGunMasterWeaponPreset(args[0])
                    if new_preset_name:
                        if self._get_rounds_left() > 0:
                            client.message('Set %s for the next round.' % new_preset_name)
                        else:
                            nMap, nGametype, nRounds = self.get_nextMap()
                            if nGametype == 'GunMaster0':
                                client.message('Set %s for the next Map (%s).' % (new_preset_name, MAP_NAME_BY_ID[nMap]))
                            else:
                                client.message('Set %s. Remember, next map game mode is: %s.' % (new_preset_name, GAME_MODES_NAMES[nGametype]))
                    else:
                        raise ValueError(args[0])
                elif args[0] == 'show':
                    if not args[1]:
                        human_presetlist = ', '.join( ['[%s]%s' %(i, GUNMASTER_WEAPONS_PRESET_BY_INDEX[i][0]) for i in range(len(GUNMASTER_WEAPONS_PRESET_BY_INDEX))] )
                        client.message(human_presetlist)
                    elif args[1].isdigit():
                        if int(args[1]) in range(len(GUNMASTER_WEAPONS_PRESET_BY_INDEX)):
                            human_weaponlist = ' '.join(GUNMASTER_WEAPONS_PRESET_BY_INDEX[int(args[1])][1])
                            client.message('%s: %s' % (GUNMASTER_WEAPONS_PRESET_BY_INDEX[int(args[1])][0], human_weaponlist))
                        else:
                            raise ValueError(args[1])
                    else:
                        raise ValueError(args[0])
                elif args[0] == 'random':
                    new_preset_name = self.setRandomRandomGunMasterWeaponPreset()
                    if new_preset_name:
                        if self._get_rounds_left() > 0:
                            client.message('Set %s for the next round.' % new_preset_name)
                        else:
                            nMap, nGametype, nRounds = self.get_nextMap()
                            if nGametype == 'GunMaster0':
                                client.message('Set %s for the next Map (%s).' % (new_preset_name, MAP_NAME_BY_ID[nMap]))
                            else:
                                client.message('Set %s. Remember, next map game mode is: %s.' % (new_preset_name, GAME_MODES_NAMES[nGametype]))
            except ValueError, err:
                client.message('Error: %s is a invalid value.' % err.message)


    def setRandomRandomGunMasterWeaponPreset(self):
        """Set new GunMaster Preset index by random generated int
        """
        _current_preset = self.console.getCvar('gunMasterWeaponsPreset').getInt()

        while True:
            _new_preset = randrange(len(GUNMASTER_WEAPONS_PRESET_BY_INDEX))
            if _new_preset != _current_preset:
                break

        return self.setGunMasterWeaponPreset(_new_preset)

    def setGunMasterWeaponPreset(self, preset):
        """Set new GunMaster WeaponPreset.

         :param preset: GunMaster Weapon preset index id
         :type preset: int
        """
        if int(preset) <= len(GUNMASTER_WEAPONS_PRESET_BY_INDEX):
            try:
                self.debug('Set %s as GunMaster Weapon Preset' % GUNMASTER_WEAPONS_PRESET_BY_INDEX[int(preset)][0])
                self.console.setCvar('gunMasterWeaponsPreset', int(preset))
                return GUNMASTER_WEAPONS_PRESET_BY_INDEX[int(preset)][0]
            except CommandFailedError, err:
                self.error('Failed to set new GunMaster Preset. Error: %s' % err.message)
                return False
        else:
            self.error('Error: %s is a invalid index.' % int(preset))
            return False

    def get_nextMap(self):
        """query the Frostbite2 game server and return the next (MapName, GameType, Rounds).

        :rtype : tuple(MapName, GameType, Rounds)
        """
        try:
            nextMapIndex = self.console.write(('mapList.getMapIndices', ))
            nextmapData = self.console.write(('mapList.list', int(nextMapIndex[1]), ))
            return nextmapData[2], nextmapData[3], nextmapData[4]
        except CommandFailedError, err:
            self.error('Error: %s' % err.message)
            return None

    def _get_rounds_left(self):
        """check and return rounds left"""
        rounds = self.console.write(('mapList.getRounds',))
        current_round = int(rounds[0]) + 1
        total_rounds = int(rounds[1])
        rounds_left = total_rounds - current_round
        return rounds_left

    # plugin helpers
    def _getCmd(self, cmd):
        cmd = 'cmd_%s' % cmd
        if hasattr(self, cmd):
            func = getattr(self, cmd)
            return func

        return None

    def _register_commands(self):
        if 'commands' in self.config.sections():
            for cmd in self.config.options('commands'):
                level = self.config.get('commands', cmd)
                sp = cmd.split('-')
                alias = None
                if len(sp) == 2:
                    cmd, alias = sp

                func = self._getCmd(cmd)
                if func:
                    self._adminPlugin.registerCommand(self, cmd, level, func, alias)

    def _load_settings(self):
        try:
            self._random_enabled = self.config.getboolean('settings','enable_random')
        except NoOptionError:
            self.warning('conf "enable_random" not found, using default : yes')
        except ValueError:
            self.warning('conf "announce first kill" allow only yes or no as value')
