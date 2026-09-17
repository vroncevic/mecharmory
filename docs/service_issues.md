# Application Service Layer Architecture Audit & Issues

## Overview
This document tracks architectural evaluations, SOLID audits, and refactorings within the Application Service Layer (`mecharmory/core/service/`), covering controller services, serial communications orchestrators, and storage interactors.

---

## Master Roadmap Matrix

| ID | Component | Description | Status | Target Module |
|---|---|---|---|---|
| SERV-001 | Arm Controller Service | Joint angle dispatching and safety bounds checking | 🟢 RESOLVED | `mecharmory.core.service.arm` |
| SERV-002 | Serial Service | Asynchronous queue draining and threading boundary | 🟢 RESOLVED | `mecharmory.core.service.serial` |
| SERV-003 | Service Container | Facade engine unifying domain services | 🟢 RESOLVED | `mecharmory.core.service.engine` |
| SERV-004 | Mecha DSL Service | Lexer, Parser, Kinematic Linter, and Compiler for .mecha Scripts | 🟢 RESOLVED | `mecharmory.core.service.dsl` |

---

## Audit Items

### 🟢 SERV-001: Arm Controller Service
* **Affected Files:**
  * `mecharmory/core/service/arm/arm_controller_service.py`
  * `mecharmory/core/service/arm/iarm_controller_service.py`
* **Status:** Implements `IArmControllerService` structurally. Coordinates target validation against joint configurations prior to serial command dispatch.

### 🟢 SERV-002: Serial Orchestration Service
* **Affected Files:**
  * `mecharmory/core/service/serial/serial_service.py`
  * `mecharmory/core/service/serial/iserial_service.py`
* **Status:** Provides thread-safe communication bridging physical hardware and virtual firmware transports.

### 🟢 SERV-003: Service Aggregate Container
* **Affected Files:**
  * `mecharmory/core/service/engine.py`
  * `mecharmory/core/service/iservice.py`
* **Status:** Structural protocol implementation grouping arm, serial, and storage services.

### 🟢 SERV-004: Mecha DSL Processing Pipeline
* **Affected Files:**
  * `mecharmory/core/service/dsl/lexer/imecha_lexer.py`
  * `mecharmory/core/service/dsl/lexer/mecha_lexer.py`
  * `mecharmory/core/service/dsl/parser/imecha_parser.py`
  * `mecharmory/core/service/dsl/parser/mecha_command_parser.py`
  * `mecharmory/core/service/dsl/parser/mecha_parser.py`
  * `mecharmory/core/service/dsl/linter/imecha_linter.py`
  * `mecharmory/core/service/dsl/linter/mecha_kinematic_bounds_checker.py`
  * `mecharmory/core/service/dsl/linter/mecha_linter.py`
  * `mecharmory/core/service/dsl/compiler/imecha_compiler.py`
  * `mecharmory/core/service/dsl/compiler/mecha_compiler.py`
  * `mecharmory/core/service/dsl/imecha_dsl_service.py`
  * `mecharmory/core/service/dsl/mecha_dsl_service.py`
* **Status:** Decomposed lexical, syntactic, semantic kinematic verification, and code generation stages adhering strictly to SRP, DIP, and $< 250$ line limits.

