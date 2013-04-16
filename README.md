# RandomGunMasterWeaponPreset (Bf3) Plugin [![Build Status](https://travis-ci.org/ozon/b3-plugin-randomgmwp.png?branch=master)](https://travis-ci.org/ozon/b3-plugin-randomgmwp)
A Plugin that sets at Round end a random weapon preset if the next map game mode is GunMaster.

### Requirements
- latest [BigBrotherBot](http://www.bigbrotherbot.net/ "BigBrotherBot")
- Battlefield3 Game server

## Usage

### Installation
1. Copy the file [extplugins/rgmwp.py](extplugins/rgmwp.py) into your `b3/extplugins` folder and
[extplugins/conf/plugin_rgmwp.ini](extplugins/conf/plugin_rgmwp.ini) into your `b3/conf` folder

2. Add the following line in your b3.xml file (below the other plugin lines)
```xml
<plugin name="rgmwp" config="@conf/plugin_rgmwp.ini"/>
```

### Settings
Look into `plugin_rgmwp.ini` file. A detailed description is coming soon.

### Commands
##### !gmwp
  Show the current weapon preset.

##### !gmwp random
  Set a random weapon preset for the next round.

##### !gmwp show
  Show all available weapons presets.

##### !gmwp <id>
  Set a new weapon preset by id.  
  Example: `!gmwp 2` - Set `EU arms race` as new weapon preset

##### !gmwp show <id>
  Shows the defined arms of the specified weapons presets.

