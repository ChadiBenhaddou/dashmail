const BASE_URL = import.meta.env.VITE_API_BASE_URL || "";

export async function getReport(id) {
  const res = await fetch(`${BASE_URL}/api/dashboard/${id}/`);
  if (!res.ok) {
    throw new Error(`Erreur ${res.status}: ${res.statusText}`);
  }
  return res.json();
}
