# ClassSession links to Instruments via M2M, not via a Course FK

A teacher at the academy can be present during a single time slot and teach multiple instruments to different students simultaneously. The original model used a `Course` entity (one per instrument) with separate overlapping `ClassSession` records per teacher — which required disabling the teacher overlap validation. We replaced this with a direct M2M between `ClassSession` and `Instrument`, so one session record represents one teacher presence and can cover multiple instruments. The overlap validation can be re-enabled cleanly.

## Considered Options

- **Separate ClassSession per Course/Instrument (original):** Simple FK, but forced disabling of overlap validation and created duplicate session records for the same teacher timeslot.
- **ClassSession → Instruments M2M (chosen):** Accurately models a teacher's presence; overlap validation works correctly; one row in the schedule per teacher timeslot.
