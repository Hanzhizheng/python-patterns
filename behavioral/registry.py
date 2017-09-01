#!/usr/bin/env python
# -*- coding: utf-8 -*-
# learn: http://www.jb51.net/article/61138.htm


class RegistryHolder(type):

   '''
    type可以接受一个类的描述作为参数，然后返回一个类：
    type(类名, 父类的元组（针对继承的情况，可以为空），包含属性的字典（名称和值）)
    '''
    REGISTRY = {}

    def __new__(cls, name, bases, attrs):
        new_cls = type.__new__(cls, name, bases, attrs)
        """
            Here the name of the class is used as key but it could be any class
            parameter.
            return type(future_class_name, future_class_parents, uppercase_attr)
            这种方式其实不是OOP。我们直接调用了type，而且我们没有改写父类的new方法
            现在让我们这样去处理:
            return type.__new__(upperattr_metaclass, future_class_name, future_class_parents, uppercase_attr)
        """
        cls.REGISTRY[new_cls.__name__] = new_cls
        return new_cls

    @classmethod
    def get_registry(cls):
        return dict(cls.REGISTRY)


class BaseRegisteredClass(object):
    __metaclass__ = RegistryHolder
    """
        Any class that will inherits from BaseRegisteredClass will be included
        inside the dict RegistryHolder.REGISTRY, the key being the name of the
        class and the associated value, the class itself.
        你可以在写一个类的时候为其添加metaclass属性，Python会在类的定义中寻找metaclass属性，
        如果找到了，Python就会用它来创建这个类，如果没有找到，继续在父类中寻找metaclass属性，
        并尝试做和前面同样的操作，如果还没有，就会用内建的type来创建这个类。
        你可以在metaclass中放置些什么代码呢？
        答案就是：可以创建一个类的东西。那么什么可以用来创建一个类呢？type，或者任何使用到type或者子类化type的东东都可以。
    """
    pass

if __name__ == "__main__":
    print("Before subclassing: ")
    for k in RegistryHolder.REGISTRY:
        print(k)

    class ClassRegistree(BaseRegisteredClass):

        def __init__(self, *args, **kwargs):
            pass

    print("After subclassing: ")
    for k in RegistryHolder.REGISTRY:
        print(k)

###  OUTPUT ###
# Before subclassing:
# BaseRegisteredClass
# After subclassing:
# BaseRegisteredClass
# ClassRegistree
