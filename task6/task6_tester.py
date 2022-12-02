import math
import unittest



class Calculator:
    def __init__(self):
        pass

    def distance(self, s_x, s_y, x, y):
        return math.sqrt((x - s_x) * (x - s_x) + (y - s_y) * (y - s_y))

    def time_to_move(self, distance, velocity_ms):
        return math.fabs(distance / velocity_ms)

    def turning_angle(self, s_x, s_y, x, y):
        angl = math.acos(((x * s_x + y * s_y) / (math.sqrt(x * x + y * y) * math.sqrt(s_x * s_x + s_y * s_y)))) * 180 / math.pi
        direction = math.degrees(math.atan2(x - s_x, y - s_y))
        if direction > 0:
            return -1 * angl
        else:
            return angl

    def time_to_turn(self, angle, angle_velocity_degs):
        return math.fabs(angle / angle_velocity_degs)


class TestCalculator(unittest.TestCase):

    def setUp(self):
        self.calculator = Calculator()
        
    def test_distance(self):
        self.assertEqual(self.calculator.distance(2.0,2.0,0.0,0.0), 2.8284271247461903)

    def test_time_to_move(self):
        self.assertEqual(self.calculator.time_to_move(1.0, 1.3),  0.7692307692307692)

    def test_turning_angle(self):
        self.assertEqual(self.calculator.turning_angle(0.0,1.0,-1.0,0.0), 90)
        self.assertEqual(self.calculator.turning_angle(0.0,1.0,-1.0,0.0), -90)#intentionally failed

    def test_time_to_turn(self):
        self.assertEqual(self.calculator.time_to_turn(90,20), 4.5)



if __name__ == "__main__":
    unittest.main()
