const API_BASE_URL = "http://localhost:8000";

export async function getWorkers() {
  const response = await fetch(`${API_BASE_URL}/api/workers/`);

  if (!response.ok) {
    throw new Error("Failed to fetch workers");
  }

  return response.json();
}

export async function getWorker(workerId) {
  const response = await fetch(
    `${API_BASE_URL}/api/workers/${workerId}`
  );

  if (!response.ok) {
    throw new Error("Failed to fetch worker");
  }

  return response.json();
}