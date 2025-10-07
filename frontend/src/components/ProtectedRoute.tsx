import { type ReactNode } from 'react';
import { Navigate } from 'react-router-dom';
import { ApiService } from '../services/api';

interface ProtectedRouteProps {
  children: ReactNode;
}

export default function ProtectedRoute({ children }: ProtectedRouteProps) {
  const isAuthenticated = ApiService.isAuthenticated();
  
  return isAuthenticated ? <>{children}</> : <Navigate to="/login" replace />;
}
