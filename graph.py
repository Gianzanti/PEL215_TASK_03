import numpy as np
from matplotlib import pyplot as mp
from scipy.stats import norm
from matplotlib import animation

def showGaussian():
    load = np.load("./data_kalman.npz")
    data = {'timeStep': load["timeStep"], 'predictions': load["predictions"], 'measurements': load["measurements"], 'corrections': load["corrections"]}

    data_points = 960

    x = np.linspace(-5, 5, data_points)

    fig, ax = mp.subplots(1,1,figsize=(20,6))
    ln1, = ax.plot([], [], 'b-', animated=True)

    ax.text(-4.9, 5.5, 'Odometria', color='blue', fontsize=14)
    ax.text(-4.9, 4.5, 'Observação', color='green', fontsize=14)
    ax.text(-4.9, 3.5, 'Correção', color='red', fontsize=14)

    ax.set_ylabel('Densidade')
    ax.set_xlabel('Posição X [m]')
    ax.set_title('Filtro de Kalman', fontsize=14)

    ax.set_xlim(-5, 5)
    ax.set_ylim(0, 6)
    ax.grid()

    def init():
        ln1.set_data([], [])
        return ln1
    
    def update(frame):
        if (data['predictions'][frame][0] == 0 or data['predictions'][frame][1] == 0):
            ln1.set_data([], [])
        else:
            y = norm.pdf(x, data['predictions'][frame][0], np.sqrt(data['predictions'][frame][1]))
            ln1.set_data(x, y)

        # plotting measurements
        if (data['measurements'][frame][0] != 0 and data['measurements'][frame][1] != 0):
            y = norm.pdf(x, data['measurements'][frame][0], np.sqrt(data['measurements'][frame][1]))
            ax.plot(x, y, 'g-')
            ax.axvline(x=data['measurements'][frame][0], color='g', linestyle='--')
            ax.text(data["measurements"][frame][0] - 0.1, -0.3, f'{data["measurements"][frame][0]:.2f}', color='red')

        # plotting corrections
        if (data['corrections'][frame][0] != 0 and data['corrections'][frame][1] != 0):
            y = norm.pdf(x, data['corrections'][frame][0], np.sqrt(data['corrections'][frame][1]))
            ax.plot(x, y, 'r-')
            ax.axvline(x=data['corrections'][frame][0], color='r', linestyle='--')

        return ln1
    
    ani = animation.FuncAnimation(fig, update, frames=data_points + 39, interval=20, init_func=init, blit=True)

    writer = animation.FFMpegWriter(
        fps=15, metadata=dict(artist='Me'), bitrate=1800)
    ani.save("movie.mp4", writer=writer)


if __name__ == "__main__":
    showGaussian()