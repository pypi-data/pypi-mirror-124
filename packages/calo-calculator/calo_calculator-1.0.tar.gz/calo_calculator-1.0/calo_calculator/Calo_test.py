import unittest

from Calo import Calo

class TestCaloClass(unittest.TestCase):
    def setUp(self):
        self.calo_female = Calo("female", 31, 60, 165)
        self.calo_male = Calo("male", 40, 100, 170)
        self.calo_none = Calo("none", 31, 60, 165)
        self.calo_height = Calo("male", 31, 60, -4)
        
    def test_valid_inputs_activity1f(self):
        assert self.calo_female.calculate_calo(1) == 1578.3
        
    def test_valid_inputs_activity2f(self):
        assert self.calo_female.calculate_calo(2) == 1808.47
        
    def test_valid_inputs_activity4f(self):
        assert self.calo_female.calculate_calo(5) == 2498.97

    def test_valid_inputs_activity1m(self):
        assert self.calo_male.calculate_calo(1) == 2241
        
    def test_valid_inputs_activity2m(self):
        assert self.calo_male.calculate_calo(3) == 2894.62
        
    def test_valid_inputs_activity4m(self):
        assert self.calo_male.calculate_calo(4) == 3221.44
        