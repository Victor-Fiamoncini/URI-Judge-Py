import matplotlib.pyplot as plt

class Pie:

  def __init__(self, slices, labels, colors, startangle, shadow, explode, radius, autopct, filename):
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
    plt.pie(
      self.slices, 
      labels=self.labels, 
      colors=self.colors,
      startangle=self.startangle, 
      shadow=self.shadow, 
      explode=self.explode,
      radius=self.radius, 
      autopct=self.autopct
    )
    fig.savefig('static/img/%s.svg' % (self.filename))
