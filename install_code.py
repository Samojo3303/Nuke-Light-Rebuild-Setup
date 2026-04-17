import nuke
import tools.AnimayhemNukeSetup_v4 as ans

menubar = nuke.menu("Nuke")
custom = menubar.addMenu("Animayhem Tools")

custom.addCommand(
    "Build Light Setup",
    "ans.main()"
)
