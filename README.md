# 🚦 RL-Based Smart Traffic Light System for Emergency Responses 🚨

***

## 📝 Cover

- **Project Title:** RL-Based Smart Traffic Light System for Emergency Responses
- **Team Name & ID:** Suraksha Squad (T40)
- **Institute / Course:** GLA University / 🎓 B.Tech : CSE (AI/ML and IoT)
- **Version:** v0.1
- **Date:** 🗓️ 20 Aug, 2025

### 👥 Team Members
- 🧑‍💻 Shubhansh Gupta — UR: 2315510204
- 🧑‍💻 Rachit Gupta — UR: 2315510159
- 🧑‍💻 Manas Kashyap — UR: 2315510114

**Mentor Name:** 👨‍🏫 Prof. Yunis Ahmed Lone

***

## 📅 Revision History

| 🔢 Version | 🗓️ Date | ✍️ Author           | 🛠️ Change             |
|------------|---------|--------------------|-----------------------|
| v0.1       | 20 Aug, 2025 | Shubhansh Gupta | Initial Draft        |
| v0.5       | 30 Sep, 2025 | Suraksha Squad  | Half Project Done    |
| v1.0       | 31 Oct, 2025 | Suraksha Squad  | Full Project Done    |

***

## 1️⃣ Overview

- **Problem Statement:** 🚑🚒🚓 Emergency vehicles face delays due to heavy traffic, resulting in longer response times and commuter frustration.
- **Goal:** 🧠🤖 Use RL (Reinforcement Learning) to prioritize emergency vehicles and optimize civilian traffic flow.
- **Non-Goals:** 🚫 Integration with GPS, fuel optimization, large-scale city rollout, smarter learning patterns.
- **Value Proposition:** 🌱 Adaptive AI for safer and greener roads, reducing response times and improving travel efficiency.

***

## 2️⃣ Scope & Control

### 📍 In-Scope
- 🔬 RL algorithm (DQN / Policy Gradient)
- 🏙️ Traffic simulation (SUMO or similar)
- 🛰️ GPS-based emergency vehicle detection
- 🚦 Dynamic signal phase adjustment
- 📈 Backend data logging
- 📊 Simulated dashboard/API

### 🚫 Out-of-Scope
- 🧰 Physical hardware installation
- 📱 Mobile/in-car app development
- 🌏 Multi-city/national scaling
- 🚴‍♂️ Advanced intelligent models (pedestrian, payments)
- 🚗 Overly detailed vehicle modeling

### 📝 Assumptions
- 🚙 EVs broadcast GPS & priority status
- 📈 Realistic traffic generation
- 🕒 3×10hr/week per member

### ⏳ Constraints
- 🕗 Time: 8 weeks
- 💻 Limited compute
- 🧐 RL focus (not full SW engineering)

### 🤝 Dependencies
- 💾 SUMO, RL libraries
- 🗺️ Maps/road network data
- 🖥️ Lab PCs
- 👨‍🏫 Mentor input

### ✅ Acceptance Criteria
- 🚨 Emergency: Green light within seconds
- 🚦 RL: Queue reduction in heavy flow
- 🧑‍🤝‍🧑 Civilian: Delay balanced with EV priority
- 💪 System: Runs without crash/log issues

***

## 3️⃣ Stakeholders & RACI

**Stakeholders:** Suraksha Squad, Mentor, University  
**Solution Benefits:** 👮‍♂️ Emergency responders, 🚗 General public

| 📌 Activity               | 👨‍💻 Responsible | 🏅 Accountable | 💬 Consulted | 📢 Informed |
|--------------------------|------------------|---------------|-------------|------------|
| Requirements & Planning  | Shubhansh Gupta  | Shubhansh Gupta | Mentor    | Team       |
| Design (Algo/UI)         | Team             | Shubhansh Gupta | Mentor    | Team       |
| RL Model Development     | Shubhansh Gupta  | Shubhansh Gupta | Rachit, Mentor | Team  |
| Simulation/Backend       | Rachit Gupta     | Rachit Gupta    | Manas, Mentor | Team   |
| Integration              | Manas Kashyap    | Manas Kashyap   | Shubhansh, Rachit, Mentor | Team |
| Testing & Validation     | Team             | Shubhansh Gupta | Mentor    | Team       |
| Final Review & Delivery  | Team             | Mentor          | Mentor    | -          |

***

## 4️⃣ Team & Roles

| 👤 Member         | 🔧 Role               | 🏗️ Responsibilities             | 💡 Key Skills           | 🕐 Availability | 📧 Contact                        |
|-------------------|----------------------|---------------------------------|-------------------------|-----------------|------------------------------------|
| Shubhansh Gupta   | RL Dev               | RL agent, states, rewards       | Python, ML, SUMO        | 15 hr/week      | shubhansh.gupta_cs.aiml23@gla.ac.in|
| Rachit Gupta      | Full Stack Dev       | UI, detection, APIs, dashboard  | Node.js, React          | 15 hr/week      | rachit.gupta_cs.aiml23@gla.ac.in   |
| Manas Kashyap     | Integration Eng      | Module integration, tests       | APIs, Sys. Intg., Python| 15 hr/week      | manas.kashyap_cs.aiml23@gla.ac.in  |

***

## 5️⃣ Weekwise Plan

- 📅 Week 1: Req. & Arch. (design, assign, initial draft)
- 🏁 Week 2: Sim setup, baseline module, EV detection
- 🤖 Week 3: RL agent prototype, training, multi-lane, metrics
- 🚨 Week 4: EV clearance rewards, sim scenarios
- ⚙️ Week 5: Traffic prediction, rerouting, metrics
- 🖥️ Week 6: Integration, dashboard/API, tests
- 🧪 Week 7: Optimization, RL tuning, bugfixes, graphs
- 🎉 Week 8: Demo, docs, final submit/report

***

## 6️⃣ Users & UX

### 👤 Personas
- 🚑 Ambulance Driver
- 🚒 Fire/Police Operator
- 🏢 Traffic Control Operator
- 🚗 Civilian Driver
- 🧑‍💻 Sim Developer/Tester

### 🌈 Top Journeys
- 🚨 Emergency clearing: green signals, minimal stops
- 📺 Control center monitoring: dashboard updates
- 🚦 Civilian commuter: fairness in signals

### 🗣️ Key User Stories
- 🚑 Ambulance: intersection turns green within ≤3s
- 🚗 Civilian: wait never >20% more due to EV
- 🏢 Operator: dashboard updates within 1s

***

## 7️⃣ Market & Competitors

### 🏁 Main Competitors
- 🕒 Fixed-time controllers: no EV bias
- 📊 Adaptive Flow: sensors, poor EV handling
- 💾 EV preemption: GPS/RFID, can ignore congestion
- 👨‍🔬 Research prototypes: rarely combine RL/EV

### ⭐ Our Edge
- 🤝 Combines real-time emergency detection & adaptive RL for fairness and speed

***

## 8️⃣ Objectives & Success Metrics

- 🕑 Emergency response time ⬇️ ≥30% vs fixed signals
- 🚧 Flow optimization ⬆️ ≥15%
- 🧑‍🤝‍🧑 Fairness: civilian delay not >20% worse with EV priority
- 🎯 EV detection ≥99% accuracy
- 🧠 RL convergence: stable performance
- ⛽ Idle time/fuel wasted less than baseline

***

## 9️⃣ Key Features

- 🧠 RL scheduling (must)
- 🚨 Real-time EV detection (must)
- 🔄 Dynamic rerouting (should)
- ⏳ Queue management (must)
- 📈 Predictive analytics (could)
- 🌐 Backend link to city center (should)

***

## 🔗 Architecture

- 🏙️ Traffic simulation engine
- 🛰️ Detection module (GPS)
- 🤖 RL controller
- 🚦 Actuator (real-light control)
- 🖥️ Dashboard (control room)
- 💾 Data storage/logs

**System Flow:**  
EV detected ➡️ Priority triggers ➡️ RL acts ➡️ Signal updates ➡️ Data logged

***

## 📊 Data Design

- 🚥 Intersection: `{intersection_id, timestamp, phase, queue_lengths}`
- 🚗 Vehicle: `{vehicle_id, type, position, speed, direction, timestamp}`
- 🧠 RL logs: `{episode_id, step, state, action, reward}`
- 📈 Metrics: `{avg delay, throughput, EV time}`

***

## 🛠️ Technical Workflow Diagrams

- 🔄 State Transition
- ⏱️ Sequence
- 🧩 Use Case
- 🚦 Data Flow
- 📝 ER
- ⚙️ Architecture

***

## 🏆 Quality & Testing

### 📈 Non-Functional Requirements

| 📊 Metric             | 🎯 Target/SLI        | 🔍 Measurement         |
|-----------------------|---------------------|-----------------------|
| Availability          | 99% uptime          | Automated monitor     |
| Real-Time Latency     | ≤1s for EV events   | Log timestamps        |
| Reliability           | No critical bugs    | Test environment      |
| Detection Accuracy    | ≥99%                | Compare event logs    |
| Throughput            | ≥ baseline          | Sim stats             |
| Security              | SSL/TLS comms       | Channels assumed      |
| Logging Integrity     | 100%/7 days         | Logs                  |

### 🧪 Test Plan
- RL module: unit+coverage ≥80%
- Detection/Integration: sim scenarios
- System: SUMO, end-to-end
- Performance: latency under stress

### 🖥️ Environments
- Dev: local, branches
- Staging: lab server
- Demo: VM simulators

***

## 🛡️ Security & Compliance

### 🔍 Threat Model

| 🦾 Asset       | 🛑 Threat        | STRIDE | 🛡️ Mitigation          | 👤 Owner  |
|---------------|-----------------|--------|------------------------|-----------|
| Signal Cmds   | Tampering       | T      | SSL/TLS, validation    | Rachit    |
| EV detection  | Spoofed signal  | S      | Auth. GPS, checks      | Rachit    |
| System Access | Unauthorized    | E      | Repo restrict, creds   | Manas     |

- **Auth:** Only team commits, control panel secure
- **Audit:** All changes/events logged for 2 weeks
- **Policy:** Follows GLA IT guidelines, open source only, no external user data

***

## 📦 Delivery & Ops

- 🚀 Milestone: v1.0 Demo Week 8
- 🔁 Release: Alpha (W3) / Beta (W5)
- 📝 Approval: Mentor validated
- ⚡ CI/CD: GitHub Actions, Git rollback/tag
- 👀 Monitoring: Logs, error watch
- 🗣️ Communication: Mon/Wed/Fri stand-ups, weekly mentor reports

***

## ⚠️ Risks & Mitigation

- 🚨 RL instability: simple scenario, fine-tune
- 🏙️ Simulation: calibrate flow
- ⏳ Time overrun: prioritize core, defer extras
- 🛠️ Bugs: weekly E2E test/integration
- 💻 Compute: efficient algo, cloud if needed

***

## 🧮 Evaluation Strategy

- 🏁 Baseline vs RL: Compare signals
- 📊 Metrics: EV time, throughput, delay
- 🧪 Stress: multiple EV events
- 🏆 Benchmark: meet/exceed targets
- 📈 Visuals: graphs/plots/episodes
- 🗣️ Expert reviews, document limitations

> **Success = Real, measurable traffic improvements and fast EV priority!**

***

## 📚 Appendices

### Glossary

- RL: Reinforcement Learning
- EV: Emergency Vehicle
- MDP: Markov Decision Process
- DQN: Deep Q-Network
- GPS: Global Positioning System
- Throughput: Vehicles passing per time
- Idle Time: Vehicles at red
- SCOOT/SCATS: Adaptive signal systems
- SUMO: Urban traffic simulation
- ETA: Estimated Time of Arrival

### References

- Sutton & Barto: RL Introduction, MIT Press 2018
- Khamis et al.: RL Traffic Light, J. Advanced Transportation 2020
- Van der Pol & Oliehoek: RL for Traffic Light, NIPS Workshop 2016
- SUMO Documentation
- Chen et al.: Deep RL for Traffic, ICLR 2019
- Google Maps & GPS Tech
- GLA University, CSE AI/ML Lecture Notes
