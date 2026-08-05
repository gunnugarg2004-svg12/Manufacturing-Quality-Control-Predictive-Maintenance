# Manufacturing Quality Control & Predictive Maintenance Analytics

Exactly **400,000 business rows** across **12 related CSV tables**.

## Realistic business rules
- Older and critical machines fail more often.
- Sensor readings deteriorate 1–7 days before linked failures.
- Failures create corrective/emergency maintenance.
- Failures and maintenance create downtime and financial losses.
- Downtime reduces production and availability.
- Supplier quality, product complexity, operator skill, shift, and machine age affect defect rates.
- Defects increase scrap, rework, inspection failure, and quality loss.

## ML targets
- sensor_readings.failure_within_7_days
- quality_inspections.inspection_result
- maintenance_work_orders.total_maintenance_cost_inr
- production_batches.downtime_hours

## Intentional cleaning issues
Missing values, inconsistent shift labels, sensor outliers, energy outliers, and class imbalance.
