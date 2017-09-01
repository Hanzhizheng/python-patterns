#!/usr/bin/python
# -*- coding : utf-8 -*-

"""
*What is this pattern about?
It decouples the creation of a complex object and its representation,
so that the same process can be reused to build objects from the same
family.
This is useful when you must separate the specification of an object
from its actual representation (generally for abstraction).

*What does this example do?

The first example achieves this by using an abstract base
class for a building, where the initializer (__init__ method) specifies the
steps needed, and the concrete subclasses implement these steps.

In other programming languages, a more complex arrangement is sometimes
necessary. In particular, you cannot have polymorphic behaviour in a
constructor in C++ - see https://stackoverflow.com/questions/1453131/how-can-i-get-polymorphic-behavior-in-a-c-constructor
- which means this Python technique will not work. The polymorphism
required has to be provided by an external, already constructed
instance of a different class.

In general, in Python this won't be necessary, but a second example showing
this kind of arrangement is also included.

*Where is the pattern used practically?

*References:
https://sourcemaking.com/design_patterns/builder

*TL;DR80
Decouples the creation of a complex object and its representation.
"""


# Abstract Building
class Building(object):

    def __init__(self):
        self.build_floor()
        self.build_size()

    def build_floor(self):
        raise NotImplementedError

    def build_size(self):
        raise NotImplementedError

    def __repr__(self):
        return 'Floor: {0.floor} | Size: {0.size}'.format(self)


# Concrete Buildings
class House(Building):

    def build_floor(self):
        self.floor = 'One'

    def build_size(self):
        self.size = 'Big'


class Flat(Building):

    def build_floor(self):
        self.floor = 'More than One'

    def build_size(self):
        self.size = 'Small'


# In some very complex cases, it might be desirable to pull out the building
# logic into another function (or a method on another class), rather than being
# in the base class '__init__'. (This leaves you in the strange situation where
# a concrete class does not have a useful constructor)


class ComplexBuilding(object):
    def __repr__(self):
        return 'Floor: {0.floor} | Size: {0.size}'.format(self)


class ComplexHouse(ComplexBuilding):
    def build_floor(self):
        self.floor = 'One'

    def build_size(self):
        self.size = 'Big and fancy'


def construct_building(cls):
    building = cls()
    building.build_floor()
    building.build_size()
    return building


# Client
if __name__ == "__main__":
    house = House()
    print(house)
    flat = Flat()
    print(flat)

    # Using an external constructor function:
    complex_house = construct_building(ComplexHouse)
    print(complex_house)

'''
问题：
在软件系统中，有时面临着一个复杂对象的创建工作，通常是由很多其他的对象按一定的规则顺序组合而成；由于需求的变化，这个复杂对象的各个部分经常面临着剧烈的变化，但是将它们组合在一起的规则是相对稳定（结构和顺序）。这时候我们需要把这个复杂对象的创建过程和这个对象的表示（展示）分离开来，使得可以使用同样的构建过程创建不同的对象 表示。

定义：
将一个复杂对象的构建与其表示相分离，使得同样的构建过程可以创建不同的表示。

意图：
提供一个建造者Builder对象，他规定了创建一个复杂对象需要的部件，通过Director指定的创建规则，调用Builder中的具体部件，并指挥Builder返回一个具体的对象。

参与者：
•建造者（Builder）：
为创建一个产品对象的各个部件指定抽象接口。一般会有两种接口方法，一种接口用于规范产品的各个部分的组成，第二种接口用于返回建造后的产品。
•具体建造者（ConcreteBuilder）：
实现Builder的接口，按具体的规则组合复杂产品的各个部件，以及提供一个返回产品的接口。
•指挥者（Director）：
指挥并构造一个使用Builder接口的对象。他只是在按照固定的流程规则将对象组合在一起。不关心组合产品的结果（复杂对象），和细节（子对象）。
•产品（Product）：
表示被构造的复杂对象。
'''
### OUTPUT ###
# Floor: One | Size: Big
# Floor: More than One | Size: Small
# Floor: One | Size: Big and fancy
