import matplotlib.pyplot as plt

class Bar:

    def __init__(self, tick_label, height, width, color, xlabel, ylabel, title, filename):
        self.tick_label = tick_label
        self.height = height
        self.width = width
        self.color = color
        self.xlabel = xlabel
        self.ylabel = ylabel
        self.title = title
        self.filename = filename
    
    def plot(self):

        fig = plt.figure()

        x = [i for i in range(1, len(tick_label) + 1)]

        plt.bar(x, self.height, tick_label = self.tick_label,
        width = self.width, color = self.color)
        
        plt.xlabel(self.xlabel)
        plt.ylabel(self.ylabel)
        plt.title(self.title)

        return fig.savefig('static/img/%s.png' % (self.filename))

height = [10, 24, 36, 40, 5]

tick_label = ['one', 'two', 'three', 'four', 'five']
color = ['red', 'green']
width = 0.8

graph = Bar(tick_label, height, width, color, 'x - axis', 'y - axis', 'My bar chart!', 'bar')
graph.plot()
