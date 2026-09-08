const workerMockData = [
  {
    worker_id: "W001",
    name: "Worker 01",
    helmet_id: "H001",
    status: "Active",

    current_seen_node: "N001",
    last_seen_node: "N001",
    last_node_id: "N001",
    last_seen: "2026-09-08 11:55:00",

    helmet: {
      helmet_id: "H001",
      battery: 92,
      status: "Connected",
    },

    location: {
      node_id: "N001",
      last_node: "N001",
      last_seen_node: "N001",
      signal_strength: -55,
      timestamp: "2026-09-08 11:55:00",
    },

    sos: {
      active: false,
      message: "",
    },
  },

  {
    worker_id: "W002",
    name: "Worker 02",
    helmet_id: "H002",
    status: "Active",

    current_seen_node: "N002",
    last_seen_node: "N001",
    last_node_id: "N002",
    last_seen: "2026-09-08 11:52:00",

    helmet: {
      helmet_id: "H002",
      battery: 68,
      status: "Connected",
    },

    location: {
      node_id: "N002",
      last_node: "N001",
      last_seen_node: "N001",
      signal_strength: -62,
      timestamp: "2026-09-08 11:52:00",
    },

    sos: {
      active: true,
      message: "Emergency alert triggered",
    },
  },

  {
    worker_id: "W003",
    name: "Worker 03",
    helmet_id: "H003",
    status: "Inactive",

    current_seen_node: "N003",
    last_seen_node: "N003",
    last_node_id: "N003",
    last_seen: "2026-09-08 11:20:00",

    helmet: {
      helmet_id: "H003",
      battery: 35,
      status: "Disconnected",
    },

    location: {
      node_id: "N003",
      last_node: "N003",
      last_seen_node: "N003",
      signal_strength: -80,
      timestamp: "2026-09-08 11:20:00",
    },

    sos: {
      active: false,
      message: "",
    },
  },
];

export default workerMockData;