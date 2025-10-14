# 🚦 RL-Based Smart Traffic Light System for Emergency Response

This document presents a comprehensive project synopsis for developing an intelligent traffic management system that prioritizes emergency vehicles while optimizing civilian traffic flow using reinforcement learning algorithms. The system represents a significant advancement in urban traffic control, combining artificial intelligence with real-time emergency response capabilities to create safer and more efficient city transportation networks.[1]

## 📋 Project Information

**🎓 Course:** B.Tech : CSE (AI/ML and IoT) (III YEAR – V SEM) (2025-2026)  
**🏛️ Department:** DEPARTMENT OF COMPUTER ENGINEERING & APPLICATIONS  
**🏫 Institution:** GLA University  
**📍 Address:** 17km Stone, NH-19, Mathura-Delhi Road P.O. Chaumuhan, Mathura – 281406 (Uttar Pradesh) India[1]

### 👥 Team Details

**🏆 Team Name:** Suraksha Squad (T40)  
**📋 Project Title:** RL-Based Smart Traffic Light System for Emergency Response

| 👤 Team Member | 🆔 University Roll |
|----------------|-------------------|
| Shubhansh Gupta | 2315510204 |
| Rachit Gupta | 2315510159 |
| Manas Kashyap | 2315510114 |

**👨‍🏫 Mentor:** Prof. Yunis Ahmed Lone[1]

### 📅 Version History

| 🔖 Version | 📅 Date | ✍️ Author | 🔄 Change |
|------------|---------|-----------|----------|
| v0.1 | 20 Aug, 2025 | Shubhansh Gupta | Initial Draft |
| v0.5 | 30 Sep, 2025 | Suraksha Squad | Half Project Done |
| v1.0 | 31 Oct, 2025 | Suraksha Squad | Full Project Done |

## 🌟 Project Overview

### 🚨 Problem Statement

Ambulances, fire trucks and police cars frequently get stuck in heavy traffic. Meanwhile, civilian traffic is mis regulated and results in long waits and traffic jams. This lack of synchronisation leads to longer emergency response times and levels of commuter disgruntlement.[1]

### 🎯 Goal

Develop a traffic light control system using RL that detects and gives priority to emergency vehicles (ambulances, fire trucks, police cars etc.) and also manages the civilian traffic flow to reduce long waits and traffic jams. This also reduces emergency response times.[1]

### ❌ Non-Goals

- Integrate with GPS tracking of vehicles
- Learn optimal signal patterns over time
- Reduce fuel wastage from idling
- Traffic flow prediction
- Integration with city control centers[1]

### 💎 Value Proposition

The proposed system will demonstrate how AI can make city roads both safer and greener. By adaptively clearing intersections for EVs, emergency responders reach destinations faster, while overall traffic delays drop. This means quicker medical assistance and firefighting on one hand, and lower commuter travel times and fuel use on the other. In simulation, we expect to show a marked reduction in EV travel time and improved average throughput, illustrating the benefits of learning-based control over static timing.[1]

## 🎯 Scope and Control

### ✅ In-Scope

- 🧠 Development of an RL-based control algorithm (e.g. Deep Q-Network or Policy Gradient) for traffic signals
- 🏙️ Simulation of urban traffic (e.g. using SUMO or similar), including vehicle agents and intersections
- 📍 GPS-based emergency vehicle detection logic in the simulation
- ⚡ Dynamic adjustment of signal phases in real time based on RL decisions and EV presence
- 📊 Backend/data logging to record traffic metrics (waiting times, queue lengths, EV travel times)
- 🌐 Connectivity to a "virtual" city traffic center (simulated dashboard/API) for monitoring[1]

### ❌ Out-of-Scope

- 🔧 Physical deployment on real traffic hardware
- 📱 Development of smartphone apps or in-car devices
- 🌍 National or multi-city scaling (only a prototype network)
- 🚶 Advanced features like pedestrian scheduling, public transport integration, or payment systems
- 🔬 Highly detailed vehicle models (we assume ideal sensor data)[1]

### 🔮 Assumptions

- 📡 Simulated emergency vehicles continuously broadcast location (GPS) and priority status
- 📈 Traffic demand patterns (vehicle arrival rates) can be generated or sourced realistically
- 🎯 The simulation environment reliably reflects key urban traffic dynamics
- 👥 Team members (3×10hr/week) are available as scheduled
- 🛠️ External libraries/tools (e.g. TensorFlow/PyTorch, SUMO, Node.js) function as expected[1]

### ⚠️ Constraints

- ⏰ **Time:** 8-week project duration (∼2 months)
- 💻 **Resources:** Limited compute for training (no industrial GPU). We may use university servers or cloud credits minimally
- 🎯 **Scope:** Focus on core RL and detection, not full-scale software engineering[1]

### 🔗 Dependencies

- 💻 **Software:** Traffic simulation framework (e.g. SUMO), RL libraries (TensorFlow/PyTorch), mapping/GPS APIs if needed
- 📊 **Data:** Road network map data or synthetic scenario generation
- 🖥️ **Hardware:** Compute resources for RL training; lab computers for integration
- 👨‍🏫 **Stakeholder input:** Guidance from faculty mentor[1]

### ✅ Acceptance Criteria (Signoff Scenarios)

- 🚑 **EMERGENCY PATH CLEARING:** GIVEN a simulated ambulance approaching an intersection, WHEN it enters the detection zone, THEN the light on its approach turns green within seconds of detection, and EV passes without halting
- 📊 **TRAFFIC OPTIMIZATION:** GIVEN a heavy-flow scenario (no EVs), WHEN the RL controller runs for some episodes, THEN the average queue length per intersection is overall decreased
- ⚖️ **BALANCED DELAY:** GIVEN simultaneous civilian and emergency vehicles, WHEN EV has right-of-way, THEN civilian delay increases by sufficient margin relative to baseline
- 🔧 **SYSTEM INTEGRITY:** GIVEN a full simulation with emergency and civilian traffic, WHEN the system runs a small trial for some minutes, THEN no software crashes occur and logs of EV events are complete[1]

## 👥 Stakeholders and RACI

**🤝 Stakeholders:** Suraksha Squad team members, Project Mentor (faculty advisor), and University administration. The RL solution ultimately serves emergency responders and drivers/public.[1]

| 📋 Activity | 👤 Responsible (R) | 📊 Accountable (A) | 💬 Consulted (C) | ℹ️ Informed (I) |
|-------------|-------------------|-------------------|------------------|-----------------|
| Requirements and planning | Shubhansh Gupta | Shubhansh Gupta | Mentor | Team |
| System Design (Algorithm / UI) | Team (Shubhansh, Rachit) | Shubhansh Gupta | Mentor | Team |
| RL Model Development | Shubhansh Gupta | Shubhansh Gupta | Rachit Gupta, Mentor | Team |
| Simulation & Backend Dev | Rachit Gupta | Rachit Gupta | Manas Kashyap, Mentor | Team |
| Integration (RL + Front-end) | Manas Kashyap | Manas Kashyap | Shubhansh, Rachit, Mentor | Team |
| Testing & Validation | Team | Shubhansh Gupta | Mentor | Team |
| Final Review & Delivery | Team | Suraksha Squad | Mentor | Mentor |

## 👨‍💻 Team and Roles

| 👤 Member | 🎭 Role | 📋 Responsibilities | 🛠️ Key Skills | ⏰ Availability (hr/week) | 📧 Contact |
|-----------|---------|-------------------|---------------|-------------------------|-----------|
| Shubhansh Gupta | 🧠 RL Model Developer | Define state/action space, design reward, train RL algorithms; simulate EV scenarios | Python, TensorFlow/PyTorch, ML, SUMO | 15 | shubhansh.gupta_cs.aiml23@gla.ac.in |
| Rachit Gupta | 💻 Full Stack Developer | Implement simulation interface, detection logic, control APIs; build dashboards | Node.js, Python, React, Databases | 15 | rachit.gupta_cs.aiml23@gla.ac.in |
| Manas Kashyap | 🔧 Integration Engineer | Integrate RL agent with simulation; coordinate modules; write test harnesses | System integration, Python, APIs | 15 | manas.kashyap_cs.aiml23@gla.ac.in |

## 📅 Weekwise Plan and Assignments

### 📅 Week 1 (Sep 8 – Sep 14): Requirements & Architecture
**🎯 Goals:** Define detailed requirements and RL problem (states, actions, rewards). Outline system architecture (interactions between GPS detection, RL agent, traffic lights).[1]

**📋 Tasks:**
- 👤 **Shubhansh:** drafts RL agent design
- 👤 **Rachit:** sets up base traffic simulation environment and mock GPS feed
- 👤 **Manas:** sketches integration points

**📦 Deliverables:** Requirement spec document, high-level design, initial simulation prototype[1]

### 📅 Week 2 (Sep 15 – Sep 21): Simulation Setup & Baseline
**🎯 Goals:** Build or configure an intersection simulation (e.g. one junction) with civilian traffic. Implement baseline fixed-time controller and simple EV-preemption rule for comparison.[1]

**📋 Tasks:**
- 👤 **Shubhansh:** codes environment interface for RL (defines traffic state representation)
- 👤 **Rachit:** implements EV detection trigger (simulated GPS input)
- 👤 **Manas:** tests end-to-end loop on one intersection

**📦 Deliverables:** Running simulation model, baseline controller, documented test scenarios[1]

### 📅 Week 3 (Sep 22 – Sep 28): RL Agent Prototype
**🎯 Goals:** Develop a basic RL agent (e.g. DQN) that controls traffic signals without EV logic. Train on simple scenarios.[1]

**📋 Tasks:**
- 👤 **Shubhansh:** implements and trains RL algorithm on small traffic patterns
- 👤 **Rachit:** extends simulation to multiple lanes
- 👤 **Manas:** begins logging metrics

**📦 Deliverables:** Trained RL model without EV priority, evaluation report (queue lengths, delays)[1]

### 📅 Week 4 (Sep 29 – Oct 5): Incorporate EV Priority
**🎯 Goals:** Modify RL reward to include EV clearance. Test EV scenarios.[1]

**📋 Tasks:**
- 👤 **Shubhansh:** updates reward function to heavily prioritize EV passage
- 👤 **Rachit:** ensures simulation generates EV vehicles and assigns priority flag
- 👤 **Manas:** integrates EV detection feed to RL agent

**📦 Deliverables:** Enhanced RL model with EV rewards, scenario demonstration (ambulance passes)[1]

### 📅 Week 5 (Oct 6 – Oct 12): Advanced Features
**🎯 Goals:** Add traffic flow prediction and dynamic rerouting logic. Implement a simple predictor (e.g. using historical sim data) to inform RL (optional) or route drivers around congested intersections when EV is incoming.[1]

**📋 Tasks:**
- 👤 **Shubhansh:** experiments with multi-step lookahead in RL
- 👤 **Rachit:** prototypes a rerouting module (e.g. Markov reroute)
- 👤 **Manas:** validates combined system

**📦 Deliverables:** Module for traffic prediction/rerouting, updated performance metrics[1]

### 📅 Week 6 (Oct 13 – Oct 19): System Integration & UI
**🎯 Goals:** Finalize integration of all components. Build a basic dashboard or logs for the virtual city traffic control center to view system status.[1]

**📋 Tasks:**
- 👤 **Rachit:** creates a simple web UI or data API for control center
- 👤 **Manas:** conducts full-system tests
- 👤 **Shubhansh:** refines RL training for stability

**📦 Deliverables:** Integrated end-to-end system, user interface prototype, midterm demo[1]

### 📅 Week 7 (Oct 20 – Oct 26): Testing & Optimization
**🎯 Goals:** Run extensive simulations to evaluate performance under varied conditions (different traffic volumes, EV arrival rates). Tune RL parameters for reliability.[1]

**📋 Tasks:** All team members run experiments and collect data
- 👤 **Shubhansh:** optimizes model parameters
- 👤 **Rachit and Manas:** identify and fix bugs

**📦 Deliverables:** Test report with graphs (EV response time, average delay), bug fix log[1]

### 📅 Week 8 (Oct 27 – Nov 2): Finalization & Demo
**🎯 Goals:** Prepare final demonstration and report. Conduct a full demo to mentor (including scenarios with multiple EVs).[1]

**📋 Tasks:** Finalize code, write user manual, polish slides and documentation

**📦 Deliverables:** Demo-ready system (v1.0), slide deck, final synopsis[1]

**📝 Note:** Weekly status updates will be shared with the mentor, and code/version control (Git) will be used throughout.[1]

## 👥 Users and UX

### 🎭 Personas

- 🚑 **Ambulance Driver (Emergency Responder):** Needs quick, uninterrupted passage through intersections. Values speed and reliability
- 🚒 **Fire/Police Vehicle Operator:** Similar needs as ambulance, with highest priority in certain scenarios
- 🎛️ **Traffic Control Center Operator:** Monitors city traffic; needs visibility into intersection status and EV movements. Values system reliability and interpretability
- 🚗 **Civilian Driver:** Typical commuter. Wants reasonable travel times and fairness (not feeling "stuck" for too long)
- 🧪 **Simulation Developer/Tester:** (Internal) Uses system to test scenarios. Values control over simulation parameters[1]

### 🛣️ Top User Journeys

#### 🚑 Emergency Vehicle (Path Clearing)
An ambulance is dispatched and enters the simulation. The detection module identifies it via GPS. The RL controller immediately gives green signals along its route while holding cross-traffic. The ambulance smoothly traverses multiple intersections with minimal stops, arriving faster.[1]

#### 🎛️ City Controller Monitoring
The city operator views a dashboard. When an emergency event occurs, they see the EV's location and system status. They may overlay predicted traffic flow and review signal adjustments. In case of anomalies, they can pause or adjust the simulation.[1]

#### 🚗 Civilian Commuter
A driver on route sees normal signal operation. If an EV approaches a nearby intersection, they might see lights change to red earlier than expected. The system ensures that civilian detours remain reasonable, and traffic flow does not collapse.[1]

### 📖 User Stories

#### 🚑 Emergency Vehicle Priority
> **"As an ambulance driver, I want approaching intersections to turn green for me, so that I reach patients as fast as possible."**

**GIVEN** an emergency vehicle is detected 100 m from an intersection, **WHEN** it is 5 s from the stop line, **THEN** the corresponding traffic light turns green (and conflicting lights turn red) with ≤3 s of processing delay.[1]

#### ⚖️ Civilian Fairness
> **"As a civilian driver, I want fair treatment during emergencies, so my wait doesn't become excessive."**

**GIVEN** both an ambulance and a civilian vehicle are queued at an intersection, **WHEN** the ambulance is given priority, **THEN** the civilian will be released by the next green cycle, and its wait time remains within 20% of typical.[1]

#### 🎛️ Traffic Control Monitoring
> **"As a traffic control operator, I want real-time insights into traffic and emergencies, so I can trust the system."**

**GIVEN** the system is running, **WHEN** an EV event occurs, **THEN** the dashboard updates within 1 s with EV status and planned signal changes.[1]

*(Accessibility & localization are minimal since this is a simulation interface used by technical staff; interface will be in English with standard UI controls.)*[1]

## 🏪 Market and Competitors

### 🏭 Competitors

#### ⏰ Fixed-Time Controllers
Pre-programmed cycles (e.g. green/yellow/red patterns)
- **💪 Strength:** Simple, widely used
- **⚠️ Weakness:** Cannot adapt to real-time conditions or EVs at all[1]

#### 📊 Adaptive Flow Systems (e.g. SCOOT, SCATS)
Adjust signal timing based on sensors/traffic detectors
- **💪 Strength:** Improve average flow
- **⚠️ Weakness:** Do not specifically expedite emergency vehicles[1]

#### 🚨 Emergency Vehicle Preemption (GPS/RFID-based)
Specialized devices allow EVs to trigger green lights on approach
- **💪 Strength:** EVs get quick passage
- **⚠️ Weakness:** Typically ignore overall congestion – often causing backups elsewhere[1]

#### 🔬 Research Prototypes
Several academic RL projects exist for traffic lights, but few integrate EV priority. For example, some use deep learning for urban signal control, but usually focus on congestion broadly.[1]

### 🎯 Positioning

#### 🌟 Our Differentiator
We combine real-time emergency detection with adaptive RL control. The system not only gives right-of-way to EVs but learns over time to do so without crippling civilian traffic. In contrast to static preemption, our solution continuously optimizes for both objectives. In summary, no existing product fully unites RL optimization with emergency prioritization in the way we propose.[1]

## 🎯 Objectives and Success Metrics

### 🚑 O1: Minimize Emergency Response Time
- **🎯 Target:** ≥30% reduction in average travel time for emergency vehicles compared to fixed signals
- **📊 KPI:** Average EV travel time (seconds) in simulation[1]

### 📊 O2: Optimize Traffic Flow
- **🎯 Target:** ≥15% improvement in average throughput (vehicles/hour) or similar reduction in overall delay
- **📊 KPI:** Average delay per non-EV vehicle (seconds)[1]

### ⚖️ O3: Fairness Between EV and Civilian Traffic
- **🎯 Target:** Ensure non-emergency average delay does not degrade more than 20% when EVs are prioritized
- **📊 KPI:** Ratio of delay (with EV priority) / (delay baseline)[1]

### 🎯 O4: EV Detection Accuracy
- **🎯 Target:** ≥99% of simulated EVs are correctly detected by GPS module
- **📊 KPI:** EV detection success rate[1]

### 🧠 O5: RL Convergence
- **🎯 Target:** Agent reaches stable performance (e.g. converged reward) within set episodes
- **📊 KPI:** Reward stability (variance) after training[1]

### ⛽ O6: Fuel/Idle Reduction
- **🎯 Target:** Measurable reduction in total vehicle idle time (e.g. minutes) compared to baseline, which correlates to fuel savings
- **📊 KPI:** Total idle time or fuel usage estimate[1]

These will be measured during simulation experiments. For instance, prior work shows RL can improve "transport efficiency" and sustainability significantly, setting a benchmark for our targets.[1]

## ⭐ Key Features

### 🧠 Adaptive RL-Based Scheduling (Must)
The core feature. The system's RL agent observes current traffic state (queue lengths, EV presence) and decides signal phases adaptively.
- **✅ Acceptance:** In simulation trials, the RL controller must produce lower average delay than a fixed schedule under identical traffic inputs[1]

### 📡 Real-Time Emergency Vehicle Detection (Must)
Simulated GPS signals identify EVs. The system must recognize an EV's approach instantly.
- **✅ Acceptance:** GIVEN an EV enters detection range, the system marks it as high-priority within 1 s, and triggers priority logic[1]

### 🗺️ Dynamic Rerouting Support (Should)
If an EV's path is blocked by congestion, the system suggests alternative routes to following vehicles.
- **✅ Acceptance:** GIVEN a congested path ahead, WHEN EV is en route, THEN backup routes are computed so that EV ETA is reduced (compared to no reroute)[1]

### 🚗 Vehicle Queue Management (Must)
The controller manages queues fairly. Civilian vehicles are queued if needed, and EV queues are cleared first.
- **✅ Acceptance:** GIVEN simultaneous queues, WHEN EV is present, THEN EV-facing lights turn green while queuing civilians do not exceed acceptable wait times[1]

### 🔮 Predictive Traffic Analytics (Could)
The system analyzes past traffic flow to forecast congestion (e.g. using a simple LSTM or statistical model) and adjusts RL training or routing.
- **✅ Acceptance:** The predictive model achieves reasonable accuracy (e.g. 85% hit rate) on simulated flow, improving decision-making efficiency[1]

### 🌐 Backend Communication with City Control (Should)
Bi-directional data interface with a traffic center.
- **✅ Acceptance:** The simulation logs and dashboard update in real time (≤2 s lag) with traffic stats and EV events, enabling oversight[1]

Each feature's implementation will rely on key dependencies (RL framework, simulation, mapping API). For example, scheduling depends on a trained neural network; detection depends on simulated GPS feeds. We will use acceptance tests as in Section 2 to verify each feature.[1]

## 🏗️ Architecture

The system follows a modular architecture:

### 🏙️ Traffic Simulation Environment
A virtual city/intersection simulation (e.g. SUMO) generates vehicle traffic (both civilian and EV). Road network and vehicle behaviors (speeds, routes) are modeled here.[1]

### 📡 Detection Module
Simulated GPS data from vehicles is processed to identify emergency vehicles. Detected EVs send priority flags to the controller.[1]

### 🧠 RL Signal Controller (Core Engine)
Implements the RL agent. It receives state inputs (current light states, queue lengths, detected EVs) and outputs actions (which direction to green-light next). The agent may run on a loop of state→action→environment update.[1]

### 🚦 Traffic Actuator
Interface to the simulation's traffic lights. It applies the RL controller's decisions by changing the signals in the simulation.[1]

### 🎛️ City Traffic Control Interface
A backend/dashboard that collects data (logs of events, traffic metrics) and allows operators to monitor or optionally override (e.g. emergency override).[1]

### 📊 Data Storage & Analytics
Logs events (timestamped state/action/reward) for analysis. Could be a simple database or log files.[1]

### 🔄 Workflow
An example sequence is: EV enters road → detection module flags EV → RL controller (in response) sets signal to green for EV → actuator changes light → vehicle moves → traffic state updates (feedback to RL). Another flow: regular traffic updates cycle, and RL agent optimizes throughput if no EV present.[1]

## 📊 Data Design

We will log key data elements for each simulation run:

### 🚦 Intersection Status
**📋 Attributes:** {intersection_id, timestamp, current_phase, queue_lengths}[1]

### 🚗 Vehicle Events
**📋 Attributes:** {vehicle_id, type (civilian/ambulance/fire/police), position, speed, direction, timestamp}. EVs have priority_flag = true[1]

### 🧠 RL Agent Logs
**📋 Attributes:** {episode_id, step, state_representation, action_taken, reward}[1]

### 📊 Traffic Metrics
Summarized data per run: average delay, throughput, EV travel times[1]

Data will be stored in CSV or simple tables. No personal/sensitive information is used (only simulated vehicle IDs). Backup logs nightly; ensure ability to reproduce scenarios from recorded seed values.[1]

## 📈 Technical Workflow Diagrams

### 🔄 State Transition Diagram
*[Diagram placeholder - refer to original document]*[1]

### 📊 Sequence Diagram
*[Diagram placeholder - refer to original document]*[1]

### 👥 Use Case Diagram
*[Diagram placeholder - refer to original document]*[1]

### 🌊 Data Flow Diagram
*[Diagram placeholder - refer to original document]*[1]

### 🗂️ ER Diagram
*[Diagram placeholder - refer to original document]*[1]

### ⚙️ Technical Workflow Diagram
*[Diagram placeholder - refer to original document]*[1]

### 🏗️ Work Architecture Diagram
*[Diagram placeholder - refer to original document]*[1]

## 🔍 Quality (Non-Functional Requirements and Testing)

### 📊 Non-Functional Requirements

| 📊 Metric | 🎯 SLI / Target | 📏 Measurement |
|-----------|----------------|----------------|
| ⏱️ Availability | 99% uptime in simulation runs | Automated uptime monitoring |
| ⚡ Real-Time Latency | Decision ≤1 s after EV detection | Log timestamp differences |
| 🔧 Reliability | No critical bugs (0% crashes) | Pass/fail in test environment |
| 🎯 EV Detection Accuracy | ≥99% | Compare detected vs actual EVs |
| 📊 Throughput | Maintain ≥ baseline | Vehicles/hour (simulation stats) |
| 🔒 Security | Secure channels (TLS) | (Assume secure communication) |
| 📝 Logging Integrity | 100% event logging retention (7 days) | Log completeness check |

### 🧪 Test Plan

#### 🧠 RL Module (Unit Tests)
Test individual functions – state encoding, reward calculation, neural network outputs
- **🛠️ Tool:** PyTest/TensorFlow tests
- **👤 Owner:** Shubhansh (Coverage ≥80%)
- **🚪 Exit:** All critical assertions pass, no errors[1]

#### 🔗 Detection/Integration (Integration Tests)
Simulate EV approach and verify detection→priority pipeline
- **🛠️ Tool:** Custom simulation scenarios, Postman for APIs
- **👤 Owner:** Manas (100% of EV cases)
- **🚪 Exit:** EVs always trigger priority within timing threshold[1]

#### 🌐 System (End-to-End Tests)
Run full simulation with mixed traffic
- **🛠️ Tool:** SUMO or custom scenario runner
- **👤 Owner:** Team (Shubhansh & Rachit)
- **📊 Coverage:** Key scenarios (rush hour, random EVs) complete
- **🚪 Exit:** Metrics (delay, EV time) meet acceptance criteria[1]

#### ⚡ Performance Tests
Measure latency of controller decisions under load
- **🛠️ Tool:** Logging, APM
- **👤 Owner:** Rachit
- **🚪 Exit:** Latency stays within SLAs in stress tests[1]

### 🌍 Environments

- **💻 Development:** Each member runs code locally with lightweight simulator, controlled branch on GitHub
- **🔧 Staging:** Central integration environment (e.g. lab server) where combined system is deployed for testing
- **🚀 Production/Demo:** Final version on lab machine or cloud VM with necessary simulation tools[1]

Feature flags will control experimental features; rollbacks are managed via version control.[1]

## 🔐 Security and Compliance

### ⚠️ Threat Model

| 🛡️ Asset | 🚨 Threat | 📊 STRIDE (Category) | 🔧 Mitigation | 👤 Owner |
|-----------|-----------|---------------------|---------------|----------|
| Signal Commands | Tampering with commands | Tampering (T) | Use SSL/TLS for control messages; validate inputs | Rachit |
| EV detection data | Spoofed EV signal (false flag) | Spoofing (S) | Assume authenticated GPS feed; ignore unrealistic inputs | Rachit |
| System Access | Unauthorized code changes | Elevation of Privilege (E) | Restrict repository access, use strong credentials | Manas |

### 🔐 AuthN / AuthZ
Only team members have commit access to code repositories. No public user accounts are needed. The traffic control interface (if web-based) will be secured for team use only.[1]

### 📋 Audit and Logging
All EV detections, signal changes, and admin actions are logged with timestamps. Logs are retained for 2 weeks for analysis. No real personal data is used. Logs contain only simulated vehicle data. Compliance with university data policy is ensured (no third-party data collection or sharing).[1]

### 📜 Compliance
This is an academic project; it follows GLA University's IT policy. No external user data is involved, and no known regulatory compliance (e.g. GDPR) applies here. We will cite all incorporated third-party code and respect open-source licenses.[1]

## 🚀 Delivery and Operations

### 📅 Release Plan

#### 🎯 Milestone
v1.0 Demo by end of Week 8 (Nov 2)[1]

#### 🔄 Internal Releases
- **🅰️ Alpha by Week 3** (basic RL without EV logic)
- **🅱️ Beta by Week 5** (with EV integration)[1]

Each release will have release notes summarizing features and any outstanding issues. The mentor will approve progression to the next stage.[1]

### 🔄 CI/CD and Rollback

#### 🔧 CI/CD Pipeline
Commits to main trigger automated tests (unit and integration). Passing builds are deployed to the staging environment nightly.[1]

#### 🛠️ Tools
GitHub Actions (or GitLab CI) for linting, testing, and packaging.[1]

#### ↩️ Rollback
Use Git tags/releases. If a build fails validation, revert to the previous tag and debug.[1]

### 📊 Monitoring and Alerting
In simulation, monitoring is minimal. We will log key metrics (queue lengths, EV response times) and manually review them. If latency or errors spike, alerts (e.g. email to team) are triggered by a simple watchdog script.[1]

### 📢 Communication Plan

- **🗣️ Stand-ups:** Brief (15-min) video calls every Monday/Wednesday/Friday to sync progress
- **📄 Weekly Reports:** Summary of achievements and issues submitted to mentor each Friday
- **👨‍🏫 Mentor Meetings:** Biweekly demos (end of Week 4 and Week 8) to present prototypes and gather feedback[1]

## ⚠️ Risks and Mitigations

### 🧠 RL Training Instability
- **⚠️ Risk:** The agent may not converge or may converge to suboptimal policies
- **🛡️ Mitigation:** Start with simple scenarios; tune hyperparameters; if needed, use tried-and-true algorithms (e.g. DQN) and curriculum learning (gradually increase complexity)[1]

### 🎮 Insufficient Simulation Fidelity
- **⚠️ Risk:** Simulation may not reflect real traffic complexities
- **🛡️ Mitigation:** Calibrate parameters (e.g. arrival rates) using standard distributions; compare baseline system performance to known benchmarks[1]

### ⏰ Time Overrun
- **⚠️ Risk:** 30 hours/week may be too little for all tasks
- **🛡️ Mitigation:** Prioritize core features (EV priority + RL); defer non-critical features (e.g. advanced UI) if behind schedule. Use open-source modules to save time[1]

### 🔗 Integration Bugs
- **⚠️ Risk:** Modules (RL, detection, UI) may not interface smoothly
- **🛡️ Mitigation:** Integrate early and incrementally. Allocate time each week for end-to-end testing[1]

### 💻 Compute/Resource Limitations
- **⚠️ Risk:** Training deep RL could be slow on available hardware
- **🛡️ Mitigation:** Use efficient algorithms, reduce state/action space if needed, or leverage cloud credits/minor GPU access for heavy runs[1]

Risk severity will be tracked weekly and addressed by adjusting scope or plan as needed.[1]

## 📊 Evaluation Strategy and Success Metrics

We will evaluate the system primarily via simulation experiments:

### 📈 Baseline Comparison
Run the same traffic scenario with (a) fixed-time signals, (b) heuristic EV preemption, and (c) our RL controller. Compare metrics: Average EV travel time, Average civilian delay, Total vehicles served, and Total idle time.[1]

### 🔥 Stress Testing
Test edge cases, e.g. many simultaneous EVs, peak-hour congestion, to ensure stability.[1]

### 🎯 Success Benchmarks
Meet or exceed the targets set in Section 8. For example, demonstrating that EV travel time under RL is significantly lower than baseline, and that throughput is not sacrificed.[1]

### 📊 Reporting
Prepare plots of key metrics over time/episodes. Document scenarios where RL provides clear benefits.[1]

### 💭 Qualitative Feedback
If possible, have a domain expert (e.g. traffic engineer) review the approach. Include lessons and limitations in the final report.[1]

In summary, success is measured by achieving the key goals with quantitative gains (as informed by literature) and validating that emergency vehicles indeed receive priority without critically harming normal traffic flow.[1]

## 📚 Appendices

### 📖 Glossary

- **🧠 RL (Reinforcement Learning):** A type of machine learning where an agent learns optimal actions by interacting with an environment and receiving rewards/penalties
- **🚨 EV (Emergency Vehicle):** Special vehicles like ambulances, fire trucks, and police cars that require immediate right-of-way
- **🔄 MDP (Markov Decision Process):** A mathematical framework used to model decision-making in RL problems
- **🧠 DQN (Deep Q-Network):** A reinforcement learning algorithm that uses neural networks to approximate Q-values
- **📍 GPS (Global Positioning System):** Satellite-based system used to detect vehicle locations
- **📊 Throughput:** Number of vehicles passing through an intersection in a given period
- **⏰ Idle Time:** Duration for which vehicles remain stationary at a red light
- **🔧 SCOOT/SCATS:** Existing adaptive traffic signal systems used in real cities
- **🏙️ SUMO (Simulation of Urban Mobility):** An open-source traffic simulation software
- **⏰ ETA (Estimated Time of Arrival):** Predicted arrival time of a vehicle at a destination[1]

### 📚 References

- Sutton, R.S. and Barto, A.G. Reinforcement Learning: An Introduction. MIT Press, 2018
- Khamis, A., et al. "Intelligent Traffic Light Control System Using Reinforcement Learning." Journal of Advanced Transportation, 2020
- Van der Pol, E., & Oliehoek, F. "Coordinated Deep Reinforcement Learners for Traffic Light Control." NIPS Workshop on Learning, Inference and Control of Multi-Agent Systems, 2016
- SUMO Documentation – Simulation of Urban Mobility. Available: https://www.eclipse.org/sumo/
- Chen, Y., et al. "Deep Reinforcement Learning for Urban Traffic Light Control." ICLR, 2019
- Google Maps & GPS Technology – Vehicle location and routing references
- University lecture notes and course material from CSE (AI/ML and IoT), GLA University
