const API_BASE_URL = "http://localhost:8000";

export async function getHelmets() {
  const response = await fetch(`${API_BASE_URL}/api/helmets/`);

  if (!response.ok) {
    throw new Error("Failed to fetch helmets");
  }

  return response.json();
}

export async function getHelmet(helmetId) {
  const response = await fetch(
    `${API_BASE_URL}/api/helmets/${helmetId}`
  );

  if (!response.ok) {
    throw new Error("Failed to fetch helmet");
  }

  return response.json();
}