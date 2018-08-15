#!/usr/bin/env python
# coding: utf-8

from ams.helpers import Target, Schedule
from ams.nodes.vehicle import EventLoop as VehicleEventLoop
from ams.nodes.autoware_dispatcher import Message as DispatcherMessage
from ams.nodes.autoware_dispatcher import CONST as AUTOWARE_DISPATCHER
from ams.nodes.autoware import CONST, Structure, Message, Helper, Publisher, StateMachine, Subscriber


class EventLoop(VehicleEventLoop):

    CONST = CONST
    Structure = Structure
    Message = Message
    Helper = Helper
    Publisher = Publisher
    StateMachine = StateMachine
    Subscriber = Subscriber

    DISPATCHER = AUTOWARE_DISPATCHER
    DispatcherMessage = DispatcherMessage

    def __init__(self, _id, group=CONST.NODE_NAME):
        super().__init__(_id, group)

        self.upper_distance_from_stopline = CONST.DEFAULT_UPPER_DISTANCE_FROM_STOPLINE

    def __set_autoware_subscriber(self):
        topic = self.Subscriber.get_closest_waypoint_topic(self.user_data["target_roles"])
        self.subscribers[topic] = {
            "topic": topic,
            "callback": self.Subscriber.on_closest_waypoint_ros_message,
            "structure": self.Structure.ROSMessage.ClosestWaypoint,
            "user_data": self.user_data
        }

        topic = self.Subscriber.get_current_pose_topic(self.user_data["target_roles"])
        self.subscribers[topic] = {
            "topic": topic,
            "callback": self.Subscriber.on_current_pose_ros_message,
            "structure": self.Structure.ROSMessage.CurrentPose,
            "user_data": self.user_data
        }

        topic = self.Subscriber.get_decision_maker_state_topic(self.user_data["target_roles"])
        self.subscribers[topic] = {
            "topic": topic,
            "callback": self.Subscriber.on_decision_maker_state_ros_message,
            "structure": self.Structure.ROSMessage.DecisionMakerState,
            "user_data": self.user_data
        }

    def set_initial_config(
        self, activation, target_ros_id=None,
        upper_distance_from_stopline=CONST.DEFAULT_UPPER_DISTANCE_FROM_STOPLINE, target_dispatcher_id=None
    ):
        self.initials["config"] = self.Structure.Config.new_data(
            activation=activation,
            upper_distance_from_stopline=upper_distance_from_stopline,
            target_ros=Target.new_target(
                self.CONST.ROS.NODE_NAME,
                target_ros_id if target_ros_id is not None else Schedule.get_id()),
            target_dispatcher=Target.new_target(
                self.DISPATCHER.NODE_NAME,
                target_dispatcher_id if target_dispatcher_id is not None else Schedule.get_id()),
        )
        self.user_data["target_roles"][self.CONST.ROS.ROLE_NAME] = self.initials["config"].target_ros
        self.user_data["target_roles"][self.DISPATCHER.ROLE_NAME] = self.initials["config"].target_dispatcher

    def set_initial_status(
            self, state=CONST.STATE.START_PROCESSING, schedule_id=None, location=None, pose=None, velocity=0.0,
            route_code=None, current_pose=None, closest_waypoint=None, decision_maker_state=None):
        self.initials["status"] = self.Structure.Status.new_data(
            state=state,
            schedule_id=schedule_id,
            location=location,
            pose=pose,
            velocity=velocity,
            route_code=route_code,
            current_pose=current_pose,
            closest_waypoint=closest_waypoint,
            decision_maker_state=decision_maker_state,
            updated_at=Schedule.get_time()
        )

    def start(self):
        self.__set_vehicle_subscriber()
        self.__set_autoware_subscriber()

        self.__connect_and_subscribe()

        self.Helper.set_vehicle_config(
            self.user_data["clients"], self.user_data["target_roles"], self.initials["config"])
        self.Helper.set_vehicle_status(
            self.user_data["clients"], self.user_data["target_roles"], self.initials["status"])

    def stop(self):
        self.user_data["clients"]["pubsub"].disconnect()