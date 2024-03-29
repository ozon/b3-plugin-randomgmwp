# -*- encoding: utf-8 -*-

# add extplugins to the Python sys.path
import sys, os, time
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../extplugins'))

from unittest import TestCase
from mock import patch, call, Mock
from mockito import when, verify
from tests import Bf3TestCase, Mockito
from b3.fake import FakeConsole, FakeClient
from b3.config import XmlConfigParser, CfgConfigParser
from b3.parsers.bf3 import GUNMASTER_WEAPONS_PRESET_BY_INDEX
from b3.cvar import Cvar
from rgmwp import RgmwpPlugin


class RgmwpPluginTest(Bf3TestCase):

    @classmethod
    def setUpClass(cls):
        Bf3TestCase.setUpClass()
        cls.sleep_patcher = patch.object(time, "sleep")
        cls.sleep_patcher.start()

    @classmethod
    def tearDownClass(cls):
        cls.sleep_patcher.stop()

    def setUp(self):
        Bf3TestCase.setUp(self)
        self.conf = CfgConfigParser()
        self.conf.loadFromString("""[commands]
gmwp: 20
        """)
        self.p = RgmwpPlugin(self.console, self.conf)
        self.p.onLoadConfig()
        self.p.console.game.gameName = 'bf3'
        self.p.onStartup()
        self.superadmin.connects('superadmin')


    def test_setGunMasterWeaponPreset(self):
        self.p.console.setCvar = Mock()
        self.assertEquals(self.p.setGunMasterWeaponPreset(1), GUNMASTER_WEAPONS_PRESET_BY_INDEX[1][0])
        self.p.console.setCvar.assert_called_with('gunMasterWeaponsPreset',1)

    def test_setGunMasterWeaponPreset_wrong_value(self):
        self.p.console.setCvar = Mock()
        self.assertFalse(self.p.setGunMasterWeaponPreset(99))
        self.p.console.setCvar.assert_not_called_with('gunMasterWeaponsPreset', 99)

    def test_setRandomGunMasterWeaponPreset(self):
        def getCvar_proxy(var_name):
            if var_name == 'gunMasterWeaponsPreset':
                return Cvar('gunMasterWeaponsPreset', value='1')
            else:
                return Mock()
        self.p.console.getCvar = Mock(side_effect=getCvar_proxy)
        with patch.object(self.p, "setGunMasterWeaponPreset") as mock_setGunMasterWeaponPreset:
            self.p.setRandomRandomGunMasterWeaponPreset()
        self.assertTrue(mock_setGunMasterWeaponPreset.called)

    def test_cmd_gmwp_random(self):
        self.moderator.connects('moderator')
        def getCvar_proxy(var_name):
            if var_name == 'gunMasterWeaponsPreset':
                return Cvar('gunMasterWeaponsPreset', value='1')
            else:
                return Mock()
        self.p.console.getCvar = Mock(side_effect=getCvar_proxy)

        self.p.setRandomRandomGunMasterWeaponPreset = Mock()
        self.moderator.says('!gmwp random')
        self.assertTrue(self.p.setRandomRandomGunMasterWeaponPreset.called)

    def test_cmd_gmwp_show(self):
        self.moderator.connects('moderator')
        self.moderator.message_history = []
        self.moderator.says('!gmwp show')
        self.assertEqual('[0]Standard Weapon list, [1]Standard Weapon list REVERSED, [2]Light Weight, [3]Heavy Gear, [4]Pistol run!, [5]Snipers Heaven, [6]US arms race, [7]RU arms race, [8]EU arms race', self.moderator.message_history[0])

    def test_cmd_gmwp_show_weapons(self):
        self.moderator.connects('moderator')
        self.moderator.message_history = []
        self.moderator.says('!gmwp show 1')
        self.assertEqual('Standard Weapon list REVERSED: JNG-90 M417 L86 LSAT SCAR-L AUG MTAR ACW-R MK3A1 Flechette SPAS-12 P90 PP-19 T44 M93 MP443 M320 LVG, Knife', self.moderator.message_history[0])

    def test_cmd_gmwp_show_weapons_wrong_id(self):
        self.moderator.connects('moderator')
        self.moderator.message_history = []
        self.moderator.says('!gmwp show 99')
        self.assertEqual('Error: 99 is a invalid value.', self.moderator.message_history[0])

