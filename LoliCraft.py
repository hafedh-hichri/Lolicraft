from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController

app = Ursina()

## Definitions #################################################################

## TEXTURES
grass_txt      = load_texture('assets/grass_block.png')
dirt_txt       = load_texture('assets/dirt_block.png')
stone_txt      = load_texture('assets/stone_block.png')
brick_txt      = load_texture('assets/brick_block.png')
sky_txt        = load_texture('assets/skybox.png')
arm_txt        = load_texture('assets/arm_texture.png')

## AUDIO
punch_sfx      = Audio("assets/punch_sound",loop = False, autoplay = False)
## ambient noise / cicadas ambient sfx
game_sfx       = Audio("assets/cicada_sfx",loop = True, autoplay = True)

## plays cicada ambient music
##dumb me realized it should be loop not Loop, so this is now useless.
#audio_amb = 1
#def audamb():
#    while audio_amb == 1:
#        game_sfx.play()
#    else:
#        game_sfx.play()
#
block_selected = 1
## Checks which button is pressed
def update():
    if held_keys['left mouse'] or held_keys['right mouse']:
        hand.active()
    else:
        hand.passive()

    global block_selected
    if held_keys['1']: block_selected = 1
    if held_keys['2']: block_selected = 2
    if held_keys['3']: block_selected = 3
    if held_keys['4']: block_selected = 4

## Voxels ######################################################################
## plays the cicada sfx on load of the game
game_sfx.play()
class Voxel(Button):
    def __init__(self, position = (0,0,0), texture = grass_txt):
        super().__init__(
            parent = scene,
            position = position,
            model = 'assets/block',
            origin_y = 0.5,
            texture = texture,
            color = color.color(0,0,random.uniform(0.9,1)),
            highlight_color = color.lime,
            scale = 0.5
            )

## Interaction with the voxel / block
    def input(self, key):
        if self.hovered:
            ## left mouse button
            if key == 'left mouse down':
                punch_sfx.play()
                ## Checks what block has been selected base from keyboard input
                if block_selected == 1:
                    voxel = Voxel(position = self.position + mouse.normal, texture = grass_txt)
                if block_selected == 2:
                    voxel = Voxel(position = self.position + mouse.normal, texture = dirt_txt)
                if block_selected == 3:
                    voxel = Voxel(position = self.position + mouse.normal, texture = stone_txt)
                if block_selected == 4:
                    voxel = Voxel(position = self.position + mouse.normal, texture = brick_txt)
            ## right mouse button
            if key == 'right mouse down':
                punch_sfx.play()
                destroy(self)

################################################################################

class Skybox(Entity):
    def __init__(self):
        super().__init__(
        parent = scene,
        model = 'sphere',
        texture = sky_txt,
        scale = 150,
        double_sided = True
        )

class Hand(Entity):
    def __init__(self):
        super().__init__(
            parent = camera.ui,
            model = 'assets/arm',
            texture = arm_txt,
            scale = 0.2,
            rotation = Vec3(150,-10,0),
            position = Vec2(0.4,-0.6)
        )
    def active(self):
        self.position = Vec2(0.3,-0.5)
    def passive(self):
        self.position = Vec2(0.4,-0.6)

## Generates the ground
for z in range(25):
    for x in range(25):
        voxel = Voxel(position = (x,0,z))

## The player in 1st person perspective
player = FirstPersonController()
## Loads the skybox
sky = Skybox()
## Loads the Hand
hand = Hand()

app = run()
