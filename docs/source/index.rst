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

✨ Features
-----------

* **Catppuccin Mocha Dark UI**: Modern, ergonomic design with high contrast, vibrant accents, and smooth controls.
* **2D Real-Time Kinematic Visualizer**: Graphical rendering of base rotation, shoulder dual-lift tandem linkage, elbow tube roll, tool pitch, and tool end flange.
* **Virtual Firmware Mode**: Built-in 50 Hz RP2040 emulator allows complete testing and posture planning without physical hardware connected.
* **Physical RP2040 Serial Streaming**: Direct connection to Raspberry Pi Pico C firmware over USB CDC serial (``/dev/ttyACM*``).
* **Interactive Console**: Live bidirectional monitor with color-coded TX/RX logs and raw ASCII command prompt.

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
