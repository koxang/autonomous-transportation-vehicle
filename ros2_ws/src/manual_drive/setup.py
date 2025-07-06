from setuptools import setup

package_name = 'manual_drive'

setup(
    name=package_name,
    version='0.0.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages',
         ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools', 'flask'],
    zip_safe=True,
    maintainer='rob',
    maintainer_email='rob@example.com',
    description='Manual drive with Flask and ROS 2',
    license='MIT',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'manual_drive_node = manual_drive.manual_drive_node:main',
            'hoverboard_controller = manual_drive.hoverboard_controller:main',
        ],
    },
)

