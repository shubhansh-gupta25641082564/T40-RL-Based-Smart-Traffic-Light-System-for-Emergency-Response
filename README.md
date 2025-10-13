# RL-Based Smart Traffic Light System for Emergency Responses

## Cover

- **Project Title:** RL-Based Smart Traffic Light System for Emergency Responses
- **Team Name & ID:** Suraksha Squad (T40)
- **Institute / Course:** GLA University / B.Tech : CSE (AI/ML and IoT)
- **Version:** v0.1
- **Date:** 20 Aug, 2025

### Team Members
- Shubhansh Gupta — UR: 2315510204
- Rachit Gupta — UR: 2315510159
- Manas Kashyap — UR: 2315510114

**Mentor Name:** Prof. Yunis Ahmed Lone

***

## Revision History

| Version | Date         | Author            | Change             |
|---------|--------------|-------------------|--------------------|
| v0.1    | 20 Aug, 2025 | Shubhansh Gupta   | Initial Draft      |
| v0.5    | 30 Sep, 2025 | Suraksha Squad    | Half Project Done  |
| v1.0    | 31 Oct, 2025 | Suraksha Squad    | Full Project Done  |

***

## 1. Overview

- **Problem Statement:** Ambulances, fire trucks, and police cars frequently get stuck in heavy traffic, while civilian traffic is misregulated, causing long waits and traffic jams. This leads to longer emergency response times and commuter displeasure.
- **Goal:** Develop a traffic light control system using RL that detects and prioritizes emergency vehicles (ambulance, fire truck, police car) and manages civilian traffic flow to reduce long waits and jams, thus decreasing emergency response times.
- **Non-Goals:** Integrating GPS vehicle tracking, learning optimal signal patterns over time, reducing fuel wastage, predicting traffic flow, full city integration.
- **Value Proposition:** Demonstrates how AI can make city roads safer and greener by adaptively clearing intersections for emergency vehicles, improving response times and reducing travel and fuel delays.

***

## 2. Scope and Control

### 2.1 In-Scope
- RL-based control algorithm (Deep Q-Network/Policy Gradient)
- Simulation of urban traffic (SUMO or similar)
- GPS-based emergency vehicle detection logic
- Dynamic signal phase adjustment (RL & EV inputs)
- Backend/data logging (waiting times, queues)
- Simulated dashboard/API for traffic center

### 2.2 Out-of-Scope
- Physical hardware deployment
- Smartphone apps/in-car device development
- Multi-city/national scaling (prototype only)
- Advanced features: pedestrian, public transport, payment integration
- Highly detailed vehicle models (assume ideal sensor data)

### 2.3 Assumptions
- Simulated EVs broadcast GPS and priority status
- Realistic traffic demand patterns can be generated/sourced
- Simulation reflects urban traffic accurately
- Members (3×10hr/week) are available per schedule
- External libraries/tools function as expected

### 2.4 Constraints
- **Time:** 8 weeks (~2 months)
- **Resources:** Limited compute, minimal cloud/server use
- **Scope:** Focus on RL and detection, not full software engineering

### 2.5 Dependencies
- **Software:** SUMO, RL libraries, mapping/GPS APIs
- **Data:** Road network or synthetic scenarios
- **Hardware:** Compute for RL training, lab PCs for integration
- **Stakeholder Input:** Faculty mentor guidance

### 2.6 Acceptance Criteria
- **EMERGENCY PATH CLEARING:** Simulated ambulance triggers green light within seconds
- **TRAFFIC OPTIMIZATION:** RL reduces average queue length in heavy-flow scenarios
- **BALANCED DELAY:** Civilian delay increases when EV has right-of-way relative to baseline
- **SYSTEM INTEGRITY:** Simulation and logs complete, no crashes in trial

***

## 3. Stakeholders and RACI

**Stakeholders:** Suraksha Squad, Project Mentor, University Administration  
**Solution Benefits:** Emergency responders, public drivers

| Activity                | Responsible (R)         | Accountable (A)        | Consulted (C)             | Informed (I)    |
|-------------------------|------------------------|------------------------|---------------------------|-----------------|
| Requirements & Planning | Shubhansh Gupta        | Shubhansh Gupta        | Mentor                    | Team            |
| System Design (Algo/UI) | Team (Shubhansh, Rachit)| Shubhansh Gupta      | Mentor                    | Team            |
| RL Model Development    | Shubhansh Gupta        | Shubhansh Gupta        | Rachit Gupta, Mentor      | Team            |
| Simulation & Backend    | Rachit Gupta           | Rachit Gupta           | Manas Kashyap, Mentor     | Team            |
| Integration (RL + UI)   | Manas Kashyap          | Manas Kashyap          | Shubhansh, Rachit, Mentor | Team            |
| Testing & Validation    | Team                   | Shubhansh Gupta        | Mentor                    | Team            |
| Final Review & Delivery | Team, Suraksha Squad   | Mentor                 | Mentor                    |                 |

***

## 4. Team and Roles

| Member             | Role                | Responsibilities                                   | Key Skills                  | Availability (hr/week) | Contact                          |
|--------------------|---------------------|----------------------------------------------------|-----------------------------|-----------------------|-----------------------------------|
| Shubhansh Gupta    | RL Model Developer  | Define state/action space, rewards, train RL models| Python, TensorFlow/PyTorch, ML, SUMO | 15                | shubhansh.gupta_cs.aiml23@gla.ac.in |
| Rachit Gupta       | Full Stack Developer| Sim interface, detection logic, control APIs, dashboards| Node.js, Python, React, Databases | 15                | rachit.gupta_cs.aiml23@gla.ac.in |
| Manas Kashyap      | Integration Engineer| Integration of RL agent, coordinate modules, tests | Sys. integration, Python, APIs      | 15                | manas.kashyap_cs.aiml23@gla.ac.in |

***

## 5. Weekwise Plan and Assignments

- **Week 1:** Requirements & Architecture — RL problem definition, system architecture, assign tasks, initial design
- **Week 2:** Simulation Setup & Baseline — Intersection simulation, baseline fixed controller, EV detection
- **Week 3:** RL Agent Prototype — Basic RL agent, training, multi-lane simulation, metrics logging
- **Week 4:** EV Priority — RL rewards for EV clearance, simulation scenarios
- **Week 5:** Advanced Features — Traffic prediction, rerouting logic, performance metrics
- **Week 6:** Integration & UI — Final integration, dashboard/API, full-system tests
- **Week 7:** Testing & Optimization — Simulations, RL parameter tuning, bug fixes, graphs
- **Week 8:** Finalization & Demo — Demo-ready system, documentation, final synopsis, reporting

***

## 6. Users and UX

### 6.1 Personas
- Ambulance Driver — Needs quick, uninterrupted intersection passage
- Fire/Police Vehicle Operator — High priority in emergencies
- Traffic Control Operator — Monitors status, values reliability
- Civilian Driver — Wants reasonable travel, fairness
- Simulation Developer/Tester — Needs scenario control

### 6.2 Top User Journeys
- **Emergency Path Clearing:** Ambulance detected, green signals given, minimal stops
- **City Controller Monitoring:** Dashboard displays EVs and traffic, updates and anomalies manageable
- **Civilian Commuter:** Normal signals, red lights when EV approaches, reasonable detours

### 6.3 User Stories
- **Ambulance driver:** Wants intersections to turn green for quick emergency response (<3s processing delay)
- **Civilian driver:** Wants fair treatment, wait time within 20% of typical even with EV priority
- **Control operator:** Wants dashboard updates within 1s of EV event, real-time visibility

***

## 7. Market and Competitors

### 7.1 Competitors
- **Fixed-Time Controllers:** Simple, can't adapt to real-time/Emergency Vehicle (EV) needs
- **Adaptive Flow Systems:** Use sensors, improve average flow, weak EV handling
- **EV Preemption:** GPS/RFID trigger green lights, ignore congestion
- **Research Prototypes:** Academic RL approaches rarely combine EV priority

### 7.2 Positioning
- **Differentiator:** Combines real-time emergency detection and adaptive RL control for balanced EV & civilian prioritization

***

## 8. Objectives and Success Metrics

- **Minimize Emergency Response Time:** ≥30% reduction for EVs vs. fixed signals
- **Optimize Traffic Flow:** ≥15% better throughput/delay reduction
- **Fairness:** Non-EV delay doesn’t degrade >20% with EV priority
- **EV Detection Accuracy:** ≥99% correct detection rate
- **RL Convergence:** Stable agent performance after training
- **Fuel/Idle Reduction:** Less idle time than baseline

***

## 9. Key Features

- Adaptive RL-Based Scheduling (must)
- Real-Time Emergency Vehicle Detection (must)
- Dynamic Rerouting Support (should)
- Vehicle Queue Management (must)
- Predictive Traffic Analytics (could)
- Backend Communication with City Control (should)

***

## 10. Architecture

- **Traffic Simulation Environment:** Generates vehicle traffic, intersection modeling
- **Detection Module:** GPS-based EV identification
- **RL Signal Controller (Core Engine):** Receives state inputs, determines actions
- **Traffic Actuator:** Applies RL controller’s signal changes
- **City Traffic Control Interface:** Dashboard/logs for monitoring
- **Data Storage & Analytics:** Logs for analysis

**Workflow:**  
EV detected → Priority triggers → RL acts → Signal updates → Data logged

***

## 11. Data Design

- **Intersection Status:** {intersection_id, timestamp, phase, queue_lengths}
- **Vehicle Events:** {vehicle_id, type, position, speed, direction, timestamp}
- **RL Agent Logs:** {episode_id, step, state, action, reward}
- **Traffic Metrics:** {average delay, throughput, EV travel time}

***

## 12. Technical Workflow Diagrams

- State Transition Diagram
- Sequence Diagram
- Use Case Diagram
- Data Flow Diagram
- ER Diagram
- Technical Workflow Diagram
- Work Architecture Diagram

***

## 13. Quality (Non-Functional Requirements and Testing)

### 13.1 Non-Functional Requirements

| Metric                | Target/SLI                | Measurement              |
|-----------------------|---------------------------|--------------------------|
| Availability          | 99% uptime (simulation)   | Automated monitoring     |
| Real-Time Latency     | ≤1s after EV detection    | Log timestamp differences|
| Reliability           | 0% critical bugs          | Test environment         |
| EV Detection Accuracy | ≥99%                      | Compare detected vs actual|
| Throughput            | ≥ baseline (vehicles/hr)  | Simulation stats         |
| Security              | Secure comms (TLS)        | Assume SSL/TLS channels  |
| Logging Integrity     | 100% retention (7 days)   | Log completeness         |

### 13.2 Test Plan

- **RL Module:** Unit tests, coverage ≥80%, PyTest/TensorFlow, owner: Shubhansh
- **Detection/Integration:** Simulated scenarios, owner: Manas, must trigger within threshold
- **System Tests:** SUMO, key scenarios, metrics validation, owner: Team (Shubhansh & Rachit)
- **Performance Tests:** Latency in stress tests, owner: Rachit

### 13.3 Environments

- Development: Local, branch-controlled
- Staging: Integrated lab server
- Production/Demo: Final version on lab/cloud VM with simulation tools

***

## 14. Security and Compliance

### 14.1 Threat Model

| Asset          | Threat                  | STRIDE       | Mitigation                            | Owner    |
|----------------|------------------------|--------------|---------------------------------------|----------|
| Signal Cmds    | Tampering              | Tampering(T) | SSL/TLS, validate inputs              | Rachit   |
| EV detection   | Spoofed EV signal      | Spoofing(S)  | Authenticated GPS, ignore unrealistic | Rachit   |
| System Access  | Unauthorized changes   | Elev of Priv.| Restrict repo, strong credentials     | Manas    |

### 14.2 AuthN/AuthZ

- Only team members allowed code commits, traffic control interface secure for team use only

### 14.3 Audit and Logging

- All EV detections, signal changes, admin actions logged (timestamped), retention 2 weeks, simulation data only

### 14.4 Compliance

- Academic project only, follows University IT policy, no external user data, open source licenses respected

***

## 15. Delivery and Operations

### 15.1 Release Plan

- Milestone: v1.0 Demo by Week 8 (Nov 2)
- Internal Releases: Alpha (Week 3), Beta (Week 5)
- Each release with notes and mentor approval

### 15.2 CI/CD and Rollback

- Commits trigger automated tests and deployment to staging
- GitHub Actions/GitLab CI for automation
- Rollback via git tags/releases

### 15.3 Monitoring and Alerting

- Logs (queue length, response times) manually reviewed
- Alerts for latency/errors by watchdog script

### 15.4 Communication Plan

- Stand-ups: Mon/Wed/Fri video calls (15min)
- Weekly reports to mentor (Fri)
- Biweekly mentor demos (Week 4/8)

***

## 16. Risks and Mitigations

- **RL Training Instability:** Use simple scenarios, tune hyperparameters, curriculum learning
- **Simulation Fidelity:** Calibrate parameters, compare baselines
- **Time Overrun:** Prioritize core features, defer non-critical items, use open-source
- **Integration Bugs:** Integrate early, weekly end-to-end testing
- **Compute/Resource Limitations:** Use efficient algorithms, reduce space, cloud/minor GPU use

***

## 17. Evaluation Strategy and Success Metrics

- **Baseline Comparison:** Signals methods compared (fixed-time, heuristic, RL), metrics: EV time, delay, throughput
- **Stress Testing:** Edge cases (many EVs, peak congestion)
- **Success Benchmarks:** Meet/exceed targets, document RL benefits
- **Reporting:** Graphs/plots over episodes
- **Qualitative Feedback:** Domain expert review, lessons/limitations

**summary:**  
Success = Key goals met by quantitative gains and validation of EV prioritization without major impact to civilian flow.

***

## 18. Appendices

### 18.1 Glossary

- **RL:** Reinforcement Learning
- **EV:** Emergency Vehicle
- **MDP:** Markov Decision Process
- **DQN:** Deep Q-Network
- **GPS:** Global Positioning System
- **Throughput:** Vehicles passing intersection per period
- **Idle Time:** Vehicles stationary at red
- **SCOOT/SCATS:** Adaptive traffic signal systems
- **SUMO:** Simulation of Urban Mobility
- **ETA:** Estimated Time of Arrival

### 18.2 References

- Sutton, R.S. and Barto, A.G.: “Reinforcement Learning: An Introduction.” MIT Press, 2018.
- Khamis, A., et al.: “Intelligent Traffic Light Control System Using Reinforcement Learning.” J. Advanced Transportation, 2020.
- Van der Pol, E., & Oliehoek, F.: “Coordinated Deep RL for Traffic Light Control.” NIPS Workshop, 2016.
- SUMO Documentation — Simulation of Urban Mobility.
- Chen, Y., et al.: “Deep RL for Urban Traffic Light Control.” ICLR, 2019.
- Google Maps & GPS Technology.
- University lecture notes, CSE (AI/ML and IoT), GLA University

***
