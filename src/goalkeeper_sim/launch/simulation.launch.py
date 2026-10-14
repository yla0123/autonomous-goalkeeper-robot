import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, SetEnvironmentVariable
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node

def generate_launch_description():
    # Pfade zu euren Paketen ermitteln
    sim_pkg = get_package_share_directory('goalkeeper_sim')
    desc_pkg = get_package_share_directory('goalkeeper_description')

    # Pfade zu den Dateien
    world_file = os.path.join(sim_pkg, 'worlds', 'goalkeeper_world.sdf')
    urdf_file = os.path.join(desc_pkg, 'urdf', 'goalkeeper.urdf')
    models_path = os.path.join(sim_pkg, 'models')

    # Gazebo-Umgebungsvariable setzen, damit Modelle (wie der soccer_ball) gefunden werden
    set_env_vars = SetEnvironmentVariable(
        name='GZ_SIM_RESOURCE_PATH',
        value=models_path
    )

    # URDF-Inhalt einlesen
    with open(urdf_file, 'r') as infp:
        robot_description_content = infp.read()

    # 1. Robot State Publisher (veröffentlicht die Roboter-Struktur für ROS 2)
    robot_state_publisher_node = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        output='screen',
        parameters=[{'robot_description': robot_description_content, 'use_sim_time': True}]
    )

    # 2. Gazebo (Ignition / Harmonic) mit eurer Welt starten
    gz_sim_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(get_package_share_directory('ros_gz_sim'), 'launch', 'gz_sim.launch.py')
        ),
        launch_arguments={'gz_args': f'-r {world_file}'}.items()
    )

    # 3. Den Roboter aus dem ROS-2-Thema in die Gazebo-Simulation spawnen
    spawn_robot = Node(
        package='ros_gz_sim',
        executable='create',
        arguments=[
            '-topic', 'robot_description',
            '-name', 'goalkeeper_robot',
            '-x', '10.0', '-y', '0.0', '-z', '0.5'  # Position direkt vor dem Tor anpassen
        ],
        output='screen'
    )

    return LaunchDescription([
        set_env_vars,
        gz_sim_launch,
        robot_state_publisher_node,
        spawn_robot
    ])