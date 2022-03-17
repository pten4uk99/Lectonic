import React from 'react'
import { useLocation, Navigate } from 'react-router-dom'
import { useAuth } from '../hook/useAuth'

export default function RequireAuth({children}) {
  const {user} = useAuth();
  
  if (!user) {
    return <Navigate to='/'/>
  }
  return children;               
}