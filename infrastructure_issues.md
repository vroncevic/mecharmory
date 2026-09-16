# Infrastructure Layer Architecture Audit & Issues

## Overview
This document tracks architectural evaluations, SOLID audits, and refactorings within the Infrastructure Layer (`mecharmory/infrastructure/`), covering GUI presentation, hardware/virtual serial communication, CLI adapters, and configuration storage.

---

## Master Roadmap Matrix

| ID | Component | Description | Status | Target Module |
|---|---|---|---|---|
| INFRA-001 | GUI Presentation | Horizontal Serial Monitor Bottom Dock & Expanded Kinematics Preview | 🟢 RESOLVED | `mecharmory.infrastructure.gui` |
| INFRA-002 | GUI Window | Tkinter geometry decoupling and responsive packaging | 🟢 RESOLVED | `mecharmory.infrastructure.gui.gui_window` |
| INFRA-003 | Communication | Hardware & Virtual Serial Transport isolation | 🟢 RESOLVED | `mecharmory.infrastructure.communication` |
| INFRA-004 | GUI Console | ConsolePanel modular decomposition into dedicated sub-widgets | 🟢 RESOLVED | `mecharmory.infrastructure.gui.console` |
| INFRA-005 | GUI Arm Control | ArmControlPanel modular decomposition into dedicated sub-widgets | 🟢 RESOLVED | `mecharmory.infrastructure.gui.arm` |
| INFRA-006 | GUI Canvas | Arm Canvas package literal extraction and architectural cleanup | 🟢 RESOLVED | `mecharmory.infrastructure.gui.canvas` |
| INFRA-007 | GUI Architecture | ArmCanvasPainter modular decomposition and Theme subpackage restructuring | 🟢 RESOLVED | `mecharmory.infrastructure.gui` |
| INFRA-008 | GUI Styling | Component-Scoped Style Architecture across all GUI subpackages | 🟢 RESOLVED | `mecharmory.infrastructure.gui` |
| INFRA-009 | GUI Refactoring | Comprehensive Literal & Metric Extraction Across All GUI Modules | 🟢 RESOLVED | `mecharmory.infrastructure.gui` |
| INFRA-010 | GUI Window | GuiWindow Modular Decomposition & ArmWorkspace Container | 🟢 RESOLVED | `mecharmory.infrastructure.gui` |
| INFRA-011 | Communication & Storage | Protocol check_available_port, ats_utilities Loader/Storer, Singleton ContextBundle & Constant Cleanup | 🟢 RESOLVED | `mecharmory.infrastructure` |
| INFRA-012 | GUI & Communication | Serial Telemetry Console Flooding Decoupling & 100ms Polling Optimization | 🟢 RESOLVED | `mecharmory.infrastructure.gui` |

---

## Audit Items

### 🟢 INFRA-001: Horizontal Serial Monitor Bottom Dock & Expanded Kinematics Preview
* **Affected Files:**
  * `mecharmory/infrastructure/gui/gui_window.py`
  * `mecharmory/infrastructure/gui/console/console_panel.py`
  * `mecharmory/infrastructure/gui/canvas/arm_canvas_preview.py`
  * `mecharmory/infrastructure/gui/canvas/arm_kinematics_2d.py`
* **Problem / Violation:**
  * In the original layout, the Serial Monitor & Command Console was vertically stacked in a narrow right-hand column (~380 px) below the 2D Kinematics Preview.
  * Long telemetry lines (`[timestamp] <- STATUS J0:... J1:... J2:... J3:... J4:... J5:...`) were severely truncated horizontally.
  * The 2D Kinematics Preview was compressed to a `340x300` canvas, limiting visual clarity and arm reach rendering.
* **Refactored Architecture:**
  * Re-architected `GuiWindow._setup_views()` into a two-tier workspace:
    * **Upper Workspace Row:** Left column for 6-DOF Joint Controls + Posture Presets; Right column (`width=480`) dedicated exclusively to the full-height Live 2D Kinematics Preview.
    * **Bottom Dock:** Full-width horizontal Serial Monitor & Command Console (`ConsolePanel`) spanning the complete window width (~1320 px).
  * Expanded `ArmCanvasPreview` canvas to `460x540` px and parameterized `ArmKinematics2D.compute_pose` with proportional visual link scaling (`scale=1.55`, `x0=110.0`).
  * Reordered `ConsolePanel` packing so the command input row (`cmd > [ ... ] [Send]`) is permanently anchored at `side=BOTTOM`, while the scrollable log area expands seamlessly.
* **Execution Checklist:**
  * [x] Update `ArmKinematics2D.compute_pose` to support `x0` and `scale`.
  * [x] Expand `ArmCanvasPreview` dimensions and kinematic paint calls.
  * [x] Update `ConsolePanel` packing order and set text height.
  * [x] Add `Select All` and `Copy` buttons with clipboard support and keyboard shortcuts (`Ctrl+A`, `Ctrl+C`).
  * [x] Reconfigure `GuiWindow` layout hierarchy and update geometry to fixed `1280x920`.
  * [x] Validate with unit tests and visual screenshot inspection.

### 🟢 INFRA-002: Tkinter Geometry & Responsive Packaging
* **Affected Files:**
  * `mecharmory/infrastructure/gui/gui_window.py`
  * `mecharmory/infrastructure/gui/joint/joint_widget_style.py`
* **Status:** Fixed non-resizable layout (`1280x920`) providing uncompressed, uniform dimensions across all 6 joint cards (J0-J5), full normalized visibility and height of Posture Presets toolbar buttons (`Home Position`, `Parked (Folded)`, `Forward Reach`, `High Reach`), and stable bottom dock console.

### 🟢 INFRA-003: Communication Transport Isolation
* **Affected Files:**
  * `mecharmory/infrastructure/communication/serial_transport.py`
  * `mecharmory/infrastructure/communication/virtual_serial_transport.py`
* **Status:** Hardware and virtual transports strictly satisfy `ISerialTransport` protocol without leaking lower-level driver dependencies.

### 🟢 INFRA-004: ConsolePanel Modular Decomposition
* **Affected Files:**
  * `mecharmory/infrastructure/gui/console/console_header_toolbar.py`
  * `mecharmory/infrastructure/gui/console/console_log_viewer.py`
  * `mecharmory/infrastructure/gui/console/console_command_entry.py`
  * `mecharmory/infrastructure/gui/console/console_panel.py`
* **Problem / Violation:**
  * `ConsolePanel` was becoming an oversized monolithic widget (~290 lines) embedding header title, action buttons, text log buffer, scrollbar, clipboard operations, prompt, entry, and send button in a single module with inline magic string literals.
* **Refactored Architecture:**
  * Decomposed into single-responsibility sub-widgets matching the pattern established in `infrastructure/gui/joint/`:
    * `ConsoleHeaderToolbar`: Dedicated module for section title and action buttons (`Clear`, `Copy`, `Select All`).
    * `ConsoleLogViewer`: Dedicated module for scrollable text log, color tags, text selection, and clipboard operations.
    * `ConsoleCommandEntry`: Dedicated module for command prompt, entry box, and submit action.
    * `ConsolePanel`: Composite coordinator delegating to sub-widgets while maintaining 100% public API backwards compatibility.
  * Extracted all literals into typed class-level constant attributes (`TITLE_TEXT`, `BTN_CLEAR_TEXT`, `TAG_TX`, `PROMPT_TEXT`, etc.).
* **Execution Checklist:**
  * [x] Create `ConsoleHeaderToolbar` with extracted text literals.
  * [x] Create `ConsoleLogViewer` with tag constants and clipboard methods.
  * [x] Create `ConsoleCommandEntry` with prompt and button constants.
  * [x] Refactor `ConsolePanel` as composite container.
  * [x] Validate individual components and end-to-end composition via automated tests.

### 🟢 INFRA-005: ArmControlPanel Modular Decomposition
* **Affected Files:**
  * `mecharmory/infrastructure/gui/arm/arm_control_header.py`
  * `mecharmory/infrastructure/gui/arm/arm_joint_list.py`
  * `mecharmory/infrastructure/gui/arm/arm_control_panel.py`
* **Problem / Violation:**
  * `ArmControlPanel` previously handled header layout, action buttons (`EMERGENCY STOP`, `Home All`, `Query Status`), and direct loop instantiation and telemetry polling of all 6 `JointControlWidget` instances in a single module with inline magic strings.
* **Refactored Architecture:**
  * Decomposed into single-responsibility collaborating components:
    * `ArmControlHeader`: Dedicated module for section title and global manipulator actions (`Query Status`, `Home All`, `EMERGENCY STOP`).
    * `ArmJointList`: Dedicated module managing the 6-DOF `JointControlWidget` collection, packing, and telemetry refresh.
    * `ArmControlPanel`: Composite coordinator maintaining 100% public API backwards compatibility.
  * Extracted all literals into typed class-level constant attributes (`TITLE_TEXT`, `BTN_STOP_TEXT`, `BTN_HOME_TEXT`, `BTN_QUERY_TEXT`, `ORDERED_JOINTS`).
* **Execution Checklist:**
  * [x] Create `ArmControlHeader` with extracted literals and global action buttons.
  * [x] Create `ArmJointList` with `ORDERED_JOINTS` constant and telemetry refresh.
  * [x] Refactor `ArmControlPanel` as composite container.
  * [x] Validate components and composite behavior via automated tests.

### 🟢 INFRA-006: Arm Canvas Package Literal Extraction and Cleanup
* **Affected Files:**
  * `mecharmory/infrastructure/gui/canvas/arm_canvas_preview.py`
  * `mecharmory/infrastructure/gui/canvas/arm_canvas_painter.py`
  * `mecharmory/infrastructure/gui/canvas/arm_kinematics_2d.py`
  * `mecharmory/infrastructure/gui/canvas/arm_pose_2d.py`
* **Problem / Violation:**
  * Magic numbers, geometry offsets, line widths, colors, and format strings were hardcoded inside drawing and kinematic calculation methods across the `canvas` package.
  * Class docstrings lacked formal `:attributes:` definitions for visual layout metrics and telemetry templates.
* **Refactored Architecture:**
  * `ArmCanvasPreview`: Extracted `TITLE_TEXT`, `CANVAS_WIDTH`, `CANVAS_HEIGHT`, `GROUND_OFFSET`, `BASE_X0`, `KINEMATICS_SCALE`, `PAD_X`, `PAD_Y`, `PAD_TITLE_Y`, `TITLE_FONT_SIZE`, `TITLE_FONT_WEIGHT`, and `CANVAS_BORDER_WIDTH` into typed class constants.
  * `ArmCanvasPainter`: Extracted all ground plane parameters (`GROUND_TEXT`, `GROUND_LINE_PADDING_X`, `GROUND_LINE_WIDTH`, `GROUND_TEXT_X`, `GROUND_TEXT_Y_OFFSET`, `GROUND_FONT_SIZE`), base pedestal & turntable geometry, dual lift linkage attributes (`ROD_OFFSET`, `ROD_LINE_WIDTH`, `ROD_DASH_PATTERN`, `BOOM_LINE_WIDTH`, `BOOM_CAP_STYLE`, joint marker radii and outlines), cylindrical tube & roll indicator parameters, end bracket & tool flange parameters, and HUD overlay constants (`HUD_OFFSET_X`, `HUD_OFFSET_Y`, `HUD_ANCHOR`, `HUD_FONT_SIZE`, `HUD_JUSTIFY`, `HUD_TEMPLATE`).
  * `ArmKinematics2D`: Extracted default kinematic parameters (`DEFAULT_GROUND_Y`, `DEFAULT_X0`, `DEFAULT_SCALE`, `SHOULDER_HEIGHT_OFFSET`, `LEN_BOOM`, `LEN_TUBE`, `LEN_END`, `BASE_ANGLE_OFFSET`, `PERPENDICULAR_OFFSET`) into typed class constants.
  * Enhanced class docstrings with complete `:attributes:` and `:methods:` sections adhering to Python coding standards.
* **Execution Checklist:**
  * [x] Extract class-level constants and update docstrings in `ArmCanvasPreview`.
  * [x] Extract class-level constants and update docstrings in `ArmCanvasPainter`.
  * [x] Extract class-level constants and update docstrings in `ArmKinematics2D`.
  * [x] Validate complete test suite (56 tests passing).
  * [x] Verify visual rendering fidelity via GUI snapshot capture.

### 🟢 INFRA-007: ArmCanvasPainter Modular Decomposition & Theme Subpackage Restructuring
* **Affected Files:**
  * `mecharmory/infrastructure/gui/theme/theme_manager.py`
  * `mecharmory/infrastructure/gui/theme/__init__.py`
  * `mecharmory/infrastructure/gui/canvas/arm_canvas_style.py`
  * `mecharmory/infrastructure/gui/canvas/arm_background_painter.py`
  * `mecharmory/infrastructure/gui/canvas/arm_pedestal_painter.py`
  * `mecharmory/infrastructure/gui/canvas/arm_linkage_painter.py`
  * `mecharmory/infrastructure/gui/canvas/arm_tube_painter.py`
  * `mecharmory/infrastructure/gui/canvas/arm_tool_painter.py`
  * `mecharmory/infrastructure/gui/canvas/arm_hud_painter.py`
  * `mecharmory/infrastructure/gui/canvas/arm_canvas_painter.py`
* **Problem / Violation:**
  * `theme.py` was a loose file sitting in `mecharmory/infrastructure/gui/`, causing architectural inconsistency with other GUI subpackages (`arm`, `canvas`, `console`, `joint`, `preset`, `serial`).
  * `ArmCanvasPainter` was a monolithic class (461 lines) responsible for all rendering primitives across the robot manipulator alongside 40+ literals hardcoded inside the class.
* **Refactored Architecture:**
  * Promoted `gui/theme/` to a dedicated package containing `ThemeManager` (`theme_manager.py`) with strict metadata-only `__init__.py` and granular imports across consumers.
  * Created `@dataclass(frozen=True, slots=True)` `ArmCanvasStyle` encapsulating all visual drawing metrics and layout literals.
  * Decomposed `ArmCanvasPainter` into single-responsibility, focused painters ($\le 60\text{--}80$ total lines each):
    * `ArmBackgroundPainter`: Ground line and datum text rendering.
    * `ArmPedestalPainter`: Base pedestal and yaw turntable indicator.
    * `ArmLinkagePainter`: Shoulder joint, main boom, and parallel linkage rod.
    * `ArmTubePainter`: Elbow joint, cylindrical forearm tube, and roll indicator.
    * `ArmToolPainter`: Wrist joint, end tilt bracket, tool flange, and tool roll mark.
    * `ArmHudPainter`: HUD telemetry text overlay.
  * Refactored `ArmCanvasPainter` into an ultra-clean coordinating facade maintaining 100% public API compatibility.
* **Execution Checklist:**
  * [x] Convert `gui/theme` into dedicated subpackage with `theme_manager.py`.
  * [x] Update all `ThemeManager` consumer imports across the codebase.
  * [x] Create `ArmCanvasStyle` frozen dataclass with default visual parameters.
  * [x] Create specialized painter modules (`ArmBackgroundPainter`, `ArmPedestalPainter`, `ArmLinkagePainter`, `ArmTubePainter`, `ArmToolPainter`, `ArmHudPainter`).
  * [x] Refactor `ArmCanvasPainter` as coordinating facade.
  * [x] Add unit tests for `ArmCanvasStyle` (`TestArmCanvasStyle`).
  * [x] Pass 100% quality gates (`interfaces_checker`, `isp_checker`, `limits_checker`, `srp_checker`).
  * [x] Attain 88% overall code coverage with 100% coverage across canvas modules.

### 🟢 INFRA-008: Component-Scoped Style Architecture Across All GUI Subpackages
* **Affected Files:**
  * `mecharmory/infrastructure/gui/arm/arm_panel_style.py`
  * `mecharmory/infrastructure/gui/arm/arm_control_header.py`
  * `mecharmory/infrastructure/gui/arm/arm_joint_list.py`
  * `mecharmory/infrastructure/gui/arm/arm_control_panel.py`
  * `mecharmory/infrastructure/gui/joint/joint_widget_style.py`
  * `mecharmory/infrastructure/gui/joint/joint_step_buttons.py`
  * `mecharmory/infrastructure/gui/joint/joint_entry_control.py`
  * `mecharmory/infrastructure/gui/joint/joint_control_widget.py`
  * `mecharmory/infrastructure/gui/preset/preset_panel_style.py`
  * `mecharmory/infrastructure/gui/preset/preset_panel.py`
  * `mecharmory/infrastructure/gui/serial/serial_panel_style.py`
  * `mecharmory/infrastructure/gui/serial/serial_status_badge.py`
  * `mecharmory/infrastructure/gui/serial/serial_port_selector.py`
  * `mecharmory/infrastructure/gui/serial/serial_bar.py`
  * `mecharmory/infrastructure/gui/console/console_panel_style.py`
  * `mecharmory/infrastructure/gui/console/console_header_toolbar.py`
  * `mecharmory/infrastructure/gui/console/console_command_entry.py`
  * `mecharmory/infrastructure/gui/console/console_log_viewer.py`
  * `mecharmory/infrastructure/gui/console/console_panel.py`
* **Problem / Violation:**
  * Individual GUI components contained inline magic constants for dimensions, paddings, fonts, and text literals.
  * Lack of uniform styling abstraction across subpackages (`arm`, `joint`, `preset`, `serial`, `console`).
* **Refactored Architecture:**
  * Adopted a two-tier styling hierarchy across the entire presentation layer:
    * **Tier 1 (Global Design Tokens):** `mecharmory.infrastructure.gui.theme.theme_manager.ThemeManager` providing system color palette, monospace and UI typography tokens.
    * **Tier 2 (Component-Scoped Styles):** Dedicated `@dataclass(frozen=True, slots=True)` in each subpackage (`ArmPanelStyle`, `JointWidgetStyle`, `PresetPanelStyle`, `SerialPanelStyle`, `ConsolePanelStyle`) defining local layout padding, geometry, and component-specific string literals.
  * Parameterized widgets with optional `style: SubpackageStyle | None = None` defaulting to `DEFAULT_STYLE`, enabling full backward compatibility while supporting decoupled style injection.
* **Execution Checklist:**
  * [x] Create `ArmPanelStyle` and refactor `arm/` subpackage components.
  * [x] Create `JointWidgetStyle` and refactor `joint/` subpackage components.
  * [x] Create `PresetPanelStyle` and refactor `preset/` subpackage components.
  * [x] Create `SerialPanelStyle` and refactor `serial/` subpackage components.
  * [x] Create `ConsolePanelStyle` and refactor `console/` subpackage components.
  * [x] Add comprehensive unit tests for all style models (`TestArmPanelStyle`, `TestJointWidgetStyle`, `TestPresetPanelStyle`, `TestSerialPanelStyle`, `TestConsolePanelStyle`).
  * [x] Pass 100% quality gates and attain 89% total code coverage with 100% coverage on all style dataclasses.

### 🟢 INFRA-009: Comprehensive Literal & Metric Extraction Across All GUI Modules
* **Affected Files:**
  * `mecharmory/infrastructure/gui/gui_window.py`
  * `mecharmory/infrastructure/gui/gui_event_mediator.py`
  * `mecharmory/infrastructure/gui/joint/joint_widget_style.py`
  * `mecharmory/infrastructure/gui/joint/joint_step_buttons.py`
  * `mecharmory/infrastructure/gui/joint/joint_control_widget.py`
  * `mecharmory/infrastructure/gui/joint/joint_entry_control.py`
  * `mecharmory/infrastructure/gui/serial/serial_panel_style.py`
  * `mecharmory/infrastructure/gui/serial/serial_bar.py`
  * `mecharmory/infrastructure/gui/serial/serial_port_selector.py`
  * `mecharmory/infrastructure/gui/serial/serial_status_badge.py`
  * `mecharmory/infrastructure/gui/console/console_panel_style.py`
  * `mecharmory/infrastructure/gui/console/console_log_viewer.py`
  * `mecharmory/infrastructure/gui/canvas/arm_canvas_preview.py`
  * `mecharmory/infrastructure/gui/preset/preset_panel_style.py`
  * `mecharmory/infrastructure/gui/preset/preset_panel.py`
  * `mecharmory/infrastructure/gui/arm/arm_panel_style.py`
  * `mecharmory/infrastructure/gui/arm/arm_control_header.py`
  * `tests/joint_widget_style_test.py`
  * `tests/serial_panel_style_test.py`
  * `tests/console_panel_style_test.py`
  * `tests/preset_panel_style_test.py`
  * `tests/arm_panel_style_test.py`
  * `tests/gui_event_mediator_test.py`
  * `tests/gui_window_test.py`
* **Problem / Violation:**
  * Residual inline magic numbers, strings, format templates, keybindings, state strings, fallback port lists, and geometry metrics remained embedded directly within implementation methods across GUI subpackages.
  * In particular, J5: Tool (Roll) step buttons had experienced vertical squishing under constrained window geometry, requiring window expansion and uniform layout sizing across all 6 joint cards.
* **Refactored Architecture:**
  * Fixed window geometry standardized to `1280x920` (`WINDOW_GEOMETRY`) with `resizable(False, False)` and extracted layout constants (`BODY_PAD_X`, `BODY_PAD_Y`, `UPPER_ROW_SPACING_Y`, `LEFT_COL_SPACING_X`, `CONTROL_PANEL_SPACING_Y`, `RIGHT_COL_WIDTH`, `POLL_INTERVAL_MS`, `PROTOCOL_DELETE_WINDOW`).
  * `JointWidgetStyle`: Extracted button texts (`'-5°'`, `'-1°'`, `'+1°'`, `'+5°'`), numerical step deltas (`5.0`, `1.0`), format templates (`'{min:.1f}° to {max:.1f}°'`, `'{angle:6.1f}°'`, `'{val:.1f}'`), sync threshold (`0.4`), and button padding (`step_btn_pad_y = 1`, `btn_set_pad_y = 1`).
  * `SerialPanelStyle`: Extracted button spacing (`connect_btn_spacing_x`), selector label font size and padding, combobox state (`'readonly'`), scan button styling, baud combobox margins, fallback ports list, disconnect color badge (`'#ffffff'`), and status string (`'Disconnected'`).
  * `ConsolePanelStyle`: Extracted wrap mode (`'none'`), text state flags (`'disabled'`, `'normal'`), start index (`'1.0'`), direction indicator (`'TX'`), keybindings (`'<Control-a>'`, `'<Control-A>'`, `'<Control-c>'`, `'<Control-C>'`), and timestamp format template.
  * `Canvas`: Replaced string literals with imported Tkinter constants (`BOTH`, `W`).
  * `PresetPanelStyle` & `ArmPanelStyle`: Extracted font weight tokens (`title_font_weight`, `btn_font_weight`).
  * `GuiEventMediator`: Extracted ASCII protocol command strings (`CMD_PING`, `CMD_HOME`, `CMD_STOP`, `CMD_STATUS`), formatting templates (`CMD_SET_TEMPLATE`), and log prefixes (`LOG_PRESET_PREFIX`).
* **Execution Checklist:**
  * [x] Set fixed non-resizable window geometry `1280x920` and extract window layout metrics.
  * [x] Center step and set buttons vertically with pad_y=1 in joint control cards.
  * [x] Extract all literals from `joint/` subpackage into `JointWidgetStyle`.
  * [x] Extract all literals from `serial/` subpackage into `SerialPanelStyle`.
  * [x] Extract all literals from `console/` subpackage into `ConsolePanelStyle`.
  * [x] Extract literals from `canvas/` subpackage.
  * [x] Extract font weights from `preset/` and `arm/` subpackages into their styles.
  * [x] Extract ASCII command constants and templates into `GuiEventMediator`.
  * [x] Update all unit tests and add `gui_event_mediator_test.py` and `gui_window_test.py` (88 tests passing).
  * [x] Verify quality gates pass 100% and test coverage reaches 90%.

### 🟢 INFRA-010: GuiWindow Modular Decomposition & ArmWorkspace Container
* **Affected Files:**
  * `mecharmory/infrastructure/gui/gui_window_style.py`
  * `mecharmory/infrastructure/gui/workspace/__init__.py`
  * `mecharmory/infrastructure/gui/workspace/arm_workspace.py`
  * `mecharmory/infrastructure/gui/gui_window.py`
  * `tests/gui_window_style_test.py`
  * `tests/arm_workspace_test.py`
  * `tests/gui_window_test.py`
* **Problem / Violation:**
  * `GuiWindow` was an overloaded coordinator class (257 lines) that mixed window lifecycle, layout metrics definitions, multi-level widget container building (`_setup_views`), and synchronized visual updates.
  * Unlike other GUI subpackages that use dedicated `@dataclass(frozen=True, slots=True)` styles, `GuiWindow` embedded 10 class-level layout constants directly.
  * The upper workspace (joint controls, posture presets toolbar, live 2D kinematics preview) was manually constructed and packed inside `GuiWindow._setup_views` without container encapsulation.
* **Refactored Architecture:**
  * Created `@dataclass(frozen=True, slots=True)` `GuiWindowStyle` in `gui_window_style.py` encapsulating all window metrics, geometry, timings, and paddings.
  * Created `ArmWorkspace` composite container in dedicated `mecharmory.infrastructure.gui.workspace` package managing the two-column upper workspace and providing `refresh_visuals()`.
  * Refactored `GuiWindow` to cleanly compose `SerialBar`, `ArmWorkspace`, and `ConsolePanel` while maintaining 100% backward compatibility.
  * Extracted private helper `_drain_ui_queue()` to decouple communication queue polling from visualization updates.
* **Execution Checklist:**
  * [x] Create `GuiWindowStyle` frozen dataclass with default metrics.
  * [x] Create `workspace/` package with metadata-only `__init__.py`.
  * [x] Create `ArmWorkspace` composite container with `refresh_visuals()`.
  * [x] Refactor `GuiWindow` to delegate workspace and style management.
  * [x] Add comprehensive unit tests (`gui_window_style_test.py`, `arm_workspace_test.py`, `gui_window_test.py`).
  * [x] Validate with 95 passing unit tests and visual rendering verification.

### 🟢 INFRA-011: Protocol check_available_port, ats_utilities Loader/Storer, Singleton ContextBundle & Constant Cleanup
* **Affected Files:**
  * `mecharmory/infrastructure/communication/iserial_port_scanner.py`
  * `mecharmory/infrastructure/communication/serial_port_scanner.py`
  * `mecharmory/infrastructure/communication/serial_preferences.py`
  * `mecharmory/infrastructure/storage/arm_storage_service.py`
  * `mecharmory/setup/factory.py`
  * `mecharmory/infrastructure/gui/arm/arm_control_header.py`
  * `mecharmory/infrastructure/gui/console/console_command_entry.py`
  * `mecharmory/infrastructure/gui/console/console_log_viewer.py`
  * `mecharmory/infrastructure/gui/console/console_panel.py`
  * `mecharmory/infrastructure/gui/gui_window.py`
  * `tests/serial_port_scanner_test.py`
  * `tests/serial_preferences_test.py`
  * `tests/arm_storage_service_test.py`
  * `tests/service_engine_test.py`
* **Problem / Violation:**
  * Port discovery interface `ISerialPortScanner` lacked a direct predicate `check_available_port(port_name: str) -> bool`.
  * `SerialPortScanner` methods were staticmethods with hardcoded string literals instead of `@classmethod` and `Final` constants (`RP2040_VID`, `KEYWORD_PICO`, `KEYWORD_RASPBERRY`).
  * `SerialPreferences` used standard library `json` (`dumps`, `loads`) and manual file I/O instead of the framework-standard `ats_utilities.config_io` `Loader` and `Storer`.
  * `ArmStorageService` allowed ad-hoc instantiation of `ContextBundle` via fallback `ContextBundleFactory.create_bundle()`, violating the architectural constraint that `ContextBundle` must be unique across the entire application and created solely in the application factory (`MecharmoryBundleFactory`).
  * Sub-components (`ArmControlHeader`, `ConsoleCommandEntry`, `ConsoleLogViewer`) duplicated styling literals as class-level alias constants despite dedicated `@dataclass(frozen=True)` style objects.
  * `ConsolePanel` maintained redundant storage (`self._on_send`) and wrapper method (`_handle_send`) instead of passing the callback directly to `ConsoleCommandEntry`.
* **Refactored Architecture:**
  * Added `check_available_port(self, port_name: str) -> bool` to `ISerialPortScanner` protocol and implemented it as `@classmethod` in `SerialPortScanner`.
  * Extracted `Final` constants (`RP2040_VID`, `KEYWORD_PICO`, `KEYWORD_RASPBERRY`) in `SerialPortScanner`.
  * Refactored `SerialPreferences` to use `ats_utilities.config_io.loader.engine.Loader` and `ats_utilities.config_io.storer.engine.Storer`, extracting `Final` constants (`PREFS_FILE_PATH`, `KEY_PORT`, `KEY_BAUDRATE`, `DEFAULT_PORT`, `DEFAULT_BAUDRATE`).
  * Enforced strict singleton `ContextBundle` injection: `ArmStorageService` requires `context_bundle: ContextBundle` in its constructor, injected from `MecharmoryBundleFactory`.
  * Instantiated `SerialPreferences` in `MecharmoryBundleFactory` and threaded it cleanly into `GuiWindow` and `SerialBar`.
  * Removed redundant alias constants and unnecessary callback storage in GUI components.
* **Execution Checklist:**
  * [x] Add `check_available_port` to `ISerialPortScanner` protocol.
  * [x] Implement `check_available_port` and convert methods to `@classmethod` in `SerialPortScanner`.
  * [x] Refactor `SerialPreferences` to use `ats_utilities` Loader/Storer and `Final` constants.
  * [x] Enforce mandatory `context_bundle` in `ArmStorageService` and inject from `MecharmoryBundleFactory`.
  * [x] Clean up redundant alias constants from `ArmControlHeader`, `ConsoleCommandEntry`, `ConsoleLogViewer`.
  * [x] Remove duplicate callback storage and wrapper from `ConsolePanel`.
  * [x] Add `serial_port_scanner_test.py` and update existing test suites.
  * [x] Validate all 102 unit tests pass with zero regressions.

### 🟢 INFRA-012: Serial Telemetry Console Flooding Decoupling & 100ms Polling Optimization
* **Affected Files:**
  * `mecharmory/infrastructure/gui/gui_window_style.py`
  * `mecharmory/infrastructure/gui/gui_event_mediator.py`
  * `tests/gui_window_style_test.py`
  * `tests/gui_window_test.py`
  * `tests/gui_event_mediator_test.py`
* **Problem / Violation:**
  * `GuiWindowStyle.poll_interval_ms` was configured to `40` ms (25 Hz), generating 25 queries and 25 responses per second over the serial transport.
  * `GuiEventMediator.on_serial_rx` unconditionally forwarded every incoming line into `_ui_queue`, flooding `ConsoleLogViewer` with 1,500 identical `STATUS J0:... MOVING:0` lines per minute.
  * The resulting log flood buried actual user commands and device acknowledgements (`SET`, `HOME`, `ACK`, `ERR`), caused continuous disruptive autoscrolling, and wasted Tkinter text widget memory and CPU.
* **Refactored Architecture:**
  * Re-tuned `poll_interval_ms` to `100` ms (10 Hz) in `GuiWindowStyle`, reducing serial bus traffic and RP2040 Pico interrupt load by 60% while maintaining smooth 10 FPS kinematics preview on the 2D Canvas.
  * Decoupled telemetry streaming from the user-facing serial console in `GuiEventMediator`:
    * Added `_manual_status_requests_pending: int` tracking explicit user status queries (via `on_query_status` button click or typing `STATUS` in the console input).
    * Suppressed unsolicited periodic background telemetry `STATUS` responses from entering `_ui_queue` (and therefore `ConsoleLogViewer`).
    * Permitted explicit manual `STATUS` query responses to display cleanly in the console alongside all normal command outputs (`ACK`, `ERR`, `HOME`, `STOP`, `PING -> PONG`).
    * Preserved direct telemetry dispatch to `ArmControllerService` (via its independent `serial_service.register_rx_callback`), guaranteeing uninterrupted real-time kinematic updates of `ArmModel`, 2D Canvas, and sliders.
* **Execution Checklist:**
  * [x] Update `poll_interval_ms` to `100` in `GuiWindowStyle`.
  * [x] Implement manual status request tracking and background telemetry filtering in `GuiEventMediator`.
  * [x] Update `gui_window_style_test.py` and `gui_window_test.py` to assert `poll_interval_ms == 100`.
  * [x] Add unit tests in `gui_event_mediator_test.py` for background status filtering and manual status query display.
  * [x] Verify visual GUI appearance and clean console log via screenshot capture.
  * [x] Validate that all 105 unit tests pass with zero errors.



