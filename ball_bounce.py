import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

G=9.8
Restitution=0.8
dt=0.02
Y0=10.0
v_stop=0.1
steps_per_frame=2
save_GIF=False

class Ball:
    def __init__(self,y0):
        self.y, self.vy, = y0, 0.0
        self.t=0.0
        self.bounces=0
        self.at_rest=False

    def step(self, dt):
        if self.at_rest:
            return
        self.vy -= G*dt
        self.y+=self.vy*dt
        self.t+=dt
        if self.y<=0:
            self.vy= -self.vy*Restitution
            self.bounces+=1
            if abs(self.vy)<v_stop:
                self.vy=0.0
                self.at_rest=True
ball=Ball(Y0)
times, height=[0.0], [Y0]

fig, (ax_ball, ax_graph)=plt.subplots(1,2,figsize=(10,5), constrained_layout=True)
ax_ball.set(xlim=(-1,1), ylim=(-0.5, Y0*1.1), ylabel="Height(m)", title="Ball")
ax_ball.set_xticks([])
ax_ball.axhline(0, color="black", linewidth=2)
dot,=ax_ball.plot([0],[Y0],"o",color="tab:red",markersize=16)
info=ax_ball.text(0.03,0.97,"",transform=ax_ball.transAxes, va="top")
ax_graph.set(xlim=(0,5),ylim=(0, Y0*1.1),xlabel="time(s)", ylabel=" Height(m)", title="Height vs Time")
ax_graph.grid(alpha=0.3)
graph_line,=ax_graph.plot(times,height,color="tab:blue")

def frames():
    frame=0
    while not ball.at_rest:
        yield frame
        frame+=1

def update (frame):
    if not ball.at_rest:
        for i in range (steps_per_frame):
            ball.step(dt)
        times.append(ball.t)
        height.append(ball.y)
        dot.set_data([0],[ball.y])
        graph_line.set_data(times,height)
        if ball.t>ax_graph.get_xlim()[1]:
            ax_graph.set_xlim(0,ball.t*1.2)
        info.set_text(f"t = {ball.t:.2f} s \nbounces = {ball.bounces}")
        if ball.at_rest:
            ax_graph.axvline(ball.t, color="gray", linestyle="---")
            print(f"Rest after {ball.bounces} bounces, t = {ball.t:.2f} s")
    return dot, graph_line, info

ani=FuncAnimation(fig, update, frames=frames(), interval=20, blit=False, repeat=False, cache_frame_data=False)

if save_GIF:
    ani.save("bounce.gif", writer="pillow", fps=25)
else:
    plt.show() 
    