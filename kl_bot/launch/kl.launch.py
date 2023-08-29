import os

from ament_index_python.packages import get_package_share_directory

import launch
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource

from launch_ros.actions import Node
from launch.substitutions import Command, LaunchConfiguration



def generate_launch_description():


    # Include the robot_state_publisher launch file, provided by our own package. Force sim time to be enabled
    # !!! MAKE SURE YOU SET THE PACKAGE NAME CORRECTLY !!!

    package_name = 'kl_bot' #<--- CHANGE ME

    rsp = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([os.path.join(
            get_package_share_directory(package_name), 'launch', 'rsp.launch.py'
        )]), launch_arguments={'use_sim_time': 'true', 'use_ros2_control': 'false'}.items()
    )

    gazebo_params_file = os.path.join(get_package_share_directory(package_name), 'config', 'gazebo_params.yaml')

    #default_rviz_config_path = os.path.join(get_package_share_directory(package_name), 'worlds', 'nav2_config.rviz')

    #add the word

    world_path = os.path.join(get_package_share_directory('kl_bot'), 'worlds' , 'wordtest.sdf')

    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([os.path.join(
            get_package_share_directory('gazebo_ros'), 'launch', 'gazebo.launch.py')]),
        launch_arguments={'extra_gazebo_args': '--ros-args --params-file ' + gazebo_params_file}.items()
    )

    # Include the Gazebo launch file, provided by the gazebo_ros package
    gazebo1 = IncludeLaunchDescription(
                PythonLaunchDescriptionSource([os.path.join(
                    get_package_share_directory('gazebo_ros'), 'launch', 'gazebo.launch.py')]),
             )

    # Run the spawner node from the gazebo_ros package. The entity name doesn't really matter if you only have a single robot.
    #spawn_entity = Node(package='gazebo_ros', executable='spawn_entity.py', arguments=['-topic', 'robot_description',  '-entity', 'my_bot'], output='screen')

    spawn_entity = Node(
        package='gazebo_ros',
        executable='spawn_entity.py',
        name='urdf_spawner',
        arguments=['-entity', 'rover', '-topic', 'robot_description'],
        output='screen'
    )

    diff_drive_spawner = Node(
        package="controller_manager",
        executable="spawner.py",
        arguments=["diff_cont"],
    )

    joint_broad_spawner = Node(
        package="controller_manager",
        executable="spawner.py",
        arguments=["joint_broad"],
    )

    rviz_node = Node(
        package='rviz2',
        executable='rviz2',
        name='rviz2',
        output='screen',
        parameters=[LaunchConfiguration('use_sim_time')],
        arguments=['-d', LaunchConfiguration('rvizconfig')])

    static_transform = Node(package="tf2_ros",
                            executable="static_transform_publisher",
                            # arguments = ["-5.0", "-30.0", "0.", "0.0", "0", "0.0", "map", "odom"])
                            arguments=["0.0", "0.0", "0.", "0.0", "0", "0.0", "map", "odom"])


    # Launch them all!
    return LaunchDescription([

        launch.actions.ExecuteProcess(
            cmd=['gazebo', '--verbose', '-s', 'libgazebo_ros_init.so', '-s', 'libgazebo_ros_factory.so', world_path],
            output='screen'),

        # launch.actions.DeclareLaunchArgument(name='rvizconfig', default_value=default_rviz_config_path,
        #                                      description='Absolute path to rviz config file'),

        rsp,
        #static_transform,
        #gazebo,
        spawn_entity,
        #diff_drive_spawner,
        #joint_broad_spawner,
        #rviz_node
        #gazebo
    ])
