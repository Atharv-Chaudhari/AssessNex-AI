import React, {useState, useRef} from 'react'
import Navbar from '../components/Navbar'
import Sidebar from '../components/Sidebar'
import api from '../services/api'
import QuestionCard from '../components/QuestionCard'
import Modal from '../components/Modal'
import { renderElementToPdfBlob, downloadBlob } from '../utils/pdf'
import { Mail } from 'lucide-react'

export default function GeneratePage(){
  const [questions, setQuestions] = useState([])
  const [loading, setLoading] = useState(false)
  const [pdfLoading, setPdfLoading] = useState(false)
  const [pdfBlob, setPdfBlob] = useState(null)
  const [emailOpen, setEmailOpen] = useState(false)
  const [recipient, setRecipient] = useState('')
  const previewRef = useRef()

  const runGenerate = async ()=>{
    setLoading(true)
    const res = await api.generate({docs:[], settings:{}})
    setQuestions(res.data.questions)
    setLoading(false)
  }

  const previewPdf = async ()=>{
    if(!previewRef.current) return
    setPdfLoading(true)
    try{
      const blob = await renderElementToPdfBlob(previewRef.current)
      setPdfBlob(blob)
    }catch(e){ console.error(e) }
    setPdfLoading(false)
  }

  const downloadPdf = async ()=>{
    if(!pdfBlob) { await previewPdf() }
    if(pdfBlob) downloadBlob(pdfBlob, `AssessNex-paper-${Date.now()}.pdf`)
  }

  const sendPdfByEmail = async (to)=>{
    if(!pdfBlob) { await previewPdf() }
    if(!pdfBlob) return
    setPdfLoading(true)
    try{
      // Convert blob to base64 for mock transport
      const arr = await pdfBlob.arrayBuffer()
      const b64 = btoa(String.fromCharCode(...new Uint8Array(arr)))
      const res = await api.sendEmail({ to, subject: 'Generated Question Paper', body: 'Attached is your generated paper', attachment: b64 })
      // success
      alert(`Email sent to ${to} (mock).`)
      setEmailOpen(false)
    }catch(e){ console.error(e); alert('Email failed') }
    setPdfLoading(false)
  }

  return (
    <div>
      <Navbar />
      <div className="container flex gap-6 mt-6">
        <Sidebar />
        <main className="flex-1">
          <h3 className="text-lg font-semibold mb-3">Question Generation</h3>
          <div className="card p-4 space-y-4">
            <div className="flex items-center justify-between">
              <div>
                <div className="text-sm text-muted">Use uploaded docs to generate questions automatically.</div>
                <div className="text-xs text-muted">Configure paper layout and metadata below before exporting.</div>
              </div>
              <div className="flex items-center gap-2">
                <button onClick={runGenerate} className="btn btn-accent btn-sm">Generate Questions</button>
                <button onClick={previewPdf} className="btn btn-ghost btn-sm">Preview PDF</button>
                <button onClick={downloadPdf} className="btn btn-primary btn-sm">Download PDF</button>
                <button onClick={()=>setEmailOpen(true)} className="btn btn-sm btn-ghost"><Mail size={14}/> Email</button>
              </div>
            </div>

            <div className="grid md:grid-cols-2 gap-4">
              <div className="space-y-3">
                <label className="block">
                  <div className="text-xs text-muted mb-1">Paper title</div>
                  <input className="input" placeholder="Midterm — Introduction to AI" />
                </label>
                <label className="block">
                  <div className="text-xs text-muted mb-1">Duration</div>
                  <input className="input" placeholder="90 minutes" />
                </label>
                <label className="block">
                  <div className="text-xs text-muted mb-1">Include answers?</div>
                  <select className="input">
                    <option value="no">No</option>
                    <option value="inline">Inline (for instructor)</option>
                  </select>
                </label>
              </div>

              <div>
                <div className="text-sm font-medium mb-2">Generated questions</div>
                <div className="space-y-3">
                  {loading && <div className="text-muted">Generating questions…</div>}
                  {questions.length===0 && !loading && <div className="text-muted">No questions yet — click Generate.</div>}
                  {questions.map(q=> <QuestionCard key={q.id} q={q} />)}
                </div>
                {emailOpen && (
                  <Modal open={emailOpen} onClose={()=>setEmailOpen(false)} title="Email Generated PDF">
                    <div>
                      <label className="block mb-2">
                        <div className="text-xs text-muted mb-1">Recipient email</div>
                        <input value={recipient} onChange={(e)=>setRecipient(e.target.value)} className="input" placeholder="instructor@example.edu" />
                      </label>
                      <div className="flex items-center gap-3">
                        <button onClick={()=>sendPdfByEmail(recipient)} className="btn btn-primary btn-sm">Send Email</button>
                        <button onClick={()=>{ downloadPdf() }} className="btn btn-ghost btn-sm">Download instead</button>
                        {pdfLoading && <div className="text-sm text-muted">Processing…</div>}
                      </div>
                    </div>
                  </Modal>
                )}
              </div>
            </div>

            <div className="mt-4">
              <div className="text-sm font-medium mb-2">PDF Preview (rendered client-side)</div>
              <div ref={previewRef} className="p-4 bg-white border rounded-md">
                <div className="text-center mb-4">
                  <div className="text-xl font-semibold">Sample Question Paper</div>
                  <div className="text-xs text-muted">Generated by AssessNex</div>
                </div>
                <ol className="list-decimal pl-6 space-y-3">
                  {questions.map(q=> <li key={q.id} className="text-sm leading-relaxed">{q.text}</li>)}
                </ol>
              </div>
            </div>
          </div>
        </main>
      </div>
    </div>
  )
}
