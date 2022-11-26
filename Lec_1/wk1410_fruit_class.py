"""  
Part 1: Fruit Salad
Define a class FruitSalad with class attributes fruits, which is initially ['melons',
'pineapples'] and servings which is initially 4.
"""

class FruitSalad:
    fruits = ['melons', 'pineapples']
    servings = 4

    def __init__(self, ingredients: list, numservings : int) -> None:
        # put this into instance (self) attributes fruits and servings
        self.fruits = ingredients
        self.servings = numservings
    
    def add(self, fruit : str) -> None:
        self.fruits.append(fruit)
    
    def serve(self) -> str:
        if self.servings > 0:
            self.servings -= 1
            return 'enjoy'
        else:
            return 'sorry'

    def __str__(self) -> str:
        text = str(self.servings) + ' servings of fruit salad with ' + str(self.fruits)
        return text