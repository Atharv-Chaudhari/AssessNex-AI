import React, {useEffect, useState} from 'react'
import Navbar from '../components/Navbar'
import Sidebar from '../components/Sidebar'
import api from '../services/api'
import QuestionCard from '../components/QuestionCard'
import Modal from '../components/Modal'


export default function ReviewPage(){
  const [questions, setQuestions] = useState([])

  useEffect(()=>{
    api.questions().then(res=>setQuestions(res.data))
  },[])

  const approve = (q)=>{
    setQuestions(prev => prev.filter(p=>p.id!==q.id))
  }

  const [editing, setEditing] = useState(null)

  const onEdit = (q)=>{
    setEditing(q)
  }

  const saveEdit = (updated)=>{
    setQuestions(prev => prev.map(p=> p.id===updated.id ? updated : p))
    setEditing(null)
  }

  return (
    <div>
      <Navbar />
      <div className="container flex gap-6 mt-6">
        <Sidebar />
        <main className="flex-1">
          <h3 className="text-lg font-semibold mb-3">Review & Edit Questions</h3>
          <div className="space-y-3">
            {questions.map(q=> <QuestionCard key={q.id} q={q} onApprove={approve} onEdit={onEdit} />)}
          </div>
          <Modal open={!!editing} onClose={()=>setEditing(null)} title="Edit Question">
            {editing && (
              <EditForm q={editing} onSave={saveEdit} />
            )}
          </Modal>
        </main>
      </div>
    </div>
  )
}

function EditForm({q, onSave}){
  const [text, setText] = useState(q.text)
  return (
    <div>
      <textarea className="w-full p-2 border rounded" value={text} onChange={e=>setText(e.target.value)} />
      <div className="mt-3 flex justify-end">
        <button onClick={()=>onSave({...q, text})} className="btn btn-primary">Save</button>
      </div>
    </div>
  )
}
