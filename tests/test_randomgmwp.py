# -*- encoding: utf-8 -*-

# add extplugins to the Python sys.path
import sys, os, time
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../extplugins'))

from unittest import TestCase
from mock import patch, call, Mock
from mockito import when, verify
from b3.fake import FakeConsole, FakeClient
from b3.config import XmlConfigParser, CfgConfigParser
from b3.parsers.bf3 import GUNMASTER_WEAPONS_PRESET_BY_INDEX
from b3.cvar import Cvar
from rgmwp import RgmwpPlugin


class RgmwpPluginTest(TestCase):

    def tearDown(self):
        if hasattr(self, "parser"):
            del self.parser.clients
            self.parser.working = False

    def setUp(self):
        # create a B3 FakeConsole
        self.parser_conf = XmlConfigParser()
        self.parser_conf.loadFromString(r"""<configuration/>""")
        self.console = FakeConsole(self.parser_conf)

        # create our plugin instance
        self.plugin_conf = CfgConfigParser()
        self.p = RgmwpPlugin(self.console, self.plugin_conf)

        # initialise the plugin
        self.plugin_conf.loadFromString(r'''
[commands]
gmwp: 20
        ''')

        self.p.onLoadConfig()
        self.p.console.game.gameName = 'bf3'
        self.p.onStartup()


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
