# LX-225 bench engineering instructions

## Scope and source of truth

The reusable driver is `servo_testbench.py`, the CLI is `test_servos.py`, and recording/experiments are in `bench_tools.py`. Edit these sources and regenerate both standalone programs with `python tools/build_standalone.py`; do not edit generated copies directly.

Read README and relevant guides before changes. `docs/gaia_lx225.md` defines the actuator boundary; `docs/datasheets/` contains technical references; `docs/validacao-calibracao.md` records validation limits. `docs/digital-twin-roadmap.md` describes planned integration, not implemented ROS hardware support. GAIA joint mechanics belong to the structure repository. OP3 simulation is a reference and does not identify GAIA or provide its physical LX-225 bridge.

## Physical commands and evidence

Before motion, check mode, limits, voltage and temperature; validate all targets before sending any. Never run physical serial tests without confirmed assembly, supply, mechanical limits and operator. Internal servo limits do not establish mechanical safety.

Velocity is ESTIMATED from successive positions; servo feedback is not external metrological ground truth. Current and torque are not measured here. Preserve raw CSV and record assembly, version, units and conditions. Separate REAL, SIMULATED, CALCULATED and ESTIMATED data. Use UNKNOWN / NOT_MEASURED for missing physical information.

## Validation and documentation

`python -m unittest discover -s tests -v` uses simulated serial responses. For source changes, verify regressions and generated-program consistency. Report commands, results and limits; do not claim hardware validation without evidence. A passing software test does not validate an assembly or certify a stop mechanism.

English is primary for new R&D documentation and maintained entrypoints. Existing Portuguese technical guides and paths remain during migration; label partial language coverage honestly and preserve useful links. Preserve third-party attribution/provenance and do not invent licensing rights; no root LICENSE is currently supplied.

Definition of Done: appropriate regression checks, consistent generated files when applicable, documented limitations and evidence, and no unsupported hardware or Digital Twin claims.
