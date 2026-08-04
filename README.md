# ReactorOnChip

A Python simulation engine for a virtual industrial piping system — fluid flow, heat transfer, and pressure — with an array of simulated sensors and actuators that communicate over Modbus TCP. Designed to run headless on a Raspberry Pi acting as an embedded field device, exposing live process data to a physical Modbus gateway / SCADA-HMI over Ethernet.

## Background

This project began as a capstone at Maine Maritime Academy's Electronics and Instrumentation Laboratory. The lab's automation curriculum covers field-level and control-level work (PLCs, power/control electronics) but had no material on networking or supervisory-level systems (SCADA/HMI). The goal was to build a teaching platform that spans the full automation stack:

1. **Field level** — a simulated plant with virtual pumps, valves, and pressure/temperature sensors
2. **Control level** — the simulated plant running on a Raspberry Pi 5, standing in for a PLC
3. **Network level** — Modbus TCP communication between the simulated field devices and the outside world
4. **Supervisory level** — an external SCADA HMI (built separately in Ignition) polling/controlling the simulation

**ReactorOnChip is the field/control-level piece**: the simulation engine and the Modbus server that exposes it. It does not include the Ignition HMI itself.

## How it works

### Node-based hydraulic graph
The system is modeled as a graph of `Node` objects (pressure, temperature, flow rate) connected by `Device` objects (pumps, pipes, heat exchangers, sensors). These devices are broken into `DeviceInline` and `DeviceParallel`. The former owns an inlet node and an outlet node and chaining these devices together builds a piping loop. The parallel device class describes everything that doesn't have fluid flow travelling through it. This generally means most sensing elements like temperature and pressure sensors. `NodeManager` creates and tracks every node in the system.

### Devices
All devices derive from a common `Device` base and fall into a few families:
- **`DeviceInline`** — sits in the flow path (pipes, pumps, heat exchangers) and computes minor (fitting/K-factor) losses from flow velocity.
- **`DevicePipe`** — adds major friction losses via the Darcy-Weisbach equation with a Swamee-Jain friction factor, based on pipe roughness, diameter, and length.
- **`DevicePump`** — takes a 0–1 process-point setpoint (percent of max speed) and generates a head-vs-flow pump curve, with first-order lag applied when the setpoint changes.
- **`DevicePlateHX`** / **`special_DeviceInternalEngineHX`** — heat exchangers with thermal mass; the "internal engine" variant also injects heat proportional to a simulated engine load.
- **`DeviceParallel`** and its subclasses (**`DevicePressureSensor`**, **`DeviceTempSensor`**, **`DeviceSpeedSensor`**) — read-only taps that report a node's (or pump's) current state with configurable scaling and random noise via `DeviceSensorBase`.

![A org chart showing inheritance of all of the basic devices](https://github.com/CooperParlee/ReactorOnChip/blob/main/docs/img/orgchart.png?raw=true)

### Solving the operating point
`ControlLoop` aggregates all devices in a loop and solves for the actual operating flow rate: it finds the flow where total major + minor head losses equal the combined pump curve output, using `scipy.optimize.root_scalar` (Brent's method). Once the flow is known, `computeDeltas()` walks the loop from a reference node, applying each device's pressure drop/rise in sequence to update every node's pressure.

![Pump and system curve operating points](https://github.com/CooperParlee/ReactorOnChip/blob/main/docs/img/oppoint.png?raw=true)

### Thermal model and fluid transport
Heat exchanger devices carry thermal mass properties (conductivity, area, specific heat, characteristic length) and compute conduction/convection heat flow against the fluid. Rather than assuming instant mixing, `FluidParcelManager` discretizes the loop's fluid volume into a configurable number of parcels that are advected through devices based on local flow velocity, exchanging heat with whatever thermal device they currently occupy. This gives the simulation realistic transport lag as temperature fronts move around the loop.

### Modbus server
`ModbusManager` (via `pymodbus`) hosts an async Modbus TCP server with holding, input, coil, and discrete-input register blocks:
- **Sensors → registers**: every sensor device is assigned a register address; a background task samples each sensor and writes its (scaled, noisy) value into the datastore roughly 10 times per second, readable by any Modbus client.
- **Registers → simulation**: `register_hr_callback()` lets specific holding registers act as writable setpoints. An external client (SCADA/HMI, PLC, or test script) writing to that register — e.g. a pump speed setpoint or a simulated engine load — triggers a callback that updates the running simulation, closing the control loop.

## Example: `coolantLoop2.py`

The included example builds a two-heat-exchanger cooling water loop (modeled after a central freshwater cooling system) consisting of a pump, an internal "engine" heat exchanger with a settable load, a seawater-cooled heat exchanger held at constant temperature, and connecting pipes. It instruments the loop with pressure sensors at each device boundary, temperature sensors across both heat exchangers, and a pump speed sensor, then:
1. Starts the Modbus TCP server on its own thread.
2. Runs a synchronous update loop that advances the pump, solves the hydraulic operating point, propagates pressure deltas, and steps the fluid parcels.
3. Exposes pump speed and engine load as holding registers that can be written by an external Modbus client to change simulation behavior in real time.

## Project structure

```
coolantLoop2.py       # Example/entry-point simulation (two-HX coolant loop)
src/
  nodes/               # Node, NodeManager, ControlLoop, FluidParcelManager, MagicNode (test signal node)
  devices/              # Pumps, pipes, heat exchangers, sensors, and the shared Device base classes
  material/             # Fluid property definitions (e.g. MaterialWater)
  modBus/                # ModbusManager — the async Modbus TCP server and register mapping
  util/                  # config.ini generation/parsing, Excel logging helper
tests/                 # Early prototypes and standalone Modbus server/client scripts
docs/                  # Original capstone proposal
```

## Setup/Install

It is recommended that you follow Python package best practices and run ReactorOnChip within a virtual environment. I use [venv](https://docs.python.org/3/library/venv.html). After following the instructions included in the venv documentation to create and activate your virtual environment, you will need to install the required packages included in `requirements.txt`, notably `pymodbus`, `numpy`, `scipy`, `matplotlib`, `openpyxl`, and `PyQt6`/`pyqtgraph` (for exploratory plotting/GUI work).

Within the activated virtual environment, the following can be run to install all of the requisite packages:

```bash
pip install -r requirements.txt
```

Simulation and Modbus server behavior (fluid parcel count, update rate, TCP address/port, register block sizes) is controlled by a generated `config.ini`; see `src/util/config.py` for defaults and to regenerate it.

## Running it

```bash
python coolantLoop2.py
```

This starts the Modbus TCP server (address/port from `config.ini`) and begins running the simulation loop. Any Modbus client — a physical gateway, a SCADA HMI, or a simple test script — can then read sensor values from the input/holding registers and write setpoints back to control the simulated plant.

## Status

This is a capstone project (Cooper Parlee, with Alyssa Moody; advised by Brendyn Sarnacki) built for Maine Maritime Academy's Electronics and Instrumentation Lab. The `tests/` directory contains earlier prototypes kept for reference, and some pieces (e.g. `DevicePumpBasic`, `MagicNode`) are exploratory/diagnostic rather than part of the main simulation path.
