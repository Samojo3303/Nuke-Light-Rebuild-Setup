# Nuke Light Rebuild Setup
Nuke tool to automatically create an additive light rebuilder setup for Houdini Karma renders.

Install:
- go to C: > Users > (your username) > .nuke
- create a "tools" folder and add the .py file to it
- open (or create) a menu.py in the .nuke folder
- paste this:

import nuke
import tools.AnimayhemNukeSetup_v4 as ans

menubar = nuke.menu("Nuke")
custom = menubar.addMenu("Animayhem Tools")

custom.addCommand(
    "Build Light Setup",
    "ans.main()"
)
- restart Nuke

Use:
- select a single Read node
- in the top menu, select "Animayhem Tools" then "Build Light Setup"
