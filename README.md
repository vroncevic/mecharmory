# Mecharmory - 6-DOF Robotic Arm Motion Studio & Hardware Streamer

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

     30 directories, 130 files
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
| `mecharmory/core/service/engine.py` | 28 | 0 | 100%|
| `mecharmory/core/service/firmware/__init__.py` | 9 | 0 | 100%|
| `mecharmory/core/service/firmware/firmware_command_parser.py` | 89 | 15 | 83%|
| `mecharmory/core/service/firmware/firmware_simulator.py` | 83 | 7 | 92%|
| `mecharmory/core/service/firmware/ivirtual_arm_firmware.py` | 16 | 16 | 0%|
| `mecharmory/core/service/firmware/virtual_arm_firmware.py` | 25 | 0 | 100%|
| `mecharmory/core/service/iservice.py` | 19 | 0 | 100%|
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
| `mecharmory/infrastructure/gui/gui_event_mediator.py` | 70 | 0 | 100%|
| `mecharmory/infrastructure/gui/gui_window.py` | 91 | 16 | 82%|
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
| `mecharmory/infrastructure/gui/serial/serial_port_selector.py` | 60 | 9 | 85%|
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
| **Total** | 3702 | 366 | 90% |

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
