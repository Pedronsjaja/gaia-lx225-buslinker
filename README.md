# LX-225 / BusLinker Test Bench

Python tools for actuator communication, feedback acquisition and reproducible bench experiments with the GAIA team.

**Status: implemented driver / experimental physical integration.** Position, voltage and temperature are read through the serial protocol; velocity is estimated from successive positions. Automated tests use simulated serial responses. They do not certify the physical assembly, electrical safety or metrological accuracy. Current and torque are not measured by this driver.

**R&D role:** physical acquisition for a future single-actuator experiment. ROS 2, ros2_control hardware integration and Gazebo synchronization are **Planned**, not implemented here. The OP3 simulation reference does not define GAIA mechanics or implement the LX-225 hardware bridge. A validated GAIA Digital Twin is not an existing result.

English is the primary language for new R&D documentation and these entrypoints. Most detailed guides below remain in Portuguese during the transition; their existing paths are preserved. This is not a claim of complete English coverage.

[Start safely](docs/instalacao.md) · [Driver interface](docs/gaia_lx225.md) · [Digital Twin roadmap](docs/digital-twin-roadmap.md)

<a id="inicio-rapido"></a>
## Start here

1. Read [GitHub basics](docs/primeiros-passos-github.md) if you are new to the repository.
2. Identify the exact board revision and follow [installation and first checks](docs/instalacao.md), starting with one servo.
3. Read the matching [board manuals and schematics](docs/datasheets/README.md). Board voltage limits and servo voltage limits are different specifications.
4. Confirm assembly, supply, IDs, mechanical limits and operator before physical commands. Begin with state queries, then supervised small movements only after those checks.
5. Record conditions and raw results using the [command guide](docs/uso.md).

The tools support Hiwonder LX-225 communication through BusLinker V2.5 or V3, including position/voltage/temperature queries, test movements, plots, ID management and calibration experiments. Firmware limits do not establish collision-free mechanical travel or replace an independent physical stop.

<a id="guia-do-projeto"></a>
## Documentation and source of truth

| Need | Reference |
| --- | --- |
| Install Python, identify USB port and prepare first checks | [Installation](docs/instalacao.md) |
| LX-225 specifications and V2.5/V3 documentation | [Technical documents](docs/datasheets/README.md) |
| Hiwonder tools and USB drivers | [Software and drivers](docs/softwares-e-drivers.md) |
| Query state, move or run calibration experiments | [Python commands](docs/uso.md) |
| Diagnose errors | [Troubleshooting](docs/solucao-de-problemas.md) |
| Understand supply and bus connections | [LX-225 electronics](docs/eletronica/README.md) |
| Reuse actuator communication in GAIA | [Actuator interface contract](docs/gaia_lx225.md) |
| Understand calibration evidence and limits | [Calibration validation](docs/validacao-calibracao.md) |
| Plan a future physical/virtual joint experiment | [Digital Twin roadmap](docs/digital-twin-roadmap.md) |
| Find servo and support CAD | [Mechanical catalog](https://github.com/Pedronsjaja/gaia-humanoid-structure/blob/main/hardware/README.md) |
| Work on Windows 10/11 or Linux | [Platform installation and tests](docs/windows-linux.md) |

The interface contract explains IDs, joint naming and quantities; examples are not the final GAIA joint map. Joint count, zero, direction, transmission and mechanical limits require an identified assembly. The [mechanical modeling contract](https://github.com/Pedronsjaja/gaia-humanoid-structure/blob/main/docs/modelo-gaia.md) belongs to the structure repository.

## Programs and development

| Board | Standalone program | Class |
| --- | --- | --- |
| BusLinker V2.5 | [buslinker_v2_5.py](buslinker_v2_5.py) | `BusLinkerV2_5` |
| BusLinker V3 | [buslinker_v3.py](buslinker_v3.py) | `BusLinkerV3` |

Install dependencies from [requirements.txt](requirements.txt). Both programs use the LX-225 protocol at 115200 baud. V3 does not mean compatibility with every servo protocol.

To view four plots **without connecting or moving servos**, use the explicit simulated-data demo:

```powershell
python test_servos.py --plot-test
```

The window labels its data **SIMULADOS** (simulated) and remains open until closed. The same argument works with `buslinker_v2_5.py` and `buslinker_v3.py`. The interactive movement menu (`--interactive`, options 2 and 4) instead uses servo feedback; option 4 accepts a distinct absolute target per ID. The program prints its path on startup to help identify old copies.

```text
servo_testbench.py     Shared serial driver
bench_tools.py         Recording, plots, IDs and calibration tools
test_servos.py         Bench command-line interface
buslinker_v2_5.py       Generated standalone V2.5 program
buslinker_v3.py         Generated standalone V3 program
docs/                  Installation, usage, references and diagnostics
tests/                 Tests with simulated serial responses
tools/                 Diagnostics and standalone generation
```

Edit the shared sources and regenerate both standalone programs; do not edit generated copies directly:

```powershell
python tools/build_standalone.py
python -m unittest discover -s tests -v
```

The unit tests use fake serial responses. Passing them does not establish physical safety, timing performance or measurement accuracy. The [Windows/Linux guide](docs/windows-linux.md) covers USB drivers, Python environments, plotting and single-/multi-servo experiments on Windows and Ubuntu/Debian/Mint/Pop!_OS.

## GAIA repositories

| Responsibility | Repository |
| --- | --- |
| LX-225, BusLinker, serial driver and bench experiments | [Actuation](https://github.com/Pedronsjaja/gaia-lx225-buslinker) |
| Gazebo, OP3 reference, ROS 2 and autonomy experiments | [Simulation](https://github.com/Pedronsjaja/gaia-humanoid-simulation) |
| CAD, supports, assembly and physical competition requirements | [Structure](https://github.com/Pedronsjaja/gaia-humanoid-structure) |
| Ubuntu 24.04 and ROS 2 Jazzy environment | [Linux / ROS 2](https://github.com/Pedronsjaja/gaia-ros2-ubuntu24) |

Each repository owns its files, issues and history. Cross-link changes that depend on another area. The former `gaia-humanoid-robot` repository was renamed to this address; simulation and mechanical material moved to the repositories above, with earlier history preserved.

No repository-wide LICENSE file is currently provided here. Preserve third-party notices and reference provenance; do not infer redistribution rights from public availability.

<!-- Legacy section fragments retained for inbound links. -->
<a id="-comece-aqui"></a>
<a id="caminho-do-projeto"></a>
<a id="-documentação"></a>
<a id="comece-aqui"></a>
<a id="qual-programa-usar"></a>
<a id="organização"></a>
<a id="repositórios-da-equipe-gaia"></a>
<a id="windows-1011-e-linux"></a>
