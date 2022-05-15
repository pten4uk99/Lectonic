import {baseURL} from "../../../ProjectConstants";


const HEADERS = {
  'Content-Type': 'application/json',
}


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

export function getChatMessages(chat_id) {
  return fetch(`${baseURL}/api/chat/message_list/?chat_id=${chat_id}`, {
    method: 'GET',
    credentials: 'include'
  })
}
