import unittest

from bookings import calculate_price


class TestCalculatePrice(unittest.TestCase):
    def test_two_guests_pay_the_base_rate(self):
        # rate 100, 3 nights, 2 guests: (100 + 0) x 3
        self.assertEqual(300.00, calculate_price(100.0, 3, 2))

    def test_first_extra_guest_adds_ten_pounds_a_night(self):
        self.assertEqual(220.00, calculate_price(100.0, 2, 3))

    def test_one_guest_pays_the_base_rate(self):
        self.assertEqual(100.00, calculate_price(100.0, 1, 1))

    def test_zero_nights_is_rejected(self):
        with self.assertRaises(ValueError):
            calculate_price(100.0, 0, 2)


if __name__ == "__main__":
    unittest.main()
