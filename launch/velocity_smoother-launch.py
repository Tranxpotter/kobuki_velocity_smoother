# -*- coding: utf-8 -*-
#
# Copyright (c) 2020 Open Source Robotics Foundation, Inc.
#
# Software License Agreement (BSD License 2.0)
#   https://raw.githubusercontent.com/kobuki-base/velocity_smoother/license/LICENSE

"""Launch the velocity smoother node with default configuration."""

import os

import ament_index_python.packages
import launch
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
import launch_ros.actions

import yaml


def generate_launch_description():
    share_dir = ament_index_python.packages.get_package_share_directory('kobuki_velocity_smoother')

    use_sim_time = LaunchConfiguration('use_sim_time')

    declare_use_sim_time_cmd = DeclareLaunchArgument(
        'use_sim_time',
        default_value='false',
        description='Use simulation (Gazebo) clock if true'
    )

    params_file = os.path.join(share_dir, 'config', 'velocity_smoother_params.yaml')
    with open(params_file, 'r') as f:
        params = yaml.safe_load(f)['kobuki_velocity_smoother']['ros__parameters']
    
    params['use_sim_time'] = use_sim_time

    velocity_smoother_node = launch_ros.actions.Node(
        package='kobuki_velocity_smoother',
        executable='velocity_smoother',
        name='velocity_smoother',
        output='both',
        parameters=[params])

    return launch.LaunchDescription([
        declare_use_sim_time_cmd,
        velocity_smoother_node
    ])