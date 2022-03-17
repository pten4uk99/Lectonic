export function logout() {
  return fetch('http://127.0.0.1:8000/api/auth/logout/', {
    method: 'GET',
    credentials: 'include'
  })
}