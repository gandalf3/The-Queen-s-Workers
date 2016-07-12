
# Quickie todos

Clamp DoF focus to middle ranges of screen
Add a marker for ant destination
Clamp camera to world bounds
Vector based camera movement DONE

# Bugs

BUG: ants don't become honey ants
(tried using replaceMesh, but that didn't work. Looks like we'll have to kill main ant and spawn a honey ant in its place)

FIXED: ants don't starve properly

FIXED: ants carrying part of a resource when it gets used up become lost

FIXED: ants don't always go to the special food buildings

BUG: ants react to clicks on the GUI

BUG: ants can still sometimes leave their carried stuff in mid-air in some cases (need to find out what exact sequence of events causes this)

BUG: worker counters just become plain wrong over time

BUG: camera control doesn't work in standalone player, reports of it being hard to control

BUG: ants just stop when the resource they were collecting runs out. Can make ants hard to find (need to determine best way to solve this; add 'summon idle ants' button to call them back to base? make them return automatically?)

BUG: lack of visual feedback/any kind of indication that food buildings are operating (looks confusing when resources disapear into them and nothing happens immediatly)

BUG: lack of visual feedback when telling ants to go somewhere or collect something (the player has to wait to see if the ants will start collecting what they clicked on, or just walk up to it and stop)

BUG: no indicators for explaining how the game works (e.g. what buildings do what, how they work, etc.)

PARTIALLY FIXED: ending suzanne doesn't go away, making continuing play nearly impossible (maybe the hole should slowly drop back below the ground after the player chooses to continue, and the suzanne can fly about, perhaps following the player?) ----- the dirt mount JetSuz emerges from does not retract back into the earth, but JetSuz doesn't follow the player around, which would be AWESOME!!!!!
