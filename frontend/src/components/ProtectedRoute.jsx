import { Navigate } from 'react-router-dom';
import { ApiService } from '../services/api';

export default function ProtectedRoute({ children }) {
  const isAuthenticated = ApiService.isAuthenticated();
  
  return isAuthenticated ? children : <Navigate to="/login" replace />;
}
