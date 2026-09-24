import axios from 'axios';

const API_BASE = '/api';

const api = axios.create({
  baseURL: API_BASE,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const getDashboardSummary = async () => {
  const res = await api.get('/dashboard/summary');
  return res.data;
};

export const getSessions = async () => {
  const res = await api.get('/sessions');
  return res.data;
};

export const getSessionDetail = async (sessionId) => {
  const res = await api.get(`/sessions/${sessionId}`);
  return res.data;
};

export const getEvents = async (sessionId = null) => {
  const params = sessionId ? { session_id: sessionId } : {};
  const res = await api.get('/events', { params });
  return res.data;
};

export const getLures = async () => {
  const res = await api.get('/lures');
  return res.data;
};

export const generateLure = async (sessionId, interestOverride = null) => {
  const res = await api.post('/lures/generate', {
    session_id: sessionId,
    interest_override: interestOverride
  });
  return res.data;
};

export const deployLure = async (lureId, endpointPath = null) => {
  const res = await api.post(`/lures/${lureId}/deploy`, {
    endpoint_path: endpointPath
  });
  return res.data;
};

export const getInteractions = async () => {
  const res = await api.get('/interactions');
  return res.data;
};

export const getSimulationScenarios = async () => {
  const res = await api.get('/simulation/scenarios');
  return res.data;
};

export const runSimulation = async (scenarioId) => {
  const res = await api.post('/simulation/run', { scenario_id: scenarioId });
  return res.data;
};

export default api;
