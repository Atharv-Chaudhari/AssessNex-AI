// Centralized configuration for API endpoints and mock data
export const API_BASE = import.meta.env.VITE_API_BASE || '/api'

export const ENDPOINTS = {
  auth: {
    login: `${API_BASE}/auth/login`,
    register: `${API_BASE}/auth/register`,
    me: `${API_BASE}/user/me`
  },
  upload: `${API_BASE}/upload`,
  parse: `${API_BASE}/parse`,
  generate: `${API_BASE}/generate`,
  questions: `${API_BASE}/questions`,
  saveExam: `${API_BASE}/save-exam`,
  studentQuestions: `${API_BASE}/student/questions`,
  sendEmail: `${API_BASE}/send-email`
}

export const MOCK = {
  homepage: 'https://Atharv-Chaudhari.github.io/AssessNex-AI',
  defaultRoles: ['Professor','Assistant','Student']
}

export function makeMockUser(role = 'Student', email, name){
  const displayName = name ? name : (role === 'Professor' ? 'Dr. Priya Rao' : role === 'Assistant' ? 'Kiran Sharma' : 'Aarav Patel')
  return {
    id: Math.floor(Math.random()*9000)+1000,
    name: displayName,
    email: email || `${role.toLowerCase()}@example.com`,
    role
  }
}

export default {
  API_BASE,
  ENDPOINTS,
  MOCK,
  makeMockUser
}
