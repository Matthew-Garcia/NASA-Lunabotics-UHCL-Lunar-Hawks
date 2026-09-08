# Design-review and release checklist

- [ ] Confirm actual drivers, actuators, sensors, power envelope, and pin budget.
- [ ] Create native KiCad schematic and custom symbol/footprint provenance.
- [ ] Verify connector mating views, voltages, default states, and fault behavior.
- [ ] Calculate protection coordination, power dissipation, regulator margins.
- [ ] Review USB backfeed prevention and signal grounding/isolation.
- [ ] Independently review hardware emergency-stop and restart prevention.
- [ ] Run ERC; document every reviewed waiver.
- [ ] Route board with reviewed stack-up, spacing, grounding, thermal and EMC practices.
- [ ] Run DRC and independently review fabrication outputs against schematic.
- [ ] Bring up rails first on a current-limited supply with motors disconnected.
- [ ] Validate boot/reset/brownout, communication loss, sensor faults and disable chain.
- [ ] Release BOM, Gerbers, drill files and assembly drawings only after review.

No item is marked complete merely because its folder exists.
