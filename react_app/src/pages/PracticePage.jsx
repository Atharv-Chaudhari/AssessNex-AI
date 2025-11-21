import React, {useEffect, useState} from 'react'
import Navbar from '../components/Navbar'
import Sidebar from '../components/Sidebar'
import api from '../services/api'

export default function PracticePage(){
  const [questions, setQuestions] = useState([])

  useEffect(()=>{
    api.student.questions().then(res=>setQuestions(res.data))
  },[])

  const download = (q)=>{
    const blob = new Blob([q.text], { type: 'text/plain' })
    const url = URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = `question-${q.id}.txt`
    a.click()
    URL.revokeObjectURL(url)
  }

  return (
    <div>
      <Navbar />
      <div className="container flex gap-6 mt-6">
        <Sidebar />
        <main className="flex-1">
          <h3 className="text-lg font-semibold mb-3">Practice Questions</h3>
          <div className="space-y-3">
            {questions.map(q=> (
              <div key={q.id} className="card p-3 flex items-center justify-between">
                <div>{q.text}</div>
                <div>
                  <button onClick={()=>download(q)} className="btn btn-sm btn-ghost">Download</button>
                </div>
              </div>
            ))}
          </div>
        </main>
      </div>
    </div>
  )
}
