# North Vacation Booking - stub implementation
#
# NOTE: this is black-box testing so we dont really get the app code.
# I made this little version myself just so my tests have something to run
# against. When the real app shows up you can delete this and point the
# tests at the real Reservation class instead.
#
# I tried to follow the requirements exactly:
#  - nights has to be 1 to 31
#  - guests has to be 1 to 12
#  - $200 a night
#  - $50 cleaning fee one time
#  - every guest over 5 is +$25 per night
#  - checkin before checkout
#  - nights = checkout - checkin (dont count checkout day)
#  - all nights have to be available
#  - bad info = ValueError, not available = UnavailableError

from datetime import date, timedelta


NIGHT_PRICE = 200
CLEANING_FEE = 50
EXTRA_GUEST_PRICE = 25
FREE_GUESTS = 5  # guests up to 5 dont cost extra

MIN_NIGHTS = 1
MAX_NIGHTS = 31
MIN_GUESTS = 1
MAX_GUESTS = 12


class UnavailableError(Exception):
    # raised when a night in the range is already taken
    pass


class Reservation:
    def __init__(self, check_in, check_out, guests, booked_nights=None):
        # booked_nights is a set of date objects that are already taken.
        # if you dont pass it in we just say everything is open.
        if booked_nights is None:
            booked_nights = set()

        # ---- check the dates ----
        # checkin has to be before checkout
        if check_in >= check_out:
            raise ValueError("check-in date must be before the checkout date")

        # ---- figure out the nights ----
        nights = (check_out - check_in).days  # dont count checkout day

        # ---- check the nights ----
        if nights < MIN_NIGHTS or nights > MAX_NIGHTS:
            raise ValueError("number of nights must be between 1 and 31")

        # ---- check the guests ----
        if guests < MIN_GUESTS or guests > MAX_GUESTS:
            raise ValueError("number of guests must be between 1 and 12")

        # ---- check availability ----
        # go through every night in the range and make sure its open.
        # the checkout day is not a reserved night so we stop before it.
        night = check_in
        while night < check_out:
            if night in booked_nights:
                raise UnavailableError("one of the nights is not available")
            night = night + timedelta(days=1)

        # if we got here everything is good, save it
        self.check_in = check_in
        self.check_out = check_out
        self.guests = guests
        self.nights = nights

    def total_cost(self):
        # base is nights times the night price
        cost = self.nights * NIGHT_PRICE

        # one time cleaning fee
        cost = cost + CLEANING_FEE

        # extra guests (anyone over 5) cost 25 each per night
        extra_guests = self.guests - FREE_GUESTS
        if extra_guests > 0:
            cost = cost + (extra_guests * EXTRA_GUEST_PRICE * self.nights)

        return cost
