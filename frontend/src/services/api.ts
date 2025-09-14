import axios from 'axios';
import { StartupInput, AnalysisResults, ApiResponse } from '../types';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8080/api';

const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 300000, // 5 minutes timeout for analysis
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add request interceptor for logging
api.interceptors.request.use(
  (config) => {
    console.log(`Making ${config.method?.toUpperCase()} request to ${config.url}`);
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Add response interceptor for error handling
api.interceptors.response.use(
  (response) => {
    return response;
  },
  (error) => {
    console.error('API Error:', error.response?.data || error.message);
    throw new Error(error.response?.data?.detail || error.message || 'API request failed');
  }
);

export const analyzeStartup = async (startupInput: StartupInput): Promise<ApiResponse<AnalysisResults>> => {
  try {
    const response = await api.post('/analyze', startupInput);
    return response.data;
  } catch (error: any) {
    throw new Error(error.message || 'Failed to analyze startup');
  }
};

export const getDemoScenarios = async (): Promise<{ scenarios: any[] }> => {
  try {
    const response = await api.get('/demo-scenarios');
    return response.data;
  } catch (error: any) {
    throw new Error(error.message || 'Failed to load demo scenarios');
  }
};

export const getHealthStatus = async (): Promise<{ status: string; timestamp: string }> => {
  try {
    const response = await api.get('/health');
    return response.data;
  } catch (error: any) {
    throw new Error(error.message || 'Failed to get health status');
  }
};

export const getSystemStatus = async (): Promise<{ status: string; agents: Record<string, string> }> => {
  try {
    const response = await api.get('/status');
    return response.data;
  } catch (error: any) {
    throw new Error(error.message || 'Failed to get system status');
  }
};
