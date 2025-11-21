import React, {useState} from 'react'
import Navbar from '../components/Navbar'
import Sidebar from '../components/Sidebar'
import api from '../services/api'

export default function ParsePage(){
  const [preview, setPreview] = useState('')
  const [loading, setLoading] = useState(false)

  const runParse = async ()=>{
    setLoading(true)
    const res = await api.parse('demo-file')
    setPreview(res.data.text)
    setLoading(false)
  }

  return (
    <div>
      <Navbar />
      <div className="container flex gap-6 mt-6">
        <Sidebar />
        <main className="flex-1">
          <h3 className="text-lg font-semibold mb-3">Document Processing (OCR preview)</h3>
          <div className="card p-4">
            <button onClick={runParse} className="px-4 py-2 bg-primary text-white rounded">Run OCR</button>
            <div className="mt-3 whitespace-pre-wrap bg-gray-50 p-3 rounded">{loading ? 'Processing...' : preview || 'No preview yet'}</div>
          </div>
        </main>
      </div>
    </div>
  )
}
