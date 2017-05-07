# Work In Progress

# Calendar Fetching
- all calendars from all posts are fetched every 24 hours (spaced out by post)
- if there is a reservation from a post, that post is fetched every N minutes (possible monetization for faster?)

# Diffs
- check for diffs by each site, log volatility (how many cancellations/new appointments)
- check diffs for each appointment range

# Data Types

## Reservation
  `start_date`
  `end_date`
  `postcode`
      - values can be pulled with `scrape_cities.py`
  `countrycode`
      - values can be pulled with `scrape_cities.py`
  `servicetype`
     - AA = Passport Services
     - 02B = Birth Abroad
     - 09 = Notary and Other
  `type_`
     - 1 = Passport Appointment
     - 2 = Birth Abroad
     - 3 = Notary and other
     - 4 = Add visa pages (no longer possible)
  `contact`

## Appointments
   `postcode`
   `countrycode`
   `servicetype`
   `type_`
   `date`
   `available`
   `url`
   `retrieved`

## Contacts
   `name`
   `registered`
   `account_type`
   `phone_number`
      - a dictionary of numbers w/ country codes
   `email`
   `preferred_contact`
      - email / phone

