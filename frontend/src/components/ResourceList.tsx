import { useState, useEffect } from 'react';
import { ApiService } from '../services/api';

export default function ResourceList() {
  const [resources, setResources] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    loadResources();
  }, []);

  const loadResources = async () => {
    try {
      setLoading(true);
      const data = await ApiService.getResources();
      setResources(data);
      setError(null);
    } catch (err) {
      setError('載入資源失敗');
      console.error('Error loading resources:', err);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="flex justify-center items-center p-8">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-500"></div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded">
        {error}
      </div>
    );
  }

  return (
    <div className="space-y-4">
      <h2 className="text-2xl font-bold text-gray-800">資源列表</h2>
      {resources.length === 0 ? (
        <div className="text-center py-8 text-gray-500">
          目前沒有資源
        </div>
      ) : (
        <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
          {resources.map((resource) => (
            <div key={resource.id} className="bg-white rounded-lg shadow-md p-6">
              <h3 className="text-lg font-semibold text-gray-800 mb-2">
                {resource.title}
              </h3>
              {resource.description && (
                <p className="text-gray-600 mb-3">{resource.description}</p>
              )}
              {resource.category && (
                <span className="inline-block bg-blue-100 text-blue-800 text-xs px-2 py-1 rounded mb-3">
                  {resource.category}
                </span>
              )}
              {resource.url && (
                <a
                  href={resource.url}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="text-blue-600 hover:text-blue-800 underline"
                >
                  查看資源
                </a>
              )}
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
