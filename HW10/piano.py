import pgzrun

WIDTH = 400
HEIGHT = 300
beep_a = tone.create('E3', 0.1)
beep_s = tone.create('D3', 0.1)
beep_d = tone.create('C3', 0.1)
# this function is called when a keyboard key is pressed down
def on_key_down(key):
   if key == keys.A:
       beep_a.play()
   if key == keys.S:
       beep_s.play()
   if key == keys.D:
       beep_d.play()
def draw():
   screen.fill((0, 0, 0)) # a black background, (red, green, blue)

pgzrun.go()