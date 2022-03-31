import {baseURL} from "../../../ProjectConstants";

export function logout() {
  return fetch(`${baseURL}/api/auth/logout/`, {
    method: 'GET',
    credentials: 'include'
  })
}


export function getNotificationsList() {
  return fetch(`${baseURL}/api/chat/chat_list/`, {
    method: 'GET',
    credentials: 'include'
  })
}

