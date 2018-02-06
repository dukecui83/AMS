#!/usr/bin/env python
# coding: utf-8

from ams.structures import Target as Structure


class Target(object):

    @staticmethod
    def new_target(_id, group):
        return Structure.new_data(
            id=_id,
            group=group
        )

    @staticmethod
    def new_node_target(node):
        if isinstance(node, type):
            return Target.new_node_target(None, node.__name__)
        else:
            return Target.new_node_target(node.event_loop_id, node.__class__.__name__)

    validate_target = Structure.validate_data
    get_errors = Structure.get_errors
