from setuptools import setup

setup(
    name='rospy2',
    description='A ROS1-like interface for ROS2.',
    license='BSD',
    version='1.0.3',
    url='https://github.com/dheera/rospy2',
    author='Dheera Venkatraman',
    author_email='dheera.removethis@dheera.net',
    install_requires=[],
    py_modules=['rospy2'],
    package_dir = {
        "rospy2": "src/rospy2",
    },
    packages = [
        "rospy2",
    ],
)
