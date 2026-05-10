# KPI Definitions

## Total Bookings
Total number of ride bookings.

## Completed Rides
Total successfully completed rides.

## Completion Rate
Percentage of rides successfully completed.

```DAX
Completion Rate =
DIVIDE([Completed Rides], [Total Bookings], 0)
```

## Customer Cancellation Rate
Percentage of rides cancelled by customers.

```DAX
Customer Cancellation Rate =
DIVIDE([Customer Cancelled], [Total Bookings], 0)
```

## Driver Cancellation Rate
Percentage of rides cancelled by drivers.

```DAX
Driver Cancellation Rate =
DIVIDE([Driver Cancelled], [Total Bookings], 0)
```

## Ride Incomplete
Total incomplete rides.

## Total Revenue
Total booking revenue.

## Avg Booking Value
Average revenue per booking.

## Avg Ride Distance
Average ride distance.

## Avg VTAT Measure
Average vehicle arrival delay.

## Avg CTAT Measure
Average customer readiness delay.

## Ride Efficiency Score
Composite operational efficiency KPI.

```DAX
Ride Efficiency Score =
([Completion Rate] * 0.5)
+
((1 - [Driver Cancellation Rate]) * 0.3)
+
((1 - [Customer Cancellation Rate]) * 0.2)
```
