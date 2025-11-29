// Traffic Simulation Data
let simulationRunning = true;
let vehicles = [];
let emergencyVehicles = [];
let trafficLights = {
  north: 'red',
  south: 'green',
  east: 'red',
  west: 'green'
};

// Chart instances
let queueChart, distributionChart, delayChart, responseChart, rewardChart;

// Initialize the dashboard
function initDashboard() {
  initCharts();
  initIntersection();
  initEmergencyVehicles();
  initSystemLogs();
  initControls();
  startSimulation();
}

// Initialize all charts
function initCharts() {
  // Queue Length Chart
  const queueCtx = document.getElementById('queueChart').getContext('2d');
  queueChart = new Chart(queueCtx, {
    type: 'line',
    data: {
      labels: ['00:00', '00:10', '00:20', '00:30', '00:40', '00:50', '01:00'],
      datasets: [
        {
          label: 'North',
          data: [12, 15, 10, 8, 14, 11, 9],
          borderColor: '#1FB8CD',
          backgroundColor: 'rgba(31, 184, 205, 0.1)',
          tension: 0.4,
          fill: true
        },
        {
          label: 'South',
          data: [8, 10, 13, 11, 7, 9, 12],
          borderColor: '#FFC185',
          backgroundColor: 'rgba(255, 193, 133, 0.1)',
          tension: 0.4,
          fill: true
        },
        {
          label: 'East',
          data: [15, 12, 14, 16, 13, 15, 14],
          borderColor: '#B4413C',
          backgroundColor: 'rgba(180, 65, 60, 0.1)',
          tension: 0.4,
          fill: true
        },
        {
          label: 'West',
          data: [10, 8, 7, 9, 11, 8, 10],
          borderColor: '#5D878F',
          backgroundColor: 'rgba(93, 135, 143, 0.1)',
          tension: 0.4,
          fill: true
        }
      ]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: {
          display: true,
          position: 'top'
        },
        tooltip: {
          mode: 'index',
          intersect: false
        }
      },
      scales: {
        y: {
          beginAtZero: true,
          title: {
            display: true,
            text: 'Queue Length'
          }
        }
      }
    }
  });

  // Traffic Distribution Chart
  const distCtx = document.getElementById('distributionChart').getContext('2d');
  distributionChart = new Chart(distCtx, {
    type: 'pie',
    data: {
      labels: ['North', 'South', 'East', 'West'],
      datasets: [{
        data: [28, 24, 30, 18],
        backgroundColor: ['#1FB8CD', '#FFC185', '#B4413C', '#5D878F']
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: {
          position: 'bottom'
        },
        tooltip: {
          callbacks: {
            label: function(context) {
              return context.label + ': ' + context.parsed + '%';
            }
          }
        }
      }
    }
  });

  // Delay Chart
  const delayCtx = document.getElementById('delayChart').getContext('2d');
  delayChart = new Chart(delayCtx, {
    type: 'bar',
    data: {
      labels: ['North', 'South', 'East', 'West'],
      datasets: [{
        label: 'Average Delay (seconds)',
        data: [45, 38, 52, 41],
        backgroundColor: ['#1FB8CD', '#FFC185', '#B4413C', '#5D878F']
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: {
          display: false
        }
      },
      scales: {
        y: {
          beginAtZero: true,
          title: {
            display: true,
            text: 'Delay (seconds)'
          }
        }
      }
    }
  });

  // Response Time Chart
  const responseCtx = document.getElementById('responseChart').getContext('2d');
  responseChart = new Chart(responseCtx, {
    type: 'line',
    data: {
      labels: ['Episode 1', 'Episode 5', 'Episode 10', 'Episode 15', 'Episode 20'],
      datasets: [
        {
          label: 'Baseline System',
          data: [120, 120, 120, 120, 120],
          borderColor: '#B4413C',
          backgroundColor: 'rgba(180, 65, 60, 0.1)',
          tension: 0.4,
          borderDash: [5, 5]
        },
        {
          label: 'RL System',
          data: [120, 95, 78, 65, 52],
          borderColor: '#1FB8CD',
          backgroundColor: 'rgba(31, 184, 205, 0.1)',
          tension: 0.4,
          fill: true
        }
      ]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: {
          display: true,
          position: 'top'
        }
      },
      scales: {
        y: {
          beginAtZero: true,
          title: {
            display: true,
            text: 'Response Time (seconds)'
          }
        }
      }
    }
  });

  // Reward Chart
  const rewardCtx = document.getElementById('rewardChart').getContext('2d');
  const rewardData = [];
  for (let i = 0; i <= 450; i += 10) {
    rewardData.push({
      x: i,
      y: Math.min(8750, 100 + i * 18 + Math.random() * 200)
    });
  }
  
  rewardChart = new Chart(rewardCtx, {
    type: 'line',
    data: {
      datasets: [{
        label: 'Cumulative Reward',
        data: rewardData,
        borderColor: '#1FB8CD',
        backgroundColor: 'rgba(31, 184, 205, 0.1)',
        tension: 0.4,
        fill: true,
        pointRadius: 0
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: {
          display: false
        }
      },
      scales: {
        x: {
          type: 'linear',
          title: {
            display: true,
            text: 'Episodes'
          }
        },
        y: {
          beginAtZero: true,
          title: {
            display: true,
            text: 'Reward'
          }
        }
      }
    }
  });
}

// Initialize intersection visualization
function initIntersection() {
  const canvas = document.getElementById('intersectionCanvas');
  canvas.innerHTML = `
    <svg width="100%" height="100%" viewBox="0 0 600 500" style="background-color: var(--color-bg-1);">
      <!-- Roads -->
      <rect x="250" y="0" width="100" height="500" fill="rgba(100, 100, 100, 0.3)"/>
      <rect x="0" y="200" width="600" height="100" fill="rgba(100, 100, 100, 0.3)"/>
      
      <!-- Road markings -->
      <line x1="300" y1="0" x2="300" y2="195" stroke="rgba(255, 255, 255, 0.5)" stroke-width="2" stroke-dasharray="10,10"/>
      <line x1="300" y1="305" x2="300" y2="500" stroke="rgba(255, 255, 255, 0.5)" stroke-width="2" stroke-dasharray="10,10"/>
      <line x1="0" y1="250" x2="245" y2="250" stroke="rgba(255, 255, 255, 0.5)" stroke-width="2" stroke-dasharray="10,10"/>
      <line x1="355" y1="250" x2="600" y2="250" stroke="rgba(255, 255, 255, 0.5)" stroke-width="2" stroke-dasharray="10,10"/>
      
      <!-- Intersection -->
      <rect x="250" y="200" width="100" height="100" fill="rgba(150, 150, 150, 0.3)"/>
      
      <!-- Traffic Lights -->
      <g id="lightNorth">
        <rect x="340" y="180" width="20" height="50" rx="5" fill="rgba(50, 50, 50, 0.8)"/>
        <circle id="lightNorthRed" cx="350" cy="195" r="6" fill="#dc2626" opacity="0.3"/>
        <circle id="lightNorthYellow" cx="350" cy="210" r="6" fill="#ca8a04" opacity="0.3"/>
        <circle id="lightNorthGreen" cx="350" cy="225" r="6" fill="#16a34a" opacity="0.3"/>
      </g>
      
      <g id="lightSouth">
        <rect x="240" y="270" width="20" height="50" rx="5" fill="rgba(50, 50, 50, 0.8)"/>
        <circle id="lightSouthRed" cx="250" cy="285" r="6" fill="#dc2626" opacity="0.3"/>
        <circle id="lightSouthYellow" cx="250" cy="300" r="6" fill="#ca8a04" opacity="0.3"/>
        <circle id="lightSouthGreen" cx="250" cy="315" r="6" fill="#16a34a" opacity="0.3"/>
      </g>
      
      <g id="lightEast">
        <rect x="370" y="240" width="50" height="20" rx="5" fill="rgba(50, 50, 50, 0.8)"/>
        <circle id="lightEastRed" cx="385" cy="250" r="6" fill="#dc2626" opacity="0.3"/>
        <circle id="lightEastYellow" cx="400" cy="250" r="6" fill="#ca8a04" opacity="0.3"/>
        <circle id="lightEastGreen" cx="415" cy="250" r="6" fill="#16a34a" opacity="0.3"/>
      </g>
      
      <g id="lightWest">
        <rect x="180" y="240" width="50" height="20" rx="5" fill="rgba(50, 50, 50, 0.8)"/>
        <circle id="lightWestRed" cx="195" cy="250" r="6" fill="#dc2626" opacity="0.3"/>
        <circle id="lightWestYellow" cx="210" cy="250" r="6" fill="#ca8a04" opacity="0.3"/>
        <circle id="lightWestGreen" cx="225" cy="250" r="6" fill="#16a34a" opacity="0.3"/>
      </g>
      
      <!-- Vehicles will be added dynamically -->
      <g id="vehiclesContainer"></g>
    </svg>
  `;
  
  updateTrafficLights();
}

// Update traffic lights
function updateTrafficLights() {
  const directions = ['north', 'south', 'east', 'west'];
  directions.forEach(dir => {
    const state = trafficLights[dir];
    ['Red', 'Yellow', 'Green'].forEach(color => {
      const element = document.getElementById(`light${dir.charAt(0).toUpperCase() + dir.slice(1)}${color}`);
      if (element) {
        element.style.opacity = state.toLowerCase() === color.toLowerCase() ? '1' : '0.3';
      }
    });
  });
}

// Generate random vehicles
function generateVehicles() {
  vehicles = [];
  const directions = ['north', 'south', 'east', 'west'];
  const numVehicles = Math.floor(Math.random() * 8) + 12;
  
  for (let i = 0; i < numVehicles; i++) {
    const direction = directions[Math.floor(Math.random() * directions.length)];
    const isEmergency = Math.random() < 0.1;
    
    vehicles.push({
      id: `v-${i}`,
      direction,
      position: Math.random() * 0.8,
      isEmergency,
      speed: isEmergency ? 0.015 : 0.01
    });
  }
  
  renderVehicles();
}

// Render vehicles on intersection
function renderVehicles() {
  const container = document.getElementById('vehiclesContainer');
  if (!container) return;
  
  container.innerHTML = '';
  
  vehicles.forEach(vehicle => {
    let x, y, rotation;
    
    switch(vehicle.direction) {
      case 'north':
        x = 270;
        y = 500 - (vehicle.position * 300);
        rotation = 0;
        break;
      case 'south':
        x = 330;
        y = vehicle.position * 300;
        rotation = 180;
        break;
      case 'east':
        x = vehicle.position * 400;
        y = 220;
        rotation = 90;
        break;
      case 'west':
        x = 600 - (vehicle.position * 400);
        y = 280;
        rotation = 270;
        break;
    }
    
    const color = vehicle.isEmergency ? '#dc2626' : '#2563eb';
    const vehicleEl = document.createElementNS('http://www.w3.org/2000/svg', 'g');
    vehicleEl.setAttribute('transform', `translate(${x}, ${y}) rotate(${rotation})`);
    vehicleEl.innerHTML = `
      <rect x="-8" y="-15" width="16" height="30" rx="2" fill="${color}" opacity="0.8"/>
      ${vehicle.isEmergency ? '<circle cx="0" cy="-10" r="3" fill="#fff" opacity="0.9"/>' : ''}
    `;
    container.appendChild(vehicleEl);
  });
}

// Initialize emergency vehicles list
function initEmergencyVehicles() {
  emergencyVehicles = [
    { id: 'EV-001', type: 'Ambulance', location: '400m North', eta: 45, status: 'Approaching' },
    { id: 'EV-002', type: 'Fire Truck', location: '800m East', eta: 90, status: 'En Route' }
  ];
  
  updateEmergencyList();
}

// Update emergency vehicles display
function updateEmergencyList() {
  const container = document.getElementById('emergencyList');
  if (!container) return;
  
  if (emergencyVehicles.length === 0) {
    container.innerHTML = '<div style="text-align: center; color: var(--color-text-secondary); padding: 20px;">No emergency vehicles active</div>';
    return;
  }
  
  container.innerHTML = emergencyVehicles.map(ev => {
    const statusClass = ev.status.toLowerCase().replace(' ', '');
    return `
      <div class="emergency-item">
        <div class="emergency-info">
          <div class="emergency-id">${ev.id}</div>
          <div class="emergency-type">${ev.type}</div>
          <div class="emergency-location">${ev.location} • ETA: ${ev.eta}s</div>
        </div>
        <div class="emergency-status status-${statusClass}">${ev.status}</div>
      </div>
    `;
  }).join('');
}

// Initialize system logs
function initSystemLogs() {
  const logs = [
    { time: '14:23:45', type: 'INFO', message: 'Traffic light cycle completed - North direction' },
    { time: '14:23:40', type: 'WARNING', message: 'High queue detected on East approach' },
    { time: '14:23:35', type: 'CRITICAL', message: 'Emergency vehicle EV-001 detected - Priority mode activated' },
    { time: '14:23:30', type: 'INFO', message: 'RL agent decision: Extend green for North' }
  ];
  
  const container = document.getElementById('systemLogs');
  if (!container) return;
  
  logs.forEach(log => addLogEntry(log));
}

// Add log entry
function addLogEntry(log) {
  const container = document.getElementById('systemLogs');
  if (!container) return;
  
  const entry = document.createElement('div');
  entry.className = `log-entry log-${log.type.toLowerCase()}`;
  entry.innerHTML = `
    <span class="log-time">${log.time}</span>
    <span class="log-type">${log.type}</span>
    <span class="log-message">${log.message}</span>
  `;
  
  container.insertBefore(entry, container.firstChild);
  
  // Keep only last 20 logs
  while (container.children.length > 20) {
    container.removeChild(container.lastChild);
  }
}

// Initialize controls
function initControls() {
  const pauseBtn = document.getElementById('pauseBtn');
  const playBtn = document.getElementById('playBtn');
  const clearLogsBtn = document.getElementById('clearLogs');
  
  if (pauseBtn) {
    pauseBtn.addEventListener('click', () => {
      simulationRunning = false;
      pauseBtn.style.display = 'none';
      playBtn.style.display = 'flex';
    });
  }
  
  if (playBtn) {
    playBtn.addEventListener('click', () => {
      simulationRunning = true;
      playBtn.style.display = 'none';
      pauseBtn.style.display = 'flex';
    });
  }
  
  if (clearLogsBtn) {
    clearLogsBtn.addEventListener('click', () => {
      const container = document.getElementById('systemLogs');
      if (container) container.innerHTML = '';
    });
  }
}

// Start simulation
function startSimulation() {
  generateVehicles();
  
  // Update vehicles every 100ms
  setInterval(() => {
    if (!simulationRunning) return;
    
    vehicles.forEach(vehicle => {
      vehicle.position += vehicle.speed;
      if (vehicle.position > 1) {
        vehicle.position = 0;
      }
    });
    
    renderVehicles();
  }, 100);
  
  // Update metrics every 2 seconds
  setInterval(() => {
    if (!simulationRunning) return;
    
    updateMetrics();
    updateCharts();
  }, 2000);
  
  // Cycle traffic lights every 5 seconds
  setInterval(() => {
    if (!simulationRunning) return;
    
    cycleTrafficLights();
  }, 5000);
  
  // Random emergency vehicle events
  setInterval(() => {
    if (!simulationRunning) return;
    
    if (Math.random() < 0.3) {
      addEmergencyVehicle();
    }
  }, 8000);
  
  // Add random log entries
  setInterval(() => {
    if (!simulationRunning) return;
    
    addRandomLog();
  }, 4000);
}

// Update metrics
function updateMetrics() {
  const totalVehicles = Math.floor(Math.random() * 20) + 150;
  const emergencyActive = emergencyVehicles.length;
  const avgWaitTime = (Math.random() * 10 + 38).toFixed(1);
  
  document.getElementById('totalVehicles').textContent = totalVehicles;
  document.getElementById('emergencyVehicles').textContent = emergencyActive;
  document.getElementById('avgWaitTime').innerHTML = `${avgWaitTime}<span class="metric-unit">s</span>`;
}

// Update charts with new data
function updateCharts() {
  // Update queue chart
  if (queueChart) {
    const newLabel = new Date().toLocaleTimeString('en-US', { hour12: false, minute: '2-digit', second: '2-digit' });
    queueChart.data.labels.push(newLabel);
    queueChart.data.labels.shift();
    
    queueChart.data.datasets.forEach(dataset => {
      dataset.data.push(Math.floor(Math.random() * 15) + 5);
      dataset.data.shift();
    });
    
    queueChart.update('none');
  }
  
  // Update delay chart
  if (delayChart) {
    delayChart.data.datasets[0].data = [
      Math.floor(Math.random() * 20) + 35,
      Math.floor(Math.random() * 20) + 35,
      Math.floor(Math.random() * 20) + 35,
      Math.floor(Math.random() * 20) + 35
    ];
    delayChart.update('none');
  }
}

// Cycle traffic lights
function cycleTrafficLights() {
  const hasEmergency = emergencyVehicles.some(ev => ev.status === 'Approaching');
  
  if (hasEmergency) {
    // Priority for emergency vehicle
    trafficLights = {
      north: 'green',
      south: 'red',
      east: 'red',
      west: 'red'
    };
    addLogEntry({
      time: new Date().toLocaleTimeString('en-US', { hour12: false }),
      type: 'CRITICAL',
      message: 'Emergency priority activated - All lights red except North'
    });
  } else {
    // Normal cycle
    if (trafficLights.north === 'green') {
      trafficLights = { north: 'yellow', south: 'red', east: 'red', west: 'red' };
      setTimeout(() => {
        trafficLights = { north: 'red', south: 'red', east: 'green', west: 'green' };
        updateTrafficLights();
      }, 2000);
    } else {
      trafficLights = { north: 'green', south: 'green', east: 'yellow', west: 'yellow' };
      setTimeout(() => {
        trafficLights = { north: 'green', south: 'green', east: 'red', west: 'red' };
        updateTrafficLights();
      }, 2000);
    }
  }
  
  updateTrafficLights();
}

// Add emergency vehicle
function addEmergencyVehicle() {
  const types = ['Ambulance', 'Fire Truck', 'Police Car'];
  const directions = ['North', 'South', 'East', 'West'];
  const id = `EV-${String(Math.floor(Math.random() * 1000)).padStart(3, '0')}`;
  
  const newVehicle = {
    id,
    type: types[Math.floor(Math.random() * types.length)],
    location: `${Math.floor(Math.random() * 800) + 200}m ${directions[Math.floor(Math.random() * directions.length)]}`,
    eta: Math.floor(Math.random() * 60) + 30,
    status: 'Approaching'
  };
  
  emergencyVehicles.push(newVehicle);
  updateEmergencyList();
  
  addLogEntry({
    time: new Date().toLocaleTimeString('en-US', { hour12: false }),
    type: 'CRITICAL',
    message: `Emergency vehicle ${id} detected - ${newVehicle.type}`
  });
  
  // Remove after some time
  setTimeout(() => {
    const index = emergencyVehicles.findIndex(ev => ev.id === id);
    if (index !== -1) {
      emergencyVehicles.splice(index, 1);
      updateEmergencyList();
      
      addLogEntry({
        time: new Date().toLocaleTimeString('en-US', { hour12: false }),
        type: 'INFO',
        message: `Emergency vehicle ${id} cleared intersection`
      });
    }
  }, Math.random() * 20000 + 10000);
}

// Add random log entry
function addRandomLog() {
  const logTypes = [
    { type: 'INFO', messages: [
      'Traffic light cycle completed',
      'RL agent decision: Optimal timing applied',
      'Queue cleared on West approach',
      'Normal traffic flow detected'
    ]},
    { type: 'WARNING', messages: [
      'High queue detected on East approach',
      'Unusual traffic pattern observed',
      'Congestion building on South direction'
    ]}
  ];
  
  const selectedType = logTypes[Math.floor(Math.random() * logTypes.length)];
  const message = selectedType.messages[Math.floor(Math.random() * selectedType.messages.length)];
  
  addLogEntry({
    time: new Date().toLocaleTimeString('en-US', { hour12: false }),
    type: selectedType.type,
    message
  });
}

// Initialize dashboard when DOM is loaded
if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', initDashboard);
} else {
  initDashboard();
}