import { useState } from 'react'
import ResourceList from './components/ResourceList'

function App() {
  const [count, setCount] = useState(0)

  return (
    <div className="min-h-screen bg-gray-100">
      {/* 標題區域 */}
      <div className="bg-white shadow-sm">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-4">
              <div className="w-12 h-12 bg-blue-500 rounded-full flex items-center justify-center">
                <span className="text-white font-bold text-lg">R</span>
              </div>
              <h1 className="text-2xl font-bold text-gray-800">Resource School</h1>
            </div>
            <div className="text-sm text-gray-500">
              前端: React + Vite + TailwindCSS | 後端: FastAPI + MySQL
            </div>
          </div>
        </div>
      </div>

      {/* 主要內容 */}
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
    </div>
  )
}

export default App