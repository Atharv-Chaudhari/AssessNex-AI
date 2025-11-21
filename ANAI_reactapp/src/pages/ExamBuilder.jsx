import React, {useState} from 'react'
import Navbar from '../components/Navbar'
import Sidebar from '../components/Sidebar'
import DragDropBuilder from '../components/DragDropBuilder'
import api from '../services/api'

export default function ExamBuilder(){
  const [saved, setSaved] = useState(null)

  const save = async (items) => {
    const res = await api.saveExam({title: 'New Exam', items})
    setSaved(res.data)
  }

  const initial = Array.from({length:6}).map((_,i)=>({id:i+1,text:`Q ${i+1}: sample`}))

  return (
    <div>
      <Navbar />
      <div className="container flex gap-6 mt-6">
        <Sidebar />
        <main className="flex-1">
          <h3 className="text-lg font-semibold mb-3">Exam Builder</h3>
          <DragDropBuilder initial={initial} onSave={save} />
          {saved && <div className="mt-3 card p-3">Saved exam id: {saved.id}</div>}
        </main>
      </div>
    </div>
  )
}
