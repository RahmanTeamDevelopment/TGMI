import tgmi.math
import math
import unittest


class TestMinOrNaN(unittest.TestCase):
    def test_returns_nan_if_empty_list_is_passed(self):
        assert math.isnan(
            tgmi.math.min_or_nan([])
        )

    def test_returns_nan_if_nan_is_passed(self):
        assert math.isnan(
            tgmi.math.min_or_nan([float('NaN')])
        )

    def test_returns_value_if_single_value_is_passed(self):
        assert tgmi.math.min_or_nan([10]) == 10

    def test_returns_value_if_single_value_and_nan_are_passed(self):
        assert tgmi.math.min_or_nan([10, float('NaN')]) == 10

    def test_returns_smaller_value_if_two_values_are_passed(self):
        assert tgmi.math.min_or_nan([10, 20]) == 10


class TestMaxOrNaN(unittest.TestCase):
    def test_returns_nan_if_empty_list_is_passed(self):
        assert math.isnan(
            tgmi.math.max_or_nan([])
        )

    def test_returns_nan_if_nan_is_passed(self):
        assert math.isnan(
            tgmi.math.max_or_nan([float('NaN')])
        )

    def test_returns_value_if_single_value_is_passed(self):
        assert tgmi.math.max_or_nan([10]) == 10

    def test_returns_value_if_single_value_and_nan_are_passed(self):
        assert tgmi.math.max_or_nan([10, float('NaN')]) == 10

    def test_returns_larger_value_if_two_values_are_passed(self):
        assert tgmi.math.max_or_nan([10, 20]) == 20


if __name__ == "__main__":
    unittest.main()
