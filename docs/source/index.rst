MECHARMORY - 6-DOF Robotic Arm Studio
-------------------------------------

**mecharmory** is a standalone desktop motion planning, kinematic validation, and real-time serial controller for 6-DOF robotic arm manipulators running Raspberry Pi Pico (RP2040) C SDK firmware and PCA9685 I2C 16-channel PWM drivers.

Developed in `python <https://www.python.org/>`_ code.

The README is used to introduce the tool and provide instructions on
how to install the tool, any machine dependencies it may have and any
other information that should be provided before the tool is installed.

|mecharmory python checker| |mecharmory package checker| |mecharmory interface checker| |mecharmory isp checker| |mecharmory srp checker| |gplv3 license| |python version| |github issues| |documentation status| |github contributors|

.. |mecharmory python checker| image:: https://github.com/vroncevic/mecharmory/actions/workflows/mecharmory_python_checker.yml/badge.svg
   :target: https://github.com/vroncevic/mecharmory/actions/workflows/mecharmory_python_checker.yml

.. |mecharmory package checker| image:: https://github.com/vroncevic/mecharmory/actions/workflows/mecharmory_package_checker.yml/badge.svg
   :target: https://github.com/vroncevic/mecharmory/actions/workflows/mecharmory_package_checker.yml

.. |mecharmory interface checker| image:: https://github.com/vroncevic/mecharmory/actions/workflows/mecharmory_interface_checker.yml/badge.svg
   :target: https://github.com/vroncevic/mecharmory/actions/workflows/mecharmory_interface_checker.yml

.. |mecharmory isp checker| image:: https://github.com/vroncevic/mecharmory/actions/workflows/mecharmory_isp_checker.yml/badge.svg
   :target: https://github.com/vroncevic/mecharmory/actions/workflows/mecharmory_isp_checker.yml

.. |mecharmory srp checker| image:: https://github.com/vroncevic/mecharmory/actions/workflows/mecharmory_srp_checker.yml/badge.svg
   :target: https://github.com/vroncevic/mecharmory/actions/workflows/mecharmory_srp_checker.yml

.. |gplv3 license| image:: https://img.shields.io/badge/License-GPLv3-blue.svg
   :target: https://www.gnu.org/licenses/gpl-3.0

.. |python version| image:: https://img.shields.io/badge/python-3.10+-blue.svg
   :target: https://www.python.org/downloads/

.. |github issues| image:: https://img.shields.io/github/issues/vroncevic/mecharmory.svg
   :target: https://github.com/vroncevic/mecharmory/issues

.. |github contributors| image:: https://img.shields.io/github/contributors/vroncevic/mecharmory.svg
   :target: https://github.com/vroncevic/mecharmory/graphs/contributors

.. |documentation status| image:: https://readthedocs.org/projects/mecharmory/badge/?version=latest
   :target: https://mecharmory.readthedocs.io/en/latest/?badge=latest

.. toctree::
   :maxdepth: 4
   :caption: Contents

   self
   modules

🚀 Installation
---------------

|mecharmory python3 build|

.. |mecharmory python3 build| image:: https://github.com/vroncevic/mecharmory/actions/workflows/mecharmory_python3_build.yml/badge.svg
   :target: https://github.com/vroncevic/mecharmory/actions/workflows/mecharmory_python3_build.yml

Navigate to release `page`_ download and extract release archive.

.. _page: https://github.com/vroncevic/mecharmory/releases

To install **mecharmory** type the following:

.. code-block:: bash

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

You can use Docker to create image/container, or you can use pip to install:

.. code-block:: bash

    # python3
    pip3 install mecharmory

📦 Dependencies
---------------

**mecharmory** requires next modules and libraries

* `ats-utilities - Python App/Tool/Script Utilities <https://pypi.org/project/ats-utilities/>`_ |ats gplv3| |ats apache|
* `pyserial - Python Serial Port Extension <https://pypi.org/project/pyserial/>`_ |pyserial bsd|

.. |ats gplv3| image:: https://img.shields.io/badge/License-GPLv3-blue.svg
   :target: https://www.gnu.org/licenses/gpl-3.0

.. |ats apache| image:: https://img.shields.io/badge/License-Apache%202.0-blue.svg
   :target: https://opensource.org/licenses/Apache-2.0

.. |pyserial bsd| image:: https://img.shields.io/badge/License-BSD_3--Clause-blue.svg
   :target: https://opensource.org/licenses/BSD-3-Clause

📁 Tool structure
-----------------

**mecharmory** is based on OOP and Clean Architecture.

Tool structure

.. code-block:: bash

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

✨ Features
-----------

* **Catppuccin Mocha Dark UI**: Modern, ergonomic design with high contrast, vibrant accents, and smooth controls.
* **2D Real-Time Kinematic Visualizer**: Graphical rendering of base rotation, shoulder dual-lift tandem linkage, elbow tube roll, tool pitch, and tool end flange.
* **Virtual Firmware Mode**: Built-in 50 Hz RP2040 emulator allows complete testing and posture planning without physical hardware connected.
* **Physical RP2040 Serial Streaming**: Direct connection to Raspberry Pi Pico C firmware over USB CDC serial (``/dev/ttyACM*``).
* **Interactive Console**: Live bidirectional monitor with color-coded TX/RX logs and raw ASCII command prompt.
* **Mecha Domain-Specific Language (``.mecha``)**: Declarative scripting language for automated robotic trajectories, variable definitions (``VAR``), Cartesian/joint 6-DOF points (``POINT``), kinematic motion primitives (``MOVE_P``, ``MOVE_J``, ``MOVE_REL``, ``PRESET``), timing (``WAIT_MS``, ``SYNC``), velocity profiling (``SPEED``, ``SPEED_JOINT``, ``OVERRIDE``), and tool actuation (``GRIPPER``, ``TOOL_ROLL``, ``HOME``, ``STOP``).
* **Integrated Script Editor Tab (``MechaEditorTab``)**: Full-featured IDE tab within ``ttk.Notebook`` with syntax highlighting (Catppuccin Mocha theme), line numbers, file open/save, live execution console, and preloaded example catalog.
* **Real-Time Static Kinematic Linter**: Static code analysis and kinematic bounds checking that inspects every instruction for joint angle limit violations (``J0``–``J5``), undefined variables, argument type mismatches, and syntax errors with clear diagnostic severity (ERROR, WARNING, INFO).
* **Asynchronous Command Streaming Runner**: Multi-threaded execution engine that compiles AST instructions to serial protocol commands and streams them sequentially to hardware or simulator without blocking the GUI.

📝 Mecha Domain-Specific Language (.mecha)
------------------------------------------

**mecharmory** features **Mecha**, a dedicated domain-specific language designed for robotic manipulation, automated pick-and-place routines, calibration routines, and continuous trajectory execution. Mecha scripts are saved with the ``.mecha`` extension and can be authored, linted, compiled, and executed directly within the integrated **Mecha Script Editor** tab.

Language Primitives & Syntax
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

* **Variables (``VAR``)**: Declare numerical values for velocities, angles, and wait intervals.

  .. code-block:: text

      VAR approach_speed = 45.0
      VAR place_delay = 500

* **Points (``POINT``)**: Define 6-DOF joint postures (``J0`` Base, ``J1`` Shoulder Left, ``J2`` Shoulder Right, ``J3`` Elbow Roll, ``J4`` Pitch Tilt, ``J5`` Tool Flange).

  .. code-block:: text

      POINT pick_pos = 45.0, 40.0, 40.0, 90.0, 70.0, 90.0

* **Coordinated Motion (``MOVE_P``)**: Move all 6 joints simultaneously to a named point.

  .. code-block:: text

      MOVE_P pick_pos

* **Single Joint & Relative Moves (``MOVE_J``, ``MOVE_REL``)**: Target an individual joint by ID or apply relative angle increments.

  .. code-block:: text

      MOVE_J 0 90.0
      MOVE_REL 4 -15.0

* **Presets (``PRESET``)**: Navigate instantly to predefined arm postures (``home``, ``park``, ``inspect``, ``ready``, etc.).

  .. code-block:: text

      PRESET inspect

* **Speed & Trajectory Profiling (``SPEED``, ``SPEED_JOINT``, ``OVERRIDE``)**: Configure global velocity, per-joint velocity limits, and global override scaling factor (0.05 – 1.0).

  .. code-block:: text

      SPEED 50.0
      SPEED_JOINT 0 30.0
      OVERRIDE 0.8

* **Tool & Gripper Actuation (``GRIPPER``, ``TOOL_ROLL``)**: Control end-effector aperture and wrist orientation.

  .. code-block:: text

      GRIPPER 85.0
      TOOL_ROLL 90.0

* **Execution Flow & Synchronization (``WAIT_MS``, ``SYNC``, ``HOME``, ``STOP``)**: Introduce millisecond dwell times, synchronize with physical motion completion, return to home, or trigger an emergency stop.

  .. code-block:: text

      WAIT_MS 1000
      SYNC
      HOME

Mecha DSL Command Reference
^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. list-table:: Mecha DSL Command Reference
   :widths: 15 35 30 20
   :header-rows: 1

   * - Command
     - Arguments
     - Description
     - Example
   * - ``VAR``
     - ``<name> = <val>``
     - Declare a numerical variable
     - ``VAR speed = 40.0``
   * - ``POINT``
     - ``<name> = <j0>, <j1>, <j2>, <j3>, <j4>, <j5>``
     - Define a 6-DOF joint target posture
     - ``POINT pick = 90, 45, 45, 90, 80, 90``
   * - ``MOVE_P``
     - ``<point_name>``
     - Coordinated 6-DOF simultaneous move
     - ``MOVE_P pick``
   * - ``MOVE_J``
     - ``<joint_id> <angle>``
     - Move single joint (0–5) to target angle
     - ``MOVE_J 0 45.0``
   * - ``MOVE_REL``
     - ``<joint_id> <delta>``
     - Relative angle adjustment for single joint
     - ``MOVE_REL 4 -10.0``
   * - ``PRESET``
     - ``<preset_name>``
     - Move to built-in posture preset
     - ``PRESET inspect``
   * - ``SPEED``
     - ``<deg_per_sec>``
     - Set global default joint motion speed
     - ``SPEED 60.0``
   * - ``SPEED_JOINT``
     - ``<joint_id> <deg_per_sec>``
     - Set joint-specific velocity limit
     - ``SPEED_JOINT 1 45.0``
   * - ``OVERRIDE``
     - ``<factor>``
     - Global speed scaling factor (0.05 – 1.0)
     - ``OVERRIDE 0.75``
   * - ``GRIPPER``
     - ``<angle_or_val>``
     - Command end-effector gripper aperture
     - ``GRIPPER 80.0``
   * - ``TOOL_ROLL``
     - ``<angle>``
     - Set wrist / tool roll orientation (J5)
     - ``TOOL_ROLL 90.0``
   * - ``WAIT_MS``
     - ``<millis>``
     - Dwell/pause execution for specified milliseconds
     - ``WAIT_MS 500``
   * - ``SYNC``
     - None
     - Synchronize and wait for physical motion completion
     - ``SYNC``
   * - ``HOME``
     - None
     - Move all joints to factory neutral / home position (90°)
     - ``HOME``
   * - ``STOP``
     - None
     - Immediate emergency stop for all joints
     - ``STOP``

Example: Automated Pick & Place Sequence
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: text

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

Integrated Mecha Script Editor Tab
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The GUI provides a dedicated tab ``[ 📝 Mecha Script Editor ]`` alongside ``[ 🎮 Manual Workspace ]``:

* **Syntax Highlighter**: Real-time token coloring matching the Catppuccin Mocha theme (commands in mauve, points/variables in blue, numbers in peach, comments in overlay).
* **Interactive Example Catalog**: Instant loading of pre-bundled routines (*Pick and Place*, *Scan Workspace*, *Joint Calibration*, *Preset Tour*).
* **Kinematic Bounds Linter**: Displays real-time warnings and errors if any commanded angle exceeds physical limits (J0: 0°–180°, J1/J2: 15°–165°, J3: 0°–180°, J4: 15°–165°, J5: 0°–180°).
* **Asynchronous Streaming Runner**: One-click compilation and sequential execution over physical USB CDC or virtual simulator without freezing the UI.

📐 Kinematic & Joint Configuration
----------------------------------

.. list-table:: Joint Kinematics Limits
   :widths: 10 15 35 20 20
   :header-rows: 1

   * - Joint ID
     - Channel
     - Name
     - Safe Angle Range
     - Neutral (Home)
   * - **J0**
     - Ch 0
     - ``Base Rotation``
     - 0° – 180°
     - 90°
   * - **J1**
     - Ch 1
     - ``Shoulder Lift Left``
     - 15° – 165°
     - 90°
   * - **J2**
     - Ch 2
     - ``Shoulder Lift Right``
     - 15° – 165°
     - 90°
   * - **J3**
     - Ch 3
     - ``Elbow Roll``
     - 0° – 180°
     - 90°
   * - **J4**
     - Ch 4
     - ``End-effector Tilt``
     - 15° – 165°
     - 90°
   * - **J5**
     - Ch 5
     - ``Tool End Rotation``
     - 0° – 180°
     - 90°

📡 Unified Serial ASCII Communication Protocol
----------------------------------------------

.. list-table:: Serial ASCII Communication Protocol
   :widths: 15 35 30 20
   :header-rows: 1

   * - Command
     - Arguments
     - Description
     - Example
   * - ``SET``
     - ``<joint_id> <angle>``
     - Move specific joint with default speed
     - ``SET 0 90.00``
   * - ``SETP``
     - ``<j0> <j1> <j2> <j3> <j4> <j5>``
     - Move all joints simultaneously
     - ``SETP 90 90 90 90 90 90``
   * - ``SPEED``
     - ``<joint_id> <deg_per_sec>``
     - Set maximum joint movement velocity
     - ``SPEED 1 45.0``
   * - ``HOME``
     - None
     - Return all joints to home position (90°)
     - ``HOME``
   * - ``STOP``
     - None
     - Immediate emergency stop for all joints
     - ``STOP``
   * - ``STATUS``
     - None
     - Query current joint angles
     - ``STATUS``
   * - ``PING``
     - None
     - Heartbeat ping
     - ``PING`` -> ``PONG``


📊 Code coverage
----------------

.. csv-table:: Code coverage
   :file: coverage_table.csv
   :widths: 60, 10, 10, 20
   :header-rows: 1

🛠 Usage
--------

Install package:

.. code-block:: bash

    pip3 install mecharmory

Launch the desktop motion studio:

.. code-block:: bash

    mecharmory

Or via python directly:

.. code-block:: bash

    python3 main.py

📚 Docs
-------

More documentation and info at

* `mecharmory.readthedocs.io <https://mecharmory.readthedocs.io>`_
* `www.python.org <https://www.python.org/>`_

👥 Contributing
---------------

`Contributing to mecharmory <https://github.com/vroncevic/mecharmory/blob/dev/CONTRIBUTING.md>`_

📄 Copyright and licence
-------------------------

Copyright (C) 2026 by `vroncevic.github.io/mecharmory <https://vroncevic.github.io/mecharmory>`_

**mecharmory** is free software; you can redistribute it and/or modify
it under the same terms as Python itself, either Python version 3.x or,
at your option, any later version of Python 3 you may have available.
