import {baseURL} from "../../../ProjectConstants";

export function logout() {
  return fetch(`${baseURL}/api/auth/logout/`, {
    method: 'GET',
    credentials: 'include'
  })
}