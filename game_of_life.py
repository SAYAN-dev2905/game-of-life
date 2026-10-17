import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

PRESENT = "glider"   # "glider", "blinker", "random", "gliders", or "gun"
SIZE = 150
SEED = 1
SAVE_GIF = False

class Life:
    def __init__(self, size, present, seed=1):
        self.generation=0
        self.grid=np.zeros((size, size), dtype=int)
        if present == "glider":
            for r,c in [(1,2),(2,3),(3,1),(3,2),(3,3)]:
                self.grid[r,c]=1
        elif present == "blinker":
            mid=size//2
            self.grid[mid, mid-1:mid+2]=1
        elif present=="random":
            rng = np.random.default_rng(seed)
            self.grid = (rng.random((size, size)) < 0.2).astype(int)
        elif present == "gliders":
            rng = np.random.default_rng(seed)
            for _ in range(size // 4):          # many gliders that crash into each other
                r, c = rng.integers(0, size, 2)
                for dr, dc in [(0,1),(1,2),(2,0),(2,1),(2,2)]:
                    self.grid[(r+dr) % size, (c+dc) % size] = 1
        elif present == "gun":
            cells = [(1,5),(1,6),(2,5),(2,6),(11,5),(11,6),(11,7),(12,4),(12,8),(13,3),(13,9),
                     (14,3),(14,9),(15,6),(16,4),(16,8),(17,5),(17,6),(17,7),(18,6),(21,3),
                    (21,4),(21,5),(22,3),(22,4),(22,5),(23,2),(23,6),(25,1),(25,2),(25,6),
                    (25,7),(35,3),(35,4),(36,3),(36,4)]
            for x, y in cells:                  # Gosper glider gun: shoots gliders forever
                self.grid[y + 5, x + 5] = 1

    def step (self):
        g=self.grid         #sum of neighbours
        n=sum(np.roll(np.roll(g,i,0),j,1) for i in (-1,0,1) for j in (-1,0,1) if (i,j)!=(0,0))
        self.grid=((n==3)|((g==1)&(n==2))).astype(int)
        self.generation+=1

life=Life(SIZE,PRESENT,SEED)

fig,ax=plt.subplots(figsize=(6,6), dpi=100)
im=ax.imshow(life.grid, cmap="binary",interpolation="nearest", vmin=0, vmax=1)
ax.set_aspect("equal")
ax.set_xticks([])
ax.set_yticks([])
title=ax.set_title("Generation 0")
plt.tight_layout()

def update(frame):
    life.step()
    im.set_data(life.grid)
    title.set_text(f"Generation: {life.generation}")
    return im, title
paused=False
def on_key(event):
    global paused
    if event.key==" ":
        ani.resume() if paused else ani.pause()
        paused=not paused

fig.canvas.mpl_connect("key_press_event",on_key)
ani=FuncAnimation(fig, update, frames=120 if SAVE_GIF else None, interval=40, blit=False, cache_frame_data=False) 
if SAVE_GIF:
    ani.save("life.gif", writer="pillow", fps=10)
else:
    # manager=plt.get_current_fig_manager()
    # manager.window.state("zoomed")
    plt.show()
        


