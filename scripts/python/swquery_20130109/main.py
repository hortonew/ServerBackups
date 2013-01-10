import pyglet
from classes import msconnect

screen = pyglet.window.Window(800, 800)
main_batch = pyglet.graphics.Batch()

title = pyglet.text.Label(text="Node Status", x=10, y=775, batch=main_batch)
count = 1

@screen.event
def on_draw():
	screen.clear()
	main_batch.draw()

@screen.event
def on_mouse_scroll(x, y, scroll_x, scroll_y):
	scrollwindow.view_y += scroll_y*50

if __name__ == "__main__":
	m = msconnect.MSSQLConnect()
	m.load_data()
	
	alltext = m.get_data()
	
	d = pyglet.text.decode_text("".ljust(800))
	d.set_style(0,12, dict(font_name='Arial', font_size=12, color=(255,255,255,255)))
	for i in alltext:
		d.insert_text(-1, "%s\t%s".ljust(800) % (i[0],i[1]))

	scrollwindow = pyglet.text.layout.ScrollableTextLayout(d, width=780, height=750, multiline=True, batch=main_batch)
	scrollwindow.x = 10
	scrollwindow.y = 10
	scrollwindow.view_y = 0

	pyglet.app.run()