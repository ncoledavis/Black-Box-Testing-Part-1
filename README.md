# Black-Box Testing Part 1 - North Vacation Booking

Class: AD361 Application Testing

So for this one we dont get the code, we just test off the requirements. I read the requirements a bunch of times and tried to pull out everything that needs tested and kind of worked backwords from there.

## Step 1: Identify the Equivalence Partitions

First I went through the requirements and found the stuff that gets input or calculated. Here is what I think needs to be tested (the classifications):

1. Number of nights
2. Number of guests
3. Check-in and checkout dates
4. Availability

I also noticed the price is calculated from the nights and guests, so the price kind of gets tested at the same time when I test valid reservations.

Then for each one I figured out the valid and invalid conditions, split them into partitions (groups that act the same), and picked a value out of each group to use as my test input.

The rules I used (straight from requirements):

- nights has to be 1 to 31 (both counted)
- guests has to be 1 to 12 (both counted)
- $200 each night
- $50 cleaning fee one time only
- every guest OVER 5 is +$25 per night each
- check-in has to be before checkout
- nights = checkout - checkin, and you dont count the checkout day
- all the nights in the range have to be open/available
- bad info = ValueError
- not available = UnavailableError

### How I picked the representative values

For a range like 1 to 31 I picked something in the middle-ish for the valid one, and then 0 and 32 for the invalid ones because those are right outside the line. (I know boundary testing is a different thing but these were just easy to grab for the invalid partitions.)

## Step 2: Equivalence Partition Tables

### Number of nights

| Classification   | Partition    | Range or Condition      | Expected Result |
| ---------------- | ------------ | ----------------------- | --------------- |
| Number of nights | Invalid low  | less than 1 night (0)   | ValueError      |
| Number of nights | Valid        | 1 to 31 nights          | reservation accepted, $200 per night |
| Number of nights | Invalid high | more than 31 nights     | ValueError      |

### Number of guests

| Classification   | Partition             | Range or Condition  | Expected Result |
| ---------------- | --------------------- | ------------------- | --------------- |
| Number of guests | Invalid low           | fewer than 1 guest  | ValueError      |
| Number of guests | Valid, standard rate  | 1 to 5 guests       | accepted, no extra guest fee |
| Number of guests | Valid, additional fee | 6 to 12 guests      | accepted, +$25 per guest over 5, per night |
| Number of guests | Invalid high          | more than 12 guests | ValueError      |

### Check-in and checkout dates

| Classification | Partition          | Range or Condition             | Expected Result |
| -------------- | ------------------ | ------------------------------ | --------------- |
| Dates          | Valid              | check-in is before checkout    | accepted, nights = checkout - checkin |
| Dates          | Invalid (same day) | check-in == checkout (0 nights)| ValueError      |
| Dates          | Invalid (backwards)| check-in is after checkout     | ValueError      |

(I made same-day its own row because that gives 0 nights which is also under the 1 night minimum, so it fails either way. The backwards one is check-in after checkout which the requirement says isnt allowed.)

### Availability

| Classification | Partition     | Range or Condition                 | Expected Result   |
| -------------- | ------------- | ---------------------------------- | ----------------- |
| Availability   | Available     | every night in the range is open   | reservation accepted |
| Availability   | Not available | at least 1 night in range is taken | UnavailableError  |

## Step 3: Test Cases

I wrote at least one test case for every partition from my tables above. For the inputs I used dates that make the nights come out how I want (like Jan 1 to Jan 3 is 2 nights because you dont count checkout).

### Number of nights

TC01 - Valid number of nights
- Classification: Number of nights
- Partition: Valid
- Input: check-in Jan 1 2026, checkout Jan 3 2026 (so 2 nights), 2 guests, all nights available
- Expected Result: reservation accepted. cost = 2 nights * $200 + $50 cleaning = $450

TC02 - Invalid low number of nights
- Classification: Number of nights
- Partition: Invalid low
- Input: 0 nights (check-in Jan 1, checkout Jan 1), 2 guests
- Expected Result: ValueError

TC03 - Invalid high number of nights
- Classification: Number of nights
- Partition: Invalid high
- Input: 32 nights (check-in Jan 1 2026, checkout Feb 2 2026), 2 guests
- Expected Result: ValueError

### Number of guests

TC04 - Valid standard number of guests
- Classification: Number of guests
- Partition: Valid, standard rate
- Input: 3 guests, 2 nights, available
- Expected Result: accepted, no extra guest fee. cost = $400 + $50 = $450

TC05 - Valid guests with additional fee
- Classification: Number of guests
- Partition: Valid, additional fee
- Input: 8 guests, 2 nights, available
- Expected Result: accepted. 8 guests means 3 guests are over 5. extra = 3 * $25 * 2 nights = $150. cost = $400 + $50 + $150 = $600

TC06 - Invalid low number of guests
- Classification: Number of guests
- Partition: Invalid low
- Input: 0 guests, 2 nights
- Expected Result: ValueError

TC07 - Invalid high number of guests
- Classification: Number of guests
- Partition: Invalid high
- Input: 13 guests, 2 nights
- Expected Result: ValueError

### Dates

TC08 - Valid dates
- Classification: Dates
- Partition: Valid
- Input: check-in Jan 1 2026, checkout Jan 5 2026, 2 guests, available
- Expected Result: accepted, nights = 4

TC09 - Invalid dates, same day
- Classification: Dates
- Partition: Invalid (same day)
- Input: check-in Jan 1 2026, checkout Jan 1 2026, 2 guests
- Expected Result: ValueError

TC10 - Invalid dates, check-in after checkout
- Classification: Dates
- Partition: Invalid (backwards)
- Input: check-in Jan 5 2026, checkout Jan 1 2026, 2 guests
- Expected Result: ValueError

### Availability

TC11 - Available reservation
- Classification: Availability
- Partition: Available
- Input: check-in Jan 1 2026, checkout Jan 3 2026, 2 guests, all those nights open
- Expected Result: accepted

TC12 - Not available reservation
- Classification: Availability
- Partition: Not available
- Input: check-in Jan 1 2026, checkout Jan 3 2026, 2 guests, but Jan 2 is already booked
- Expected Result: UnavailableError

## Bonus: Boundary Value Tests

Equivalence partitioning picks a value from the middle of each group, but my instructor said bugs like to hide right on the edges (off by one errors) so I added some boundary tests too. These hit the exact edge numbers and the numbers just outside.

| Test | Input | Expected Result |
| ---- | ----- | --------------- |
| nights = 0 | checkout same as checkin | ValueError |
| nights = 1 | Jan 1 to Jan 2 | accepted, cost $250 |
| nights = 31 | Jan 1 to Feb 1 2026 | accepted |
| nights = 32 | Jan 1 to Feb 2 2026 | ValueError |
| guests = 0 | 0 guests | ValueError |
| guests = 1 | 1 guest | accepted, no extra fee |
| guests = 12 | 12 guests, 2 nights | accepted, cost $800 |
| guests = 13 | 13 guests | ValueError |
| guests = 5 | 5 guests, 2 nights | accepted, no extra fee ($450) |
| guests = 6 | 6 guests, 2 nights | accepted, extra fee starts ($500) |

The 5 vs 6 one is important because thats the line where the extra $25 per guest kicks in. 5 is the last free one and 6 is the first one that costs extra.

## How To Run Everything

```
python3 --version
```

### Run all the tests

Open a terminal in this folder (the Black-Box Testing Part 1 folder) and run:

```
python3 -m unittest test_booking.py
```

If you want to see each test name and if it passed, add the -v (verbose):

```
python3 -m unittest test_booking.py -v
```

When everything passes you should see `OK` at the bottom and it says it ran 22 tests.

### Run just one group of tests

If you only want the main equivalence partition tests:

```
python3 -m unittest test_booking.TestBooking -v
```

If you only want the bonus boundary tests:

```
python3 -m unittest test_booking.TestBoundaries -v
```

### Run just one single test

Like if you only want to check TC05:

```
python3 -m unittest test_booking.TestBooking.test_TC05_valid_extra_fee_guests -v
```

### Note

On some computers the command is just `python` instead of `python3`. If `python3` doesnt work try:

```
python -m unittest test_booking.py -v
```
