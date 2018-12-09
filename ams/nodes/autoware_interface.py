#!/usr/bin/env python
# coding: utf-8

from ams import logger
from ams.helpers import Subscriber
from ams.nodes.event_loop import EventLoop
from ams.structures import Vehicle, Autoware
from ams.structures import AutowareInterface as Structure


class AutowareInterface(EventLoop):

    Config = Structure.Config
    Message = Structure.Message

    def __init__(self, config, ros_msgs=None):
        super(AutowareInterface, self).__init__(config)

        self.user_data["target_autoware"] = self.config.target_autoware
        self.user_data["target_vehicle"] = self.config.target_vehicle
        self.user_data["lane_array_structure"] = ros_msgs["LaneArray"]
        self.user_data["state_cmd_structure"] = ros_msgs["String"]
        self.user_data["stop_waypoint_index_structure"] = ros_msgs["Int32"]

        topic = Subscriber.get_route_code_message_topic(
            self.user_data["target_vehicle"], self.user_data["target_autoware"])
        self.subscribers[topic] = {
            "topic": topic,
            "callback": Subscriber.on_route_code_message_publish_lane_array,
            "structure": Vehicle.Message.RouteCode,
            "user_data": self.user_data
        }

        topic = Subscriber.get_state_cmd_topic(self.user_data["target_vehicle"], self.user_data["target_autoware"])
        self.subscribers[topic] = {
            "topic": topic,
            "callback": Subscriber.on_state_cmd_publish,
            "structure": None,
            "user_data": self.user_data
        }

        topic = Subscriber.get_stop_route_point_message_topic(
            self.user_data["target_vehicle"], self.user_data["target_autoware"])
        self.subscribers[topic] = {
            "topic": topic,
            "callback": Subscriber.on_route_point_message_publish_stop_waypoint_index,
            "structure": Vehicle.Message.RoutePoint,
            "user_data": self.user_data
        }

        topic = Autoware.CONST.TOPIC.CURRENT_POSE
        self.ros_subscribers[topic] = {
            "topic": topic,
            "callback": Subscriber.on_current_pose_publish,
            "structure": ros_msgs["PoseStamped"],
            "user_data": self.user_data,
            "rate": 1.0
        }

        topic = Autoware.CONST.TOPIC.VEHICLE_LOCATION
        self.ros_subscribers[topic] = {
            "topic": topic,
            "callback": Subscriber.on_vehicle_location_publish_route_point,
            "structure": ros_msgs["VehicleLocation"],
            "user_data": self.user_data,
            "rate": 1.0
        }

        topic = Autoware.CONST.TOPIC.DECISION_MAKER_STATE
        self.ros_subscribers[topic] = {
            "topic": topic,
            "callback": Subscriber.on_decision_maker_state_publish,
            "structure": ros_msgs["String"],
            "user_data": self.user_data,
            "rate": 1.0
        }

    def loop(self):
        self.user_data["ros_client"].loop(self.dt)
