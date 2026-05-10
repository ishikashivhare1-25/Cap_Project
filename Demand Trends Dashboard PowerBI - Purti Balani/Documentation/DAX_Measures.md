# DAX Measures Documentation

## Total Bookings

```DAX
Total Bookings =
COUNT('rideBookings_preprocessed'[Booking ID])
```

## Completed Rides

```DAX
Completed Rides =
CALCULATE(
    COUNT('rideBookings_preprocessed'[Booking ID]),
    'rideBookings_preprocessed'[Booking Status] = "Completed"
)
```

## Completion Rate

```DAX
Completion Rate =
DIVIDE([Completed Rides], [Total Bookings], 0)
```

## Total Revenue

```DAX
Total Revenue =
SUM('rideBookings_preprocessed'[Booking Value])
```

## Avg Booking Value

```DAX
Avg Booking Value =
AVERAGE('rideBookings_preprocessed'[Booking Value])
```

## Avg Ride Distance

```DAX
Avg Ride Distance =
AVERAGE('rideBookings_preprocessed'[Ride Distance])
```

## Avg VTAT Measure

```DAX
Avg VTAT Measure =
AVERAGE('rideBookings_preprocessed'[Avg VTAT])
```

## Avg CTAT Measure

```DAX
Avg CTAT Measure =
AVERAGE('rideBookings_preprocessed'[Avg CTAT])
```
