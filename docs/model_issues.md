# Domain Model Layer Architecture Audit & Issues

## Overview
This document tracks architectural evaluations, SOLID audits, and refactorings within the Domain Model Layer (`mecharmory/core/model/`), covering core entities, value objects, joint configurations, states, and domain messages.

---

## Master Roadmap Matrix

| ID | Component | Description | Status | Target Module |
|---|---|---|---|---|
| MODEL-001 | Kinematics Models | Value objects immutability and granular joint state encapsulation | 🟢 RESOLVED | `mecharmory.core.model.kinematics` |
| MODEL-002 | Arm Model | Complete encapsulation of 6-DOF joint models and posture presets | 🟢 RESOLVED | `mecharmory.core.model.arm` |
| MODEL-003 | Communication Messages | Immutable value object for bidirectional serial messages | 🟢 RESOLVED | `mecharmory.core.model.communication` |
| MODEL-004 | Mecha DSL Models | AST, Tokens, and Diagnostic Value Objects for .mecha Language | 🟢 RESOLVED | `mecharmory.core.model.dsl` |

---

## Audit Items

### 🟢 MODEL-001: Kinematics Value Objects & Entities
* **Affected Files:**
  * `mecharmory/core/model/kinematics/joint_id.py`
  * `mecharmory/core/model/kinematics/joint_config.py`
  * `mecharmory/core/model/kinematics/joint_state.py`
* **Status:** Clean separation of immutable configuration vs runtime joint state. Single responsibility per module.

### 🟢 MODEL-002: Manipulator Aggregate Root
* **Affected Files:**
  * `mecharmory/core/model/arm/arm_model.py`
  * `mecharmory/core/model/arm/iarm_model.py`
* **Status:** Conforms to `IArmModel` protocol without concrete inheritance, granular imports, full type annotation support.

### 🟢 MODEL-003: Communication Value Objects
* **Affected Files:**
  * `mecharmory/core/model/communication/serial_message.py`
* **Status:** Immutable dataclass for serial logging and UI telemetry queuing.

### 🟢 MODEL-004: Mecha DSL Domain Models (AST, Tokens, Diagnostics)
* **Affected Files:**
  * `mecharmory/core/model/dsl/token/mecha_token_type.py`
  * `mecharmory/core/model/dsl/token/mecha_token.py`
  * `mecharmory/core/model/dsl/ast/mecha_command_type.py`
  * `mecharmory/core/model/dsl/ast/imecha_instruction.py`
  * `mecharmory/core/model/dsl/ast/mecha_instruction.py`
  * `mecharmory/core/model/dsl/ast/imecha_program.py`
  * `mecharmory/core/model/dsl/ast/mecha_program.py`
  * `mecharmory/core/model/dsl/diagnostic/mecha_diagnostic_severity.py`
  * `mecharmory/core/model/dsl/diagnostic/imecha_diagnostic.py`
  * `mecharmory/core/model/dsl/diagnostic/mecha_diagnostic.py`
* **Status:** Full structural protocol decoupling, one class per module under 250 lines, immutable frozen dataclasses for tokens and diagnostics.

