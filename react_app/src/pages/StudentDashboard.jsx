import React from 'react'
import Navbar from '../components/Navbar'
import Sidebar from '../components/Sidebar'
import { Link } from 'react-router-dom'

export default function StudentDashboard(){
  return (
    <div>
      <Navbar />
      <div className="container flex gap-6 mt-6">
        <Sidebar />
        <main className="flex-1">
          <div className="card p-4">
            <div className="flex items-center justify-between">
              <h3 className="text-lg font-semibold">Student Dashboard</h3>
              <div className="text-sm text-muted">Practice and assignments</div>
            </div>
            <div className="mt-4 grid grid-cols-1 md:grid-cols-2 gap-4">
              <Link to="/practice" className="p-4 card hover:shadow">Practice Questions</Link>
              <Link to="/practice" className="p-4 card hover:shadow">Assigned Papers</Link>
            </div>
          </div>
        </main>
      </div>
    </div>
  )
}
