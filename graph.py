import numpy as np
from matplotlib import pyplot as mp
from scipy.stats import norm
from icecream import ic
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
    
    ani = animation.FuncAnimation(fig, update, frames=data_points, interval=20, init_func=init, blit=True)
    # ani.save('kalman.gif', writer='imagemagick', fps=60)

    writer = animation.FFMpegWriter(
        fps=31.25, metadata=dict(artist='Me'), bitrate=1800)
    ani.save("movie.mp4", writer=writer)

    mp.show()

    # fig = mp.figure(figsize=(8,6), dpi=100)
    # ax = fig.add_subplot(111, aspect='equal')
    # # y = norm.pdf(x, mu_pred[0], np.sqrt(S_pred[0,0]))e


    # # # plotting current door locations
    # # doors = [FIRST_DOOR[0], SECOND_DOOR[0], THIRD_DOOR[0]]
    # # for door in doors:
    # #     x = np.linspace(door-1, door+1, 50)
    # #     y = norm.pdf(x, door, np.sqrt(0.02))
    # #     ax.plot(x, y, '-', color='orange')

    # # mp.show()

    # for i in range(data_points):
    #     # plotting predictions
    #     for prediction in data['predictions']:
    #         y = norm.pdf(x, prediction[0], np.sqrt(prediction[1]))
    #         ax.plot(x, y, 'b-')

    #     # plotting measurements
    #     for measurement in data['measurements']:
    #         y = norm.pdf(x, measurement[0], np.sqrt(measurement[1]))
    #         ax.plot(x, y, 'g-')

    #     # plotting corrections
    #     for correction in data['corrections']:
    #         y = norm.pdf(x, correction[0], np.sqrt(correction[1]))
    #         ax.plot(x, y, 'r-')

    #     # ax.grid()
    #     # ax.legend(
    #     #     ['Odometria', 'Medidas', 'Correção'], 
    #     #     bbox_to_anchor=(0, 1.02, 1, 0.2), 
    #     #     mode="expand", 
    #     #     borderaxespad=0, 
    #     #     ncol=3
    #     # )


    #     # #add legend to plot
    #     # # mp.legend(title='Parameters')

    #     #add axes labels and a title
    #     mp.ylabel('Densidade')
    #     mp.xlabel('Posição X (m)')
    #     mp.title('Distribuição Normal do Mapa', fontsize=14)
    #     mp.show()


    # # plotting predictions
    # for prediction in data['predictions']:
    #     y = norm.pdf(x, prediction[0], np.sqrt(prediction[1]))
    #     ax.plot(x, y, 'b-')

    # # plotting measurements
    # for measurement in data['measurements']:
    #     y = norm.pdf(x, measurement[0], np.sqrt(measurement[1]))
    #     ax.plot(x, y, 'g-')

    # # plotting corrections
    # for correction in data['corrections']:
    #     y = norm.pdf(x, correction[0], np.sqrt(correction[1]))
    #     ax.plot(x, y, 'r-')

    # # ax.grid()
    # # ax.legend(
    # #     ['Odometria', 'Medidas', 'Correção'], 
    # #     bbox_to_anchor=(0, 1.02, 1, 0.2), 
    # #     mode="expand", 
    # #     borderaxespad=0, 
    # #     ncol=3
    # # )


    # # #add legend to plot
    # # # mp.legend(title='Parameters')

    # #add axes labels and a title
    # mp.ylabel('Densidade')
    # mp.xlabel('Posição X (m)')
    # mp.title('Distribuição Normal do Mapa', fontsize=14)
    # mp.show()

if __name__ == "__main__":
    showGaussian()