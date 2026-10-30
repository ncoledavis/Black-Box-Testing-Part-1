# Test cases for North Vacation Booking
# These match the test cases TC01 - TC12 in my black-box-testing-part-1.md file.
# Im using unittest because thats what we did in class.
#
# to run these: python -m unittest test_booking.py

import unittest
from datetime import date

from booking import Reservation, UnavailableError


class TestBooking(unittest.TestCase):

    # ---------- Number of nights ----------

    def test_TC01_valid_nights(self):
        # TC01 valid number of nights
        # Jan 1 to Jan 3 is 2 nights (dont count checkout)
        r = Reservation(date(2026, 1, 1), date(2026, 1, 3), 2)
        self.assertEqual(r.nights, 2)
        # 2 nights * 200 + 50 cleaning = 450
        self.assertEqual(r.total_cost(), 450)

    def test_TC02_invalid_low_nights(self):
        # TC02 invalid low, 0 nights (same day)
        with self.assertRaises(ValueError):
            Reservation(date(2026, 1, 1), date(2026, 1, 1), 2)

    def test_TC03_invalid_high_nights(self):
        # TC03 invalid high, 32 nights (Jan 1 to Feb 2)
        with self.assertRaises(ValueError):
            Reservation(date(2026, 1, 1), date(2026, 2, 2), 2)

    # ---------- Number of guests ----------

    def test_TC04_valid_standard_guests(self):
        # TC04 valid standard rate, 3 guests, no extra fee
        r = Reservation(date(2026, 1, 1), date(2026, 1, 3), 3)
        # still just 400 + 50 = 450 because nobody is over 5
        self.assertEqual(r.total_cost(), 450)

    def test_TC05_valid_extra_fee_guests(self):
        # TC05 valid with additional fee, 8 guests
        r = Reservation(date(2026, 1, 1), date(2026, 1, 3), 8)
        # 3 guests over 5, 3 * 25 * 2 nights = 150
        # 400 + 50 + 150 = 600
        self.assertEqual(r.total_cost(), 600)

    def test_TC06_invalid_low_guests(self):
        # TC06 invalid low, 0 guests
        with self.assertRaises(ValueError):
            Reservation(date(2026, 1, 1), date(2026, 1, 3), 0)

    def test_TC07_invalid_high_guests(self):
        # TC07 invalid high, 13 guests
        with self.assertRaises(ValueError):
            Reservation(date(2026, 1, 1), date(2026, 1, 3), 13)

    # ---------- Dates ----------

    def test_TC08_valid_dates(self):
        # TC08 valid dates, Jan 1 to Jan 5 = 4 nights
        r = Reservation(date(2026, 1, 1), date(2026, 1, 5), 2)
        self.assertEqual(r.nights, 4)

    def test_TC09_invalid_same_day(self):
        # TC09 same day, 0 nights
        with self.assertRaises(ValueError):
            Reservation(date(2026, 1, 1), date(2026, 1, 1), 2)

    def test_TC10_invalid_backwards_dates(self):
        # TC10 checkin after checkout
        with self.assertRaises(ValueError):
            Reservation(date(2026, 1, 5), date(2026, 1, 1), 2)

    # ---------- Availability ----------

    def test_TC11_available(self):
        # TC11 all nights open, should work
        r = Reservation(date(2026, 1, 1), date(2026, 1, 3), 2, booked_nights=set())
        self.assertEqual(r.nights, 2)

    def test_TC12_not_available(self):
        # TC12 Jan 2 is already booked so it should blow up
        taken = {date(2026, 1, 2)}
        with self.assertRaises(UnavailableError):
            Reservation(date(2026, 1, 1), date(2026, 1, 3), 2, booked_nights=taken)


if __name__ == "__main__":
    unittest.main()


# ==========================================================================
# BONUS: Boundary value tests
# ==========================================================================
# Equivalence partitioning picks one value from the middle of a group, but
# boundary testing checks right ON the edges because thats where bugs like
# to hide (off by one stuff). So here I test the exact edge numbers and the
# numbers just outside the edge.
#
# nights edges: 0 (bad), 1 (good), 31 (good), 32 (bad)
# guests edges: 0 (bad), 1 (good), 12 (good), 13 (bad)
# and the 5/6 guest line where the extra fee starts.

class TestBoundaries(unittest.TestCase):

    # ---------- nights boundaries ----------

    def test_nights_0_is_invalid(self):
        # 0 nights, just below the min, should fail
        with self.assertRaises(ValueError):
            Reservation(date(2026, 1, 1), date(2026, 1, 1), 2)

    def test_nights_1_is_valid(self):
        # exactly 1 night, the low edge, should be ok
        # Jan 1 to Jan 2 = 1 night
        r = Reservation(date(2026, 1, 1), date(2026, 1, 2), 2)
        self.assertEqual(r.nights, 1)
        # 1 * 200 + 50 = 250
        self.assertEqual(r.total_cost(), 250)

    def test_nights_31_is_valid(self):
        # exactly 31 nights, the high edge, should be ok
        # Jan 1 to Feb 1 2026 = 31 nights
        r = Reservation(date(2026, 1, 1), date(2026, 2, 1), 2)
        self.assertEqual(r.nights, 31)

    def test_nights_32_is_invalid(self):
        # 32 nights, just over the max, should fail
        with self.assertRaises(ValueError):
            Reservation(date(2026, 1, 1), date(2026, 2, 2), 2)

    # ---------- guests boundaries ----------

    def test_guests_0_is_invalid(self):
        # 0 guests, just below min
        with self.assertRaises(ValueError):
            Reservation(date(2026, 1, 1), date(2026, 1, 3), 0)

    def test_guests_1_is_valid(self):
        # exactly 1 guest, low edge
        r = Reservation(date(2026, 1, 1), date(2026, 1, 3), 1)
        # no extra fee, 400 + 50 = 450
        self.assertEqual(r.total_cost(), 450)

    def test_guests_12_is_valid(self):
        # exactly 12 guests, high edge
        r = Reservation(date(2026, 1, 1), date(2026, 1, 3), 12)
        # 12 - 5 = 7 extra guests, 7 * 25 * 2 nights = 350
        # 400 + 50 + 350 = 800
        self.assertEqual(r.total_cost(), 800)

    def test_guests_13_is_invalid(self):
        # 13 guests, just over max
        with self.assertRaises(ValueError):
            Reservation(date(2026, 1, 1), date(2026, 1, 3), 13)

    # ---------- the 5 / 6 guest fee line ----------

    def test_guests_5_no_extra_fee(self):
        # 5 guests is the last one with no extra fee
        r = Reservation(date(2026, 1, 1), date(2026, 1, 3), 5)
        # 400 + 50 = 450, no extra
        self.assertEqual(r.total_cost(), 450)

    def test_guests_6_starts_extra_fee(self):
        # 6 guests is the first one that costs extra
        r = Reservation(date(2026, 1, 1), date(2026, 1, 3), 6)
        # 1 guest over 5, 1 * 25 * 2 nights = 50
        # 400 + 50 + 50 = 500
        self.assertEqual(r.total_cost(), 500)
