import matplotlib.pyplot as plt

class Pie:

    def __init__(self, slices, labels, colors, startangle, shadow, explode, radius, autopct, 
    filename):
        self.slices = slices
        self.labels = labels
        self.colors = colors
        self.startangle = startangle
        self.shadow = shadow
        self.explode = explode
        self.radius = radius
        self.autopct = autopct
        self.filename = filename

    def plot(self):

        fig = plt.figure()

        plt.pie(self.slices, labels = self.labels, colors = self.colors,
        startangle = self.startangle, shadow = self.shadow, explode = self.explode,
        radius = self.radius, autopct = self.autopct)

        return fig.savefig("static/img/%s.png" % (self.filename))

activities = ['eat', 'sleep', 'work', 'play'] 
slices = [3, 7, 8, 6]  
colors = ['r', 'y', 'g', 'b'] 
startangle = 90
shadow = True
explode = (0, 0, 0.1, 0)
radius = 1.2
autopct = '%1.1f%%'


graph = Pie(slices, activities, colors, startangle, shadow, explode, radius, autopct, 'pie')

graph.plot()
