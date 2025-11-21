import React from 'react'
import Navbar from '../components/Navbar'
import Sidebar from '../components/Sidebar'
import { Link } from 'react-router-dom'

export default function ProfessorDashboard(){
  return (
    <div>
      <Navbar />
      <div className="container flex gap-6 mt-6">
        <Sidebar />
        <main className="flex-1">
          <div className="card p-4">
            <div className="flex items-center justify-between">
              <h3 className="text-lg font-semibold">Professor Dashboard</h3>
              <div className="text-sm text-muted">Premium AI tools</div>
            </div>
            <div className="mt-4 grid grid-cols-1 md:grid-cols-3 gap-4">
              <Link to="/upload" className="p-4 card hover:shadow">Upload Documents</Link>
              <Link to="/generate" className="p-4 card hover:shadow">Generate Questions</Link>
              <Link to="/exam-builder" className="p-4 card hover:shadow">Build Exam Paper</Link>
            </div>
          </div>
        </main>
      </div>
    </div>
  )
}
