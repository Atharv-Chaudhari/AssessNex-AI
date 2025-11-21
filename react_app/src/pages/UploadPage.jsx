import React from 'react'
import Navbar from '../components/Navbar'
import Sidebar from '../components/Sidebar'
import FileUploader from '../components/FileUploader'

export default function UploadPage(){
  const onUploaded = (data)=>{ console.log('uploaded',data) }
  return (
    <div>
      <Navbar />
      <div className="container flex gap-6 mt-6">
        <Sidebar />
        <main className="flex-1">
          <h3 className="text-lg font-semibold mb-3">Upload Documents</h3>
          <FileUploader onUploaded={onUploaded} />
        </main>
      </div>
    </div>
  )
}
