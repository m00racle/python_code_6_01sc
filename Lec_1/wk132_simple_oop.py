import os
dir = os.path.dirname(__file__)

class Car:
    color = 'gray'
    def describeCar(self):
        return 'A cool ' + Car.color + ' car'
    def describeSelf(self):
        return 'A cool ' + self.color + ' car'
    
def run():
    # clear the output file content:
    f = open(dir + '/wk132_simple_oop_answer.txt', 'w')
    f.write("")
    f.close()
    nona = Car()
    f = open(dir + '/wk132_simple_oop_answer.txt', 'a')
    f.write("\nnona = Car()")
    f.write('\n\n1. >>> nona.describeCar():\n')
    f.write(nona.describeCar())
    
    f.write("\n\n2 >> nona.describeSelf () :\n")
    f.write(nona.describeSelf ())
    
    f.write('\n\n3. >>> nona.color : \n')
    f.write(nona.color)

    f.write('\n\n4. >>> lola = Car()')
    f.write('\n   >>> lola.color = \'plaid\'')
    f.write("\n   >>> lola.describeCar() : \n")
    lola = Car()
    lola.color = 'plaid'
    f.write(lola.describeCar())

    f.write('\n\n5. >>> lola.describeSelf() :\n')
    f.write(lola.describeSelf())

    f.write(f'\n\n6. >>> lola.color\n{lola.color}')

    f.write(f'\n\n7. >>> nona.describeSelf()\n{nona.describeSelf()}')

    f.write(f'\n\n8. >>> nona.size = \'small\'\
            \n   >>> lola.size \n')
    nona.size = 'small'
    f.write("AttributeError: 'Car' object has no attribute 'size'")

    f.write(f"\n\n9. >>> Car.size = 'big'\
        \n   >>> lola.size \n")
    Car.size = 'big'
    f.write(lola.size)
    
    f.write("\n\n10. >>> nona.size\n")
    f.write(nona.size)

    f.close()



if __name__ == '__main__':
    run()
