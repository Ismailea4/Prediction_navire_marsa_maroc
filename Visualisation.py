import matplotlib.pyplot as plt

def create_plot(x, y):
    fig, ax = plt.subplots()
    ax.plot(x, y)
    ax.set(xlabel='X-axis label', ylabel='Y-axis label',
           title='Simple Plot')
    ax.grid()
    return fig

# Utilisation de la fonction
x = [0, 1, 2, 3, 4, 5]
y = [0, 1, 4, 9, 16, 25]
fig = create_plot(x, y)
fig.show()
