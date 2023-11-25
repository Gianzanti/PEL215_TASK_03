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
    tx1 = ax.text(0.02, 0.95, '', transform=ax.transAxes)

    ax.text(-4.75, 0.76, 'Odometria', color='blue')
    ax.text(-4.75, 0.71, 'Observação', color='green')
    ax.text(-4.75, 0.66, 'Correção', color='red')

    ax.set_ylabel('Densidade')
    ax.set_xlabel('Posição X [m]')
    ax.set_title('Filtro de Kalman', fontsize=14)

    ax.set_xlim(-5, 5)
    ax.set_ylim(0, 1)
    ax.grid()

    def init():
        ln1.set_data([], [])
        tx1.set_text('')
        return ln1, tx1
    
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
            ax.text(data["measurements"][frame][0] - 0.08, -0.05, f'{data["measurements"][frame][0]:.2f}', color='red')

        # plotting corrections
        if (data['corrections'][frame][0] != 0 and data['corrections'][frame][1] != 0):
            y = norm.pdf(x, data['corrections'][frame][0], np.sqrt(data['corrections'][frame][1]))
            ax.plot(x, y, 'r-')
            ax.axvline(x=data['corrections'][frame][0], color='r', linestyle='--')

        tx1.set_text(f'Tempo: {(data["timeStep"]/1000)*frame:.2f} s')

        return ln1, tx1
    
    ani = animation.FuncAnimation(fig, update, frames=data_points + 39, interval=20, init_func=init, blit=True)

    writer = animation.FFMpegWriter(
        fps=15, metadata=dict(artist='Me'), bitrate=1800)
    ani.save("movie.mp4", writer=writer)

    # mp.show()


if __name__ == "__main__":
    showGaussian()