import axios from 'axios'
import config, { ENDPOINTS, makeMockUser } from '../config'

const delay = (ms=700)=> new Promise(r=>setTimeout(r,ms))

const api = axios.create({ baseURL: config.API_BASE || '/' })

export default {
  endpoints: ENDPOINTS,
  auth: {
    login: async ({email, password, role, name}) => {
      await delay(700)
      const token = `mock-jwt-${role}-${Date.now()}`
      return { data: { token, user: makeMockUser(role, email, name), endpoint: ENDPOINTS.auth.login } }
    },
    register: async ({name, email, password, role}) => {
      await delay(900)
      const token = `mock-jwt-${role}-${Date.now()}`
      return { data: { token, user: makeMockUser(role, email, name), endpoint: ENDPOINTS.auth.register } }
    },
    me: async (token) => {
      await delay(400)
      if(!token) throw new Error('Not authenticated')
      const parts = token.split('-')
      const role = parts[2] || 'Student'
      return { data: { user: makeMockUser(role), endpoint: ENDPOINTS.auth.me } }
    }
  },
  upload: async (file) => {
    await delay(800)
    return { data: { id: Date.now(), name: file?.name || 'document.pdf', size: file?.size||12345, status: 'uploaded', endpoint: ENDPOINTS.upload } }
  },
  parse: async (fileId) => {
    await delay(1000)
    return { data: { text: `Extracted text preview for file ${fileId}...\n1. What is X?\n2. Explain Y.\n3. Solve Z.`, endpoint: ENDPOINTS.parse } }
  },
  generate: async ({docs, settings}) => {
    await delay(1200)
    const questions = Array.from({length:5}).map((_,i)=>({ id: i+1, text: `Generated question ${i+1} based on docs`, difficulty: ['Easy','Medium','Hard'][i%3] }))
    return { data: { questions, endpoint: ENDPOINTS.generate } }
  },
  questions: async () => {
    await delay(500)
    const q = Array.from({length:8}).map((_,i)=>({ id: i+1, text: `Sample question ${i+1}`, choices: [], answer: null }))
    return { data: q, endpoint: ENDPOINTS.questions }
  },
  saveExam: async (payload) => {
    await delay(700)
    return { data: { id: Date.now(), ...payload, status: 'saved', endpoint: ENDPOINTS.saveExam } }
  },
  sendEmail: async ({to, subject, body, attachment}) => {
    await delay(900)
    // Mock email send - in a real app you'd POST to your mail backend
    return { data: { status: 'sent', to, subject, endpoint: ENDPOINTS.sendEmail } }
  },
  student: {
    questions: async (studentId) => {
      await delay(400)
      const q = Array.from({length:6}).map((_,i)=>({ id: i+1, text: `Practice question ${i+1}`, difficulty: ['Easy','Medium'][i%2] }))
      return { data: q, endpoint: ENDPOINTS.studentQuestions }
    }
  }
}
