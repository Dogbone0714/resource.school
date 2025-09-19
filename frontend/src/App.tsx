import { useState } from 'react'
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom'
import Navigation from './components/Navigation'
import ProtectedRoute from './components/ProtectedRoute'
import ResourceList from './components/ResourceList'
import LoginPage from './pages/LoginPage'
import UploadPage from './pages/UploadPage'
import ResultPage from './pages/ResultPage'

function HomePage() {
  const [count, setCount] = useState(0)

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <div className="mb-8">
        <div className="bg-white rounded-lg shadow-md p-6">
          <h2 className="text-xl font-semibold text-gray-800 mb-4">歡迎使用 Resource School</h2>
          <div className="text-center">
            <button 
              onClick={() => setCount((count) => count + 1)}
              className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded transition duration-200"
            >
              點擊次數: {count}
            </button>
            <p className="mt-4 text-gray-600">
              編輯 <code className="bg-gray-200 px-2 py-1 rounded">src/App.tsx</code> 並儲存以測試 HMR
            </p>
          </div>
        </div>
      </div>

      {/* 資源列表 */}
      <div className="bg-white rounded-lg shadow-md p-6">
        <ResourceList />
      </div>
    </div>
  )
}

function App() {
  return (
    <Router>
      <div className="min-h-screen bg-gray-100">
        <Navigation />
        
        <Routes>
          <Route path="/" element={<HomePage />} />
          <Route path="/login" element={<LoginPage />} />
          <Route 
            path="/upload" 
            element={
              <ProtectedRoute>
                <UploadPage />
              </ProtectedRoute>
            } 
          />
          <Route 
            path="/result/:userId" 
            element={
              <ProtectedRoute>
                <ResultPage />
              </ProtectedRoute>
            } 
          />
          <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
      </div>
    </Router>
  )
}

export default App