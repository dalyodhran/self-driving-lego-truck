from buildhat import MotorPair

"""
A is for turning
B and C are for forward movement
"""

mBC = MotorPair('B','C')

if __name__ == '__main__':
    print("Running motor BC")
    mAB.run_for_seconds(10)