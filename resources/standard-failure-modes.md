# Standard Failure-Mode Checklist (PFMEA)

A reference list of common process failure modes. When drafting a PFMEA (workflow
`draft-pfmea.md`, step 3), check each process step against the relevant categories so
"standard" failure modes are never forgotten. Not every item applies to every step — use
judgement, and add process-specific modes beyond this list.

## Generic process failure modes (apply to most steps)
- Operation not performed / omitted (step skipped)
- Operation performed incompletely / partially
- Operation performed too much (over-process, over-torque, over-fill)
- Operation performed too little (under-process, under-torque, under-fill)
- Wrong sequence / out of order
- Right action, wrong part or wrong location
- Wrong setting / wrong parameter (temperature, pressure, speed, time)
- Performed too early / too late (timing)
- Wrong material / wrong component used (mix-up)
- Contamination introduced (dirt, oil, moisture, foreign object/FOD)
- Damage during handling (scratch, dent, deform, ESD)

## Assembly & joining
- Missing component / fastener
- Loose / under-torqued joint; over-torqued (stripped, cracked)
- Cross-threaded; wrong fastener
- Misaligned / mispositioned parts
- Incomplete weld/solder/bond; cold joint; insufficient adhesive
- Wrong polarity / orientation (connector, electronic part)
- Trapped/pinched wire, seal, or O-ring

## Machining / forming / molding
- Out of dimensional tolerance (over/under size)
- Surface finish defect (roughness, burr, flash)
- Crack / fracture / porosity / void
- Warp / distortion; residual stress
- Tool wear producing drift; chatter marks

## Measurement, inspection & test
- Defect not detected (escape) / false accept
- Good part rejected (false reject)
- Measurement error (gauge out of calibration, wrong method)
- Test skipped or test condition wrong
- Mislabeled pass/fail result

## Material handling, identification & traceability
- Wrong label / no label / unreadable label
- Lot/serial mix-up; loss of traceability
- FIFO not followed; expired/aged material used
- Incorrect quantity (over/under count)
- Storage damage / wrong storage condition

## Electrical / electronic specific
- Open circuit / short circuit
- Intermittent connection
- Component value out of spec
- Software/firmware not loaded or wrong version
- ESD damage; reverse polarity
