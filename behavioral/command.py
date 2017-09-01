#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
*TL;DR80
Encapsulates all information needed to perform an action or trigger an event.
"""

from __future__ import print_function
import os
from os.path import lexists


class MoveFileCommand(object):

    def __init__(self, src, dest):
        self.src = src
        self.dest = dest

    def execute(self):
        self.rename(self.src, self.dest)

    def undo(self):
        self.rename(self.dest, self.src)

    def rename(self, src, dest):
        print(u"renaming %s to %s" % (src, dest))
        os.rename(src, dest)


def main():
    command_stack = []

    # commands are just pushed into the command stack
    command_stack.append(MoveFileCommand('foo.txt', 'bar.txt'))
    command_stack.append(MoveFileCommand('bar.txt', 'baz.txt'))

    # verify that none of the target files exist
    assert(not lexists("foo.txt"))
    assert(not lexists("bar.txt"))
    assert(not lexists("baz.txt"))
    try:
        with open("foo.txt", "w"):  # Creating the file
            pass

        # they can be executed later on
        for cmd in command_stack:
            cmd.execute()

        # and can also be undone at will
        for cmd in reversed(command_stack):
            cmd.undo()
    finally:
        os.unlink("foo.txt")

if __name__ == "__main__":
    main()

# os.unlink() 方法用于删除文件,如果文件是一个目录则返回一个错误。
# os.path.lexists: 主要的区别在于，exists()会自动判断失效的文件链接。如果检查的文件是一个软链接，但这个软连接指向的文件被删除了，会返回False。
# 而lexists()不会做这个检查，只要软连接存在，即使它指向的文件不存在，也返回True。
### OUTPUT ###
# renaming foo.txt to bar.txt
# renaming bar.txt to baz.txt
# renaming baz.txt to bar.txt
# renaming bar.txt to foo.txt
