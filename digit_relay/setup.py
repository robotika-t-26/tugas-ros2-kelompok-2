import os
from glob import glob

from setuptools import setup

package_name = 'digit_relay'

setup(
    name=package_name,
    version='0.1.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages', ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),

        (os.path.join('share', package_name, 'launch'), glob('launch/*.launch.py')),
        (os.path.join('share', package_name, 'config'), glob('config/*.yaml')),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='Kelompok TODO',
    maintainer_email='todo@example.com',
    description='Distributed Digit Relay di turtlesim',
    license='MIT',
    entry_points={
        'console_scripts': [
            'member1 = digit_relay.member1:main',
            'member2 = digit_relay.member2:main',
            'member3 = digit_relay.member3:main',
            'member4 = digit_relay.member4:main',
            'member5 = digit_relay.member5:main',
            'member6 = digit_relay.member6:main',
        ],
    },
)
