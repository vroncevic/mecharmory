# Mecharmory - 6-DOF Robotic Arm Motion Studio & Hardware Streamer

<img align="right" src="https://raw.githubusercontent.com/vroncevic/mecharmory/dev/docs/mecharmory_logo.png" width="25%">

**mecharmory** is a standalone desktop motion planning, kinematic validation, and real-time serial controller for 6-DOF robotic arm manipulators running Raspberry Pi Pico (RP2040) C SDK firmware and PCA9685 I2C 16-channel PWM drivers.

Developed in **[python](https://www.python.org/)** code.

The README is used to introduce the modules and provide instructions on
how to install the modules, any machine dependencies it may have and any
other information that should be provided before the modules are installed.

[![mecharmory python checker](https://github.com/vroncevic/mecharmory/actions/workflows/mecharmory_python_checker.yml/badge.svg)](https://github.com/vroncevic/mecharmory/actions/workflows/mecharmory_python_checker.yml) [![mecharmory package checker](https://github.com/vroncevic/mecharmory/actions/workflows/mecharmory_package_checker.yml/badge.svg)](https://github.com/vroncevic/mecharmory/actions/workflows/mecharmory_package_checker.yml) [![mecharmory interface checker](https://github.com/vroncevic/mecharmory/actions/workflows/mecharmory_interface_checker.yml/badge.svg)](https://github.com/vroncevic/mecharmory/actions/workflows/mecharmory_interface_checker.yml) [![mecharmory isp checker](https://github.com/vroncevic/mecharmory/actions/workflows/mecharmory_isp_checker.yml/badge.svg)](https://github.com/vroncevic/mecharmory/actions/workflows/mecharmory_isp_checker.yml) [![mecharmory srp checker](https://github.com/vroncevic/mecharmory/actions/workflows/mecharmory_srp_checker.yml/badge.svg)](https://github.com/vroncevic/mecharmory/actions/workflows/mecharmory_srp_checker.yml) [![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0) [![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/) [![GitHub issues open](https://img.shields.io/github/issues/vroncevic/mecharmory.svg)](https://github.com/vroncevic/mecharmory/issues) [![GitHub contributors](https://img.shields.io/github/contributors/vroncevic/mecharmory.svg)](https://github.com/vroncevic/mecharmory/graphs/contributors)

<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->
**Table of Contents**

- [🚀 Installation](#-installation)
    - [Install using pip](#install-using-pip)
    - [Install using build](#install-using-build)
    - [Install using py setup](#install-using-py-setup)
    - [Install using docker](#install-using-docker)
- [📦 Dependencies](#-dependencies)
- [📁 Tool structure](#-tool-structure)
  - [🏗 Architecture & SOLID Principles](#-architecture--solid-principles)
    - [SOLID Principles Compliance](#solid-principles-compliance)
    - [Automated Quality Gates (`run_quality_gates.sh`)](#automated-quality-gates-run_quality_gatessh)
- [✨ Features](#-features)
- [📝 Mecha Domain-Specific Language (.mecha)](#-mecha-domain-specific-language-mecha)
- [📐 Kinematic & Joint Configuration](#-kinematic--joint-configuration)
- [📡 Unified Serial ASCII Communication Protocol](#-unified-serial-ascii-communication-protocol)
- [📊 Code coverage](#-code-coverage)
- [🛠 Usage](#-usage)
- [📚 Docs](#-docs)
- [👥 Contributing](#-contributing)
- [📄 Copyright and licence](#-copyright-and-licence)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->

### 🚀 Installation

[![mecharmory python3 build](https://github.com/vroncevic/mecharmory/actions/workflows/mecharmory_python3_build.yml/badge.svg)](https://github.com/vroncevic/mecharmory/actions/workflows/mecharmory_python3_build.yml)

Currently there are four ways to install package
* Install process based on using pip mechanism
* Install process based on build mechanism
* Install process based on setup.py mechanism
* Install process based on docker mechanism

##### Install using pip

**mecharmory** is located at **[pypi.org](https://pypi.org/project/mecharmory/)**.

You can install by using pip

```bash
# python3
pip3 install mecharmory
```

##### Install using build

Navigate to release **[page](https://github.com/vroncevic/mecharmory/releases/)** download and extract release archive.

To install **mecharmory** type the following

```bash
tar xvzf mecharmory-x.y.z.tar.gz
cd mecharmory-x.y.z/
# python3
wget https://bootstrap.pypa.io/get-pip.py
python3 get-pip.py 
python3 -m pip install --upgrade setuptools
python3 -m pip install --upgrade pip
python3 -m pip install --upgrade build
pip3 install -r requirements.txt
python3 -m build --no-isolation --wheel
pip3 install ./dist/mecharmory-*-py3-none-any.whl
rm -f get-pip.py
```

##### Install using py setup

Navigate to **[release page](https://github.com/vroncevic/mecharmory/releases)** download and extract release archive.

To install **mecharmory** locate and run setup.py with arguments

```bash
tar xvzf mecharmory-x.y.z.tar.gz
cd mecharmory-x.y.z
# python3
pip3 install -r requirements.txt
python3 setup.py install_lib
python3 setup.py install_egg_info
```

##### Install using docker

You can use Dockerfile to create image/container:

```bash
docker build -t mecharmory:latest .
```

### 📦 Dependencies

**mecharmory** requires next modules and libraries

* [ats-utilities - Python App/Tool/Script Utilities](https://pypi.org/project/ats-utilities/) [![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0) [![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
* [pyserial - Python Serial Port Extension](https://pypi.org/project/pyserial/) [![License: BSD](https://img.shields.io/badge/License-BSD_3--Clause-blue.svg)](https://opensource.org/licenses/BSD-3-Clause)

### 📁 Tool structure

**mecharmory** is based on OOP and Clean Architecture.

Tool structure

<details>
<summary><b>Click to expand framework structure</b></summary>

```bash
    mecharmory/
         ├── core/
         │   ├── __init__.py
         │   ├── model/
         │   │   ├── arm/
         │   │   │   ├── arm_config_defaults.py
         │   │   │   ├── arm_model.py
         │   │   │   ├── arm_preset_defaults.py
         │   │   │   ├── iarm_model.py
         │   │   │   └── __init__.py
         │   │   ├── communication/
         │   │   │   ├── __init__.py
         │   │   │   └── serial_message.py
         │   │   ├── dsl/
         │   │   │   ├── ast/
         │   │   │   │   ├── imecha_instruction.py
         │   │   │   │   ├── imecha_program.py
         │   │   │   │   ├── __init__.py
         │   │   │   │   ├── mecha_command_type.py
         │   │   │   │   ├── mecha_instruction.py
         │   │   │   │   └── mecha_program.py
         │   │   │   ├── diagnostic/
         │   │   │   │   ├── imecha_diagnostic.py
         │   │   │   │   ├── __init__.py
         │   │   │   │   ├── mecha_diagnostic.py
         │   │   │   │   └── mecha_diagnostic_severity.py
         │   │   │   ├── __init__.py
         │   │   │   └── token/
         │   │   │       ├── __init__.py
         │   │   │       ├── mecha_token.py
         │   │   │       └── mecha_token_type.py
         │   │   ├── __init__.py
         │   │   ├── kinematics/
         │   │   │   ├── __init__.py
         │   │   │   ├── joint_config.py
         │   │   │   ├── joint_id.py
         │   │   │   └── joint_state.py
         │   │   └── preset/
         │   │       ├── __init__.py
         │   │       └── motion_preset.py
         │   └── service/
         │       ├── arm/
         │       │   ├── arm_command_formatter.py
         │       │   ├── arm_controller_service.py
         │       │   ├── arm_telemetry_parser.py
         │       │   ├── iarm_controller_service.py
         │       │   └── __init__.py
         │       ├── dsl/
         │       │   ├── compiler/
         │       │   │   ├── imecha_compiler.py
         │       │   │   ├── __init__.py
         │       │   │   └── mecha_compiler.py
         │       │   ├── imecha_dsl_service.py
         │       │   ├── __init__.py
         │       │   ├── lexer/
         │       │   │   ├── imecha_lexer.py
         │       │   │   ├── __init__.py
         │       │   │   └── mecha_lexer.py
         │       │   ├── linter/
         │       │   │   ├── imecha_linter.py
         │       │   │   ├── __init__.py
         │       │   │   ├── mecha_kinematic_bounds_checker.py
         │       │   │   └── mecha_linter.py
         │       │   ├── mecha_dsl_service.py
         │       │   └── parser/
         │       │       ├── imecha_parser.py
         │       │       ├── __init__.py
         │       │       ├── mecha_command_parser.py
         │       │       └── mecha_parser.py
         │       ├── engine.py
         │       ├── firmware/
         │       │   ├── firmware_command_parser.py
         │       │   ├── firmware_simulator.py
         │       │   ├── __init__.py
         │       │   ├── ivirtual_arm_firmware.py
         │       │   └── virtual_arm_firmware.py
         │       ├── __init__.py
         │       ├── iservice.py
         │       ├── serial/
         │       │   ├── __init__.py
         │       │   ├── iserial_service.py
         │       │   ├── serial_listener_hub.py
         │       │   ├── serial_rx_worker.py
         │       │   └── serial_service.py
         │       ├── storage/
         │       │   ├── iarm_storage_service.py
         │       │   └── __init__.py
         │       └── transport/
         │           ├── __init__.py
         │           └── itransport.py
         ├── engine.py
         ├── infrastructure/
         │   ├── cli/
         │   │   ├── engine.py
         │   │   ├── icli.py
         │   │   ├── __init__.py
         │   │   └── setup/
         │   │       ├── bundle.py
         │   │       ├── dep_validator.py
         │   │       ├── dependencies.py
         │   │       ├── factory.py
         │   │       ├── __init__.py
         │   │       ├── keys.py
         │   │       ├── opt_validator.py
         │   │       ├── options.py
         │   │       ├── registry.py
         │   │       └── validator.py
         │   ├── command/
         │   │   ├── command.py
         │   │   ├── icommand_definition.py
         │   │   ├── icommand_executor.py
         │   │   ├── __init__.py
         │   │   ├── studio_command_definition.py
         │   │   └── studio_command_executor.py
         │   ├── communication/
         │   │   ├── __init__.py
         │   │   ├── iserial_port_scanner.py
         │   │   ├── iserial_preferences.py
         │   │   ├── itransport.py
         │   │   ├── serial_port_scanner.py
         │   │   ├── serial_preferences.py
         │   │   ├── serial_transport.py
         │   │   └── virtual_serial_transport.py
         │   ├── config/
         │   │   ├── mecharmory.cfg
         │   │   ├── mecharmory.logo
         │   │   ├── mecharmory_config.json
         │   │   └── scheme.json
         │   ├── gui/
         │   │   ├── arm/
         │   │   │   ├── arm_control_header.py
         │   │   │   ├── arm_control_panel.py
         │   │   │   ├── arm_joint_list.py
         │   │   │   ├── arm_panel_style.py
         │   │   │   └── __init__.py
         │   │   ├── canvas/
         │   │   │   ├── arm_background_painter.py
         │   │   │   ├── arm_canvas_painter.py
         │   │   │   ├── arm_canvas_preview.py
         │   │   │   ├── arm_canvas_style.py
         │   │   │   ├── arm_hud_painter.py
         │   │   │   ├── arm_kinematics_2d.py
         │   │   │   ├── arm_linkage_painter.py
         │   │   │   ├── arm_pedestal_painter.py
         │   │   │   ├── arm_pose_2d.py
         │   │   │   ├── arm_tool_painter.py
         │   │   │   ├── arm_tube_painter.py
         │   │   │   └── __init__.py
         │   │   ├── console/
         │   │   │   ├── console_command_entry.py
         │   │   │   ├── console_header_toolbar.py
         │   │   │   ├── console_log_viewer.py
         │   │   │   ├── console_panel.py
         │   │   │   ├── console_panel_style.py
         │   │   │   └── __init__.py
         │   │   ├── dsl/
         │   │   │   ├── imecha_editor_tab.py
         │   │   │   ├── __init__.py
         │   │   │   ├── mecha_code_editor.py
         │   │   │   ├── mecha_console_view.py
         │   │   │   ├── mecha_document_manager.py
         │   │   │   ├── mecha_editor_tab.py
         │   │   │   ├── mecha_editor_toolbar.py
         │   │   │   ├── mecha_example_catalog.py
         │   │   │   ├── mecha_stream_runner.py
         │   │   │   └── mecha_syntax_highlighter.py
         │   │   ├── gui_event_mediator.py
         │   │   ├── gui_window.py
         │   │   ├── gui_window_style.py
         │   │   ├── igui_window.py
         │   │   ├── __init__.py
         │   │   ├── joint/
         │   │   │   ├── __init__.py
         │   │   │   ├── joint_control_widget.py
         │   │   │   ├── joint_entry_control.py
         │   │   │   ├── joint_step_buttons.py
         │   │   │   └── joint_widget_style.py
         │   │   ├── preset/
         │   │   │   ├── __init__.py
         │   │   │   ├── preset_panel.py
         │   │   │   └── preset_panel_style.py
         │   │   ├── serial/
         │   │   │   ├── __init__.py
         │   │   │   ├── serial_bar.py
         │   │   │   ├── serial_panel_style.py
         │   │   │   ├── serial_port_selector.py
         │   │   │   └── serial_status_badge.py
         │   │   ├── theme/
         │   │   │   ├── __init__.py
         │   │   │   └── theme_manager.py
         │   │   └── workspace/
         │   │       ├── arm_workspace.py
         │   │       └── __init__.py
         │   ├── __init__.py
         │   └── storage/
         │       ├── arm_storage_service.py
         │       └── __init__.py
         ├── __init__.py
         └── setup/
             ├── bundle.py
             ├── config_resolver.py
             ├── dep_validator.py
             ├── dependencies.py
             ├── factory.py
             ├── __init__.py
             ├── keys.py
             ├── model_resolver.py
             ├── opt_validator.py
             ├── options.py
             ├── registry.py
             └── validator.py

     40 directories, 171 files
```
</details>

#### 🏗 Architecture & SOLID Principles

**mecharmory** is built on a strictly decoupled, **Layered Clean Architecture** where presentation, domain logic, and hardware communication are segregated through pure Python protocols:

##### SOLID Principles Compliance

* **S — Single Responsibility Principle (SRP)**:
  * Each class or interface is housed in its own dedicated module.
  * Controller, telemetry parsing, and command formatting logic is decomposed into dedicated handlers rather than a monolithic service.
  * Enforced by automated gate: strict limit of $\le 15$ methods per class across the entire codebase.
* **O — Open/Closed Principle (OCP)**:
  * Transport layers and firmware emulators can be added without altering existing services.
* **L — Liskov Substitution Principle (LSP)**:
  * Pure structural subtyping via Python `@runtime_checkable Protocol` definitions. `VirtualSerialTransport` seamlessly substitutes `SerialTransport`.
* **I — Interface Segregation Principle (ISP)**:
  * Protocols specify strictly minimal, client-focused contracts (`IArmControllerService`, `ISerialService`, `ITransport`).
* **D — Dependency Inversion Principle (DIP)**:
  * Concrete implementations do not inherit from protocols; duck-typing / PEP 544 structural subtyping decouples layers completely.

##### Automated Quality Gates (`run_quality_gates.sh`)

Every build is validated against 4 strict automated quality gates:
1. **Structural Protocols Gate**: Verifies 100% compliance with `@runtime_checkable Protocol` structural typing.
2. **Interface Segregation Gate (ISP)**: Verifies that no bloated or unused interfaces exist.
3. **Module Limits Gate**: Enforces file length and line length limits ($\le 100$ characters).
4. **Single Responsibility Gate (SRP)**: Strictly enforces $\le 15$ methods per class.

### ✨ Features

1. **Catppuccin Mocha Dark UI**: Modern, ergonomic design with high contrast, vibrant accents, and smooth controls.
2. **2D Real-Time Kinematic Visualizer**: Graphical rendering of base rotation, shoulder dual-lift tandem linkage, elbow tube roll, tool pitch, and tool end flange.
3. **Virtual Firmware Mode**: Built-in 50 Hz RP2040 emulator allows complete testing and posture planning without physical hardware connected.
4. **Physical RP2040 Serial Streaming**: Direct connection to Raspberry Pi Pico C firmware over USB CDC serial (`/dev/ttyACM*`).
5. **Interactive Console**: Live bidirectional monitor with color-coded TX/RX logs and raw ASCII command prompt.
6. **Mecha Domain-Specific Language (`.mecha`)**: Declarative scripting language for automated robotic trajectories, variable definitions (`VAR`), Cartesian/joint 6-DOF points (`POINT`), kinematic motion primitives (`MOVE_P`, `MOVE_J`, `MOVE_REL`, `PRESET`), timing (`WAIT_MS`, `SYNC`), velocity profiling (`SPEED`, `SPEED_JOINT`, `OVERRIDE`), and tool actuation (`GRIPPER`, `TOOL_ROLL`, `HOME`, `STOP`).
7. **Integrated Script Editor Tab (`MechaEditorTab`)**: Full-featured IDE tab within `ttk.Notebook` with syntax highlighting (Catppuccin Mocha theme), line numbers, file open/save, live execution console, and preloaded example catalog.
8. **Real-Time Static Kinematic Linter**: Static code analysis and kinematic bounds checking that inspects every instruction for joint angle limit violations (`J0`–`J5`), undefined variables, argument type mismatches, and syntax errors with clear diagnostic severity (ERROR, WARNING, INFO).
9. **Asynchronous Command Streaming Runner**: Multi-threaded execution engine that compiles AST instructions to serial protocol commands and streams them sequentially to hardware or simulator without blocking the GUI.

### 📝 Mecha Domain-Specific Language (.mecha)

**mecharmory** features **Mecha**, a dedicated domain-specific language designed for robotic manipulation, automated pick-and-place routines, calibration routines, and continuous trajectory execution. Mecha scripts are saved with the `.mecha` extension and can be authored, linted, compiled, and executed directly within the integrated **Mecha Script Editor** tab.

#### Language Primitives & Syntax

* **Variables (`VAR`)**: Declare numerical values for velocities, angles, and wait intervals.
  ```mecha
  VAR approach_speed = 45.0
  VAR place_delay = 500
  ```
* **Points (`POINT`)**: Define 6-DOF joint postures (`J0` Base, `J1` Shoulder Left, `J2` Shoulder Right, `J3` Elbow Roll, `J4` Pitch Tilt, `J5` Tool Flange).
  ```mecha
  POINT pick_pos = 45.0, 40.0, 40.0, 90.0, 70.0, 90.0
  ```
* **Coordinated Motion (`MOVE_P`)**: Move all 6 joints simultaneously to a named point.
  ```mecha
  MOVE_P pick_pos
  ```
* **Single Joint & Relative Moves (`MOVE_J`, `MOVE_REL`)**: Target an individual joint by ID or apply relative angle increments.
  ```mecha
  MOVE_J 0 90.0
  MOVE_REL 4 -15.0
  ```
* **Presets (`PRESET`)**: Navigate instantly to predefined arm postures (`home`, `park`, `inspect`, `ready`, etc.).
  ```mecha
  PRESET inspect
  ```
* **Speed & Trajectory Profiling (`SPEED`, `SPEED_JOINT`, `OVERRIDE`)**: Configure global velocity, per-joint velocity limits, and global override scaling factor ($0.05 \le f \le 1.0$).
  ```mecha
  SPEED 50.0
  SPEED_JOINT 0 30.0
  OVERRIDE 0.8
  ```
* **Tool & Gripper Actuation (`GRIPPER`, `TOOL_ROLL`)**: Control end-effector aperture and wrist orientation.
  ```mecha
  GRIPPER 85.0
  TOOL_ROLL 90.0
  ```
* **Execution Flow & Synchronization (`WAIT_MS`, `SYNC`, `HOME`, `STOP`)**: Introduce millisecond dwell times, synchronize with physical motion completion, return to home, or trigger an emergency stop.
  ```mecha
  WAIT_MS 1000
  SYNC
  HOME
  ```

#### Mecha DSL Command Reference

| Command | Arguments | Description | Example |
| :--- | :--- | :--- | :--- |
| `VAR` | `<name> = <val>` | Declare a numerical variable | `VAR speed = 40.0` |
| `POINT` | `<name> = <j0>, <j1>, <j2>, <j3>, <j4>, <j5>` | Define a 6-DOF joint target posture | `POINT pick = 90, 45, 45, 90, 80, 90` |
| `MOVE_P` | `<point_name>` | Coordinated 6-DOF simultaneous move | `MOVE_P pick` |
| `MOVE_J` | `<joint_id> <angle>` | Move single joint (0–5) to target angle | `MOVE_J 0 45.0` |
| `MOVE_REL` | `<joint_id> <delta>` | Relative angle adjustment for single joint | `MOVE_REL 4 -10.0` |
| `PRESET` | `<preset_name>` | Move to built-in posture preset | `PRESET inspect` |
| `SPEED` | `<deg_per_sec>` | Set global default joint motion speed | `SPEED 60.0` |
| `SPEED_JOINT` | `<joint_id> <deg_per_sec>` | Set joint-specific velocity limit | `SPEED_JOINT 1 45.0` |
| `OVERRIDE` | `<factor>` | Global speed scaling factor (0.05 – 1.0) | `OVERRIDE 0.75` |
| `GRIPPER` | `<angle_or_val>` | Command end-effector gripper aperture | `GRIPPER 80.0` |
| `TOOL_ROLL` | `<angle>` | Set wrist / tool roll orientation (J5) | `TOOL_ROLL 90.0` |
| `WAIT_MS` | `<millis>` | Dwell/pause execution for specified milliseconds | `WAIT_MS 500` |
| `SYNC` | None | Synchronize and wait for physical motion completion | `SYNC` |
| `HOME` | None | Move all joints to factory neutral / home position (90°) | `HOME` |
| `STOP` | None | Immediate emergency stop for all joints | `STOP` |

#### Example: Automated Pick & Place Sequence (`pick_and_place.mecha`)

```mecha
# Pick-and-Place Demonstration Routine
VAR approach_speed = 45.0
VAR place_speed = 30.0

POINT pick_approach = 45.0, 60.0, 60.0, 90.0, 80.0, 90.0
POINT pick_pos      = 45.0, 40.0, 40.0, 90.0, 70.0, 90.0
POINT drop_approach = 135.0, 60.0, 60.0, 90.0, 80.0, 90.0
POINT drop_pos      = 135.0, 40.0, 40.0, 90.0, 70.0, 90.0

HOME
SPEED approach_speed
MOVE_P pick_approach
SYNC

SPEED place_speed
MOVE_P pick_pos
SYNC
GRIPPER 85.0
WAIT_MS 500

MOVE_P pick_approach
SYNC

SPEED approach_speed
MOVE_P drop_approach
SYNC

SPEED place_speed
MOVE_P drop_pos
SYNC
GRIPPER 30.0
WAIT_MS 500

MOVE_P drop_approach
SYNC
HOME
```

#### Integrated Mecha Script Editor Tab

The GUI provides a dedicated tab `[ 📝 Mecha Script Editor ]` alongside `[ 🎮 Manual Workspace ]`:
* **Syntax Highlighter**: Real-time token coloring matching the Catppuccin Mocha theme (commands in mauve `#cba6f7`, points/variables in blue `#89b4fa`, numbers in peach `#fab387`, comments in overlay `#6c7086`).
* **Interactive Example Catalog**: Instant loading of pre-bundled routines (*Pick and Place*, *Scan Workspace*, *Joint Calibration*, *Preset Tour*).
* **Kinematic Bounds Linter**: Displays real-time warnings and errors if any commanded angle exceeds physical limits ($J0 \in [0, 180]$, $J1, J2 \in [15, 165]$, $J3 \in [0, 180]$, $J4 \in [15, 165]$, $J5 \in [0, 180]$).
* **Asynchronous Streaming Runner**: One-click compilation and sequential execution over physical USB CDC or virtual simulator without freezing the UI.


### 📐 Kinematic & Joint Configuration

| Joint ID | Channel | Name | Safe Angle Range | Neutral (Home) | Pulse Width (µs) | Role in Mechanism |
| :---: | :---: | :--- | :---: | :---: | :---: | :--- |
| **J0** | Ch 0 | `Base Rotation` | 0° – 180° | 90° | 500 – 2500 µs | Base turntable yaw rotation |
| **J1** | Ch 1 | `Shoulder Lift Left` | 15° – 165° | 90° | 600 – 2400 µs | Shoulder lift (Left servo, tandem drive) |
| **J2** | Ch 2 | `Shoulder Lift Right`| 15° – 165° | 90° | 600 – 2400 µs | Shoulder lift (Right servo, symmetrical tandem) |
| **J3** | Ch 3 | `Elbow Roll` | 0° – 180° | 90° | 500 – 2500 µs | Elbow aluminum tube axial roll |
| **J4** | Ch 4 | `End-effector Tilt` | 15° – 165° | 90° | 500 – 2500 µs | End-effector wrist pitch tilt |
| **J5** | Ch 5 | `Tool End Rotation` | 0° – 180° | 90° | 500 – 2500 µs | Tool flange / steering wheel rotation |

### 📡 Unified Serial ASCII Communication Protocol

| Command | Arguments | Description | Example |
| :--- | :--- | :--- | :--- |
| `SET` | `<joint_id> <angle>` | Move specific joint with default speed | `SET 0 90.00` |
| `SETP` | `<j0> <j1> <j2> <j3> <j4> <j5>` | Move all joints simultaneously | `SETP 90 90 90 90 90 90` |
| `SPEED` | `<joint_id> <deg_per_sec>` | Set maximum joint movement velocity | `SPEED 1 45.0` |
| `HOME` | None | Return all joints to home position (90°) | `HOME` |
| `STOP` | None | Immediate emergency stop for all joints | `STOP` |
| `STATUS` | None | Query current joint angles | `STATUS` |
| `PING` | None | Heartbeat ping | `PING` $\to$ `PONG` |

### 📊 Code coverage

<details>
<summary><b>Click to expand code coverage</b></summary>

| Name | Stmts | Miss | Cover |
|------|-------|------|-------|
| `mecharmory/__init__.py` | 9 | 0 | 100%|
| `mecharmory/core/__init__.py` | 9 | 0 | 100%|
| `mecharmory/core/model/__init__.py` | 9 | 0 | 100%|
| `mecharmory/core/model/arm/__init__.py` | 9 | 0 | 100%|
| `mecharmory/core/model/arm/arm_config_defaults.py` | 15 | 0 | 100%|
| `mecharmory/core/model/arm/arm_model.py` | 45 | 0 | 100%|
| `mecharmory/core/model/arm/arm_preset_defaults.py` | 32 | 0 | 100%|
| `mecharmory/core/model/arm/iarm_model.py` | 23 | 0 | 100%|
| `mecharmory/core/model/communication/__init__.py` | 9 | 0 | 100%|
| `mecharmory/core/model/communication/serial_message.py` | 24 | 0 | 100%|
| `mecharmory/core/model/dsl/__init__.py` | 9 | 0 | 100%|
| `mecharmory/core/model/dsl/ast/__init__.py` | 9 | 0 | 100%|
| `mecharmory/core/model/dsl/ast/imecha_instruction.py` | 22 | 0 | 100%|
| `mecharmory/core/model/dsl/ast/imecha_program.py` | 23 | 0 | 100%|
| `mecharmory/core/model/dsl/ast/mecha_command_type.py` | 29 | 0 | 100%|
| `mecharmory/core/model/dsl/ast/mecha_instruction.py` | 34 | 2 | 94%|
| `mecharmory/core/model/dsl/ast/mecha_program.py` | 36 | 0 | 100%|
| `mecharmory/core/model/dsl/diagnostic/__init__.py` | 9 | 0 | 100%|
| `mecharmory/core/model/dsl/diagnostic/imecha_diagnostic.py` | 24 | 0 | 100%|
| `mecharmory/core/model/dsl/diagnostic/mecha_diagnostic.py` | 39 | 3 | 92%|
| `mecharmory/core/model/dsl/diagnostic/mecha_diagnostic_severity.py` | 15 | 0 | 100%|
| `mecharmory/core/model/dsl/token/__init__.py` | 9 | 0 | 100%|
| `mecharmory/core/model/dsl/token/mecha_token.py` | 17 | 0 | 100%|
| `mecharmory/core/model/dsl/token/mecha_token_type.py` | 21 | 0 | 100%|
| `mecharmory/core/model/kinematics/__init__.py` | 9 | 0 | 100%|
| `mecharmory/core/model/kinematics/joint_config.py` | 22 | 0 | 100%|
| `mecharmory/core/model/kinematics/joint_id.py` | 17 | 0 | 100%|
| `mecharmory/core/model/kinematics/joint_state.py` | 18 | 0 | 100%|
| `mecharmory/core/model/preset/__init__.py` | 9 | 0 | 100%|
| `mecharmory/core/model/preset/motion_preset.py` | 15 | 0 | 100%|
| `mecharmory/core/service/__init__.py` | 9 | 0 | 100%|
| `mecharmory/core/service/arm/__init__.py` | 9 | 0 | 100%|
| `mecharmory/core/service/arm/arm_command_formatter.py` | 29 | 1 | 97%|
| `mecharmory/core/service/arm/arm_controller_service.py` | 75 | 2 | 97%|
| `mecharmory/core/service/arm/arm_telemetry_parser.py` | 35 | 3 | 91%|
| `mecharmory/core/service/arm/iarm_controller_service.py` | 24 | 0 | 100%|
| `mecharmory/core/service/dsl/__init__.py` | 9 | 0 | 100%|
| `mecharmory/core/service/dsl/compiler/__init__.py` | 9 | 0 | 100%|
| `mecharmory/core/service/dsl/compiler/imecha_compiler.py` | 14 | 14 | 0%|
| `mecharmory/core/service/dsl/compiler/mecha_compiler.py` | 138 | 49 | 64%|
| `mecharmory/core/service/dsl/imecha_dsl_service.py` | 21 | 0 | 100%|
| `mecharmory/core/service/dsl/lexer/__init__.py` | 9 | 0 | 100%|
| `mecharmory/core/service/dsl/lexer/imecha_lexer.py` | 14 | 14 | 0%|
| `mecharmory/core/service/dsl/lexer/mecha_lexer.py` | 53 | 3 | 94%|
| `mecharmory/core/service/dsl/linter/__init__.py` | 9 | 0 | 100%|
| `mecharmory/core/service/dsl/linter/imecha_linter.py` | 16 | 16 | 0%|
| `mecharmory/core/service/dsl/linter/mecha_kinematic_bounds_checker.py` | 33 | 1 | 97%|
| `mecharmory/core/service/dsl/linter/mecha_linter.py` | 119 | 31 | 74%|
| `mecharmory/core/service/dsl/mecha_dsl_service.py` | 49 | 0 | 100%|
| `mecharmory/core/service/dsl/parser/__init__.py` | 9 | 0 | 100%|
| `mecharmory/core/service/dsl/parser/imecha_parser.py` | 15 | 15 | 0%|
| `mecharmory/core/service/dsl/parser/mecha_command_parser.py` | 71 | 3 | 96%|
| `mecharmory/core/service/dsl/parser/mecha_parser.py` | 69 | 8 | 88%|
| `mecharmory/core/service/engine.py` | 33 | 1 | 97%|
| `mecharmory/core/service/firmware/__init__.py` | 9 | 0 | 100%|
| `mecharmory/core/service/firmware/firmware_command_parser.py` | 89 | 15 | 83%|
| `mecharmory/core/service/firmware/firmware_simulator.py` | 83 | 7 | 92%|
| `mecharmory/core/service/firmware/ivirtual_arm_firmware.py` | 16 | 16 | 0%|
| `mecharmory/core/service/firmware/virtual_arm_firmware.py` | 25 | 0 | 100%|
| `mecharmory/core/service/iservice.py` | 21 | 0 | 100%|
| `mecharmory/core/service/serial/__init__.py` | 9 | 0 | 100%|
| `mecharmory/core/service/serial/iserial_service.py` | 21 | 0 | 100%|
| `mecharmory/core/service/serial/serial_listener_hub.py` | 30 | 6 | 80%|
| `mecharmory/core/service/serial/serial_rx_worker.py` | 38 | 3 | 92%|
| `mecharmory/core/service/serial/serial_service.py` | 67 | 4 | 94%|
| `mecharmory/core/service/storage/__init__.py` | 9 | 0 | 100%|
| `mecharmory/core/service/storage/iarm_storage_service.py` | 17 | 0 | 100%|
| `mecharmory/core/service/transport/__init__.py` | 9 | 0 | 100%|
| `mecharmory/core/service/transport/itransport.py` | 17 | 0 | 100%|
| `mecharmory/engine.py` | 64 | 64 | 0%|
| `mecharmory/infrastructure/__init__.py` | 9 | 0 | 100%|
| `mecharmory/infrastructure/cli/__init__.py` | 9 | 0 | 100%|
| `mecharmory/infrastructure/cli/engine.py` | 41 | 9 | 78%|
| `mecharmory/infrastructure/cli/icli.py` | 15 | 0 | 100%|
| `mecharmory/infrastructure/cli/setup/__init__.py` | 9 | 0 | 100%|
| `mecharmory/infrastructure/cli/setup/bundle.py` | 22 | 1 | 95%|
| `mecharmory/infrastructure/cli/setup/dep_validator.py` | 36 | 5 | 86%|
| `mecharmory/infrastructure/cli/setup/dependencies.py` | 18 | 0 | 100%|
| `mecharmory/infrastructure/cli/setup/factory.py` | 37 | 0 | 100%|
| `mecharmory/infrastructure/cli/setup/keys.py` | 28 | 0 | 100%|
| `mecharmory/infrastructure/cli/setup/opt_validator.py` | 36 | 5 | 86%|
| `mecharmory/infrastructure/cli/setup/options.py` | 17 | 0 | 100%|
| `mecharmory/infrastructure/cli/setup/registry.py` | 24 | 0 | 100%|
| `mecharmory/infrastructure/cli/setup/validator.py` | 43 | 5 | 88%|
| `mecharmory/infrastructure/command/__init__.py` | 9 | 0 | 100%|
| `mecharmory/infrastructure/command/command.py` | 16 | 0 | 100%|
| `mecharmory/infrastructure/command/icommand_definition.py` | 14 | 0 | 100%|
| `mecharmory/infrastructure/command/icommand_executor.py` | 14 | 0 | 100%|
| `mecharmory/infrastructure/command/studio_command_definition.py` | 24 | 1 | 96%|
| `mecharmory/infrastructure/command/studio_command_executor.py` | 49 | 26 | 47%|
| `mecharmory/infrastructure/communication/__init__.py` | 9 | 0 | 100%|
| `mecharmory/infrastructure/communication/iserial_port_scanner.py` | 14 | 0 | 100%|
| `mecharmory/infrastructure/communication/iserial_preferences.py` | 14 | 0 | 100%|
| `mecharmory/infrastructure/communication/itransport.py` | 17 | 17 | 0%|
| `mecharmory/infrastructure/communication/serial_port_scanner.py` | 35 | 1 | 97%|
| `mecharmory/infrastructure/communication/serial_preferences.py` | 51 | 3 | 94%|
| `mecharmory/infrastructure/communication/serial_transport.py` | 60 | 36 | 40%|
| `mecharmory/infrastructure/communication/virtual_serial_transport.py` | 67 | 2 | 97%|
| `mecharmory/infrastructure/gui/__init__.py` | 9 | 0 | 100%|
| `mecharmory/infrastructure/gui/arm/__init__.py` | 9 | 0 | 100%|
| `mecharmory/infrastructure/gui/arm/arm_control_header.py` | 36 | 0 | 100%|
| `mecharmory/infrastructure/gui/arm/arm_control_panel.py` | 30 | 0 | 100%|
| `mecharmory/infrastructure/gui/arm/arm_joint_list.py` | 41 | 1 | 98%|
| `mecharmory/infrastructure/gui/arm/arm_panel_style.py` | 34 | 0 | 100%|
| `mecharmory/infrastructure/gui/canvas/__init__.py` | 9 | 0 | 100%|
| `mecharmory/infrastructure/gui/canvas/arm_background_painter.py` | 17 | 0 | 100%|
| `mecharmory/infrastructure/gui/canvas/arm_canvas_painter.py` | 48 | 0 | 100%|
| `mecharmory/infrastructure/gui/canvas/arm_canvas_preview.py` | 46 | 0 | 100%|
| `mecharmory/infrastructure/gui/canvas/arm_canvas_style.py` | 54 | 0 | 100%|
| `mecharmory/infrastructure/gui/canvas/arm_hud_painter.py` | 17 | 0 | 100%|
| `mecharmory/infrastructure/gui/canvas/arm_kinematics_2d.py` | 41 | 0 | 100%|
| `mecharmory/infrastructure/gui/canvas/arm_linkage_painter.py` | 22 | 0 | 100%|
| `mecharmory/infrastructure/gui/canvas/arm_pedestal_painter.py` | 22 | 0 | 100%|
| `mecharmory/infrastructure/gui/canvas/arm_pose_2d.py` | 24 | 0 | 100%|
| `mecharmory/infrastructure/gui/canvas/arm_tool_painter.py` | 30 | 0 | 100%|
| `mecharmory/infrastructure/gui/canvas/arm_tube_painter.py` | 27 | 0 | 100%|
| `mecharmory/infrastructure/gui/console/__init__.py` | 9 | 0 | 100%|
| `mecharmory/infrastructure/gui/console/console_command_entry.py` | 41 | 6 | 85%|
| `mecharmory/infrastructure/gui/console/console_header_toolbar.py` | 36 | 0 | 100%|
| `mecharmory/infrastructure/gui/console/console_log_viewer.py` | 70 | 25 | 64%|
| `mecharmory/infrastructure/gui/console/console_panel.py` | 39 | 4 | 90%|
| `mecharmory/infrastructure/gui/console/console_panel_style.py` | 51 | 0 | 100%|
| `mecharmory/infrastructure/gui/dsl/__init__.py` | 9 | 0 | 100%|
| `mecharmory/infrastructure/gui/dsl/imecha_editor_tab.py` | 18 | 18 | 0%|
| `mecharmory/infrastructure/gui/dsl/mecha_code_editor.py` | 36 | 3 | 92%|
| `mecharmory/infrastructure/gui/dsl/mecha_console_view.py` | 38 | 3 | 92%|
| `mecharmory/infrastructure/gui/dsl/mecha_document_manager.py` | 47 | 28 | 40%|
| `mecharmory/infrastructure/gui/dsl/mecha_editor_tab.py` | 97 | 28 | 71%|
| `mecharmory/infrastructure/gui/dsl/mecha_editor_toolbar.py` | 40 | 5 | 88%|
| `mecharmory/infrastructure/gui/dsl/mecha_example_catalog.py` | 18 | 0 | 100%|
| `mecharmory/infrastructure/gui/dsl/mecha_stream_runner.py` | 43 | 21 | 51%|
| `mecharmory/infrastructure/gui/dsl/mecha_syntax_highlighter.py` | 54 | 0 | 100%|
| `mecharmory/infrastructure/gui/gui_event_mediator.py` | 70 | 0 | 100%|
| `mecharmory/infrastructure/gui/gui_window.py` | 100 | 17 | 83%|
| `mecharmory/infrastructure/gui/gui_window_style.py` | 22 | 0 | 100%|
| `mecharmory/infrastructure/gui/igui_window.py` | 16 | 0 | 100%|
| `mecharmory/infrastructure/gui/joint/__init__.py` | 9 | 0 | 100%|
| `mecharmory/infrastructure/gui/joint/joint_control_widget.py` | 80 | 22 | 72%|
| `mecharmory/infrastructure/gui/joint/joint_entry_control.py` | 40 | 6 | 85%|
| `mecharmory/infrastructure/gui/joint/joint_step_buttons.py` | 29 | 0 | 100%|
| `mecharmory/infrastructure/gui/joint/joint_widget_style.py` | 45 | 0 | 100%|
| `mecharmory/infrastructure/gui/preset/__init__.py` | 9 | 0 | 100%|
| `mecharmory/infrastructure/gui/preset/preset_panel.py` | 28 | 0 | 100%|
| `mecharmory/infrastructure/gui/preset/preset_panel_style.py` | 22 | 0 | 100%|
| `mecharmory/infrastructure/gui/serial/__init__.py` | 9 | 0 | 100%|
| `mecharmory/infrastructure/gui/serial/serial_bar.py` | 61 | 9 | 85%|
| `mecharmory/infrastructure/gui/serial/serial_panel_style.py` | 51 | 0 | 100%|
| `mecharmory/infrastructure/gui/serial/serial_port_selector.py` | 60 | 8 | 87%|
| `mecharmory/infrastructure/gui/serial/serial_status_badge.py` | 32 | 5 | 84%|
| `mecharmory/infrastructure/gui/theme/__init__.py` | 9 | 0 | 100%|
| `mecharmory/infrastructure/gui/theme/theme_manager.py` | 29 | 0 | 100%|
| `mecharmory/infrastructure/gui/workspace/__init__.py` | 9 | 0 | 100%|
| `mecharmory/infrastructure/gui/workspace/arm_workspace.py` | 45 | 0 | 100%|
| `mecharmory/infrastructure/storage/__init__.py` | 9 | 0 | 100%|
| `mecharmory/infrastructure/storage/arm_storage_service.py` | 49 | 1 | 98%|
| `mecharmory/setup/__init__.py` | 9 | 0 | 100%|
| `mecharmory/setup/bundle.py` | 23 | 0 | 100%|
| `mecharmory/setup/config_resolver.py` | 35 | 2 | 94%|
| `mecharmory/setup/dep_validator.py` | 36 | 5 | 86%|
| `mecharmory/setup/dependencies.py` | 19 | 0 | 100%|
| `mecharmory/setup/factory.py` | 60 | 1 | 98%|
| `mecharmory/setup/keys.py` | 35 | 0 | 100%|
| `mecharmory/setup/model_resolver.py` | 29 | 1 | 97%|
| `mecharmory/setup/opt_validator.py` | 36 | 16 | 56%|
| `mecharmory/setup/options.py` | 20 | 0 | 100%|
| `mecharmory/setup/registry.py` | 24 | 0 | 100%|
| `mecharmory/setup/validator.py` | 48 | 5 | 90%|
| **Total** | 5071 | 632 | 88% |

</details>

### 🛠 Usage

To start the motion studio:
```bash
./run.sh
```
Or when installed:
```bash
mecharmory
```

### 📚 Docs

Sphinx documentation is hosted on Read the Docs:
* [https://mecharmory.readthedocs.io/en/latest/](https://mecharmory.readthedocs.io/en/latest/)

To build documentation locally:
```bash
cd docs
make clean && make html
```

### 👥 Contributing

Please see [CONTRIBUTING.md](CONTRIBUTING.md) and [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md).

### 📄 Copyright and licence

Copyright (C) 2026 by [vroncevic.github.io/mecharmory](https://vroncevic.github.io/mecharmory)

**mecharmory** is free software; you can redistribute it and/or modify
it under the same terms as Python itself, either Python version 3.x or,
at your option, any later version of Python 3 you may have available.
