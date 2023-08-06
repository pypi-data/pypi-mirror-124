import math
from .Shape import Shape

class Circle(Shape):
    
    def __init__(self, color = 'black', radius = 1):
    
        self.radius = radius
        Shape.__init__(self, color)
    
    def get_area(self):
        return  math.pi * (self.radius  ** 2)
    
    def get_perimeter(self):
        return 2 * math.pi * self.radius