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

export function deleteChat(id) {
  return fetch(`${baseURL}/api/chat/chat_list/?chat_id=${id}`, {
    method: 'DELETE',
    credentials: 'include'
  })
}

export function getChatMessages(chat_id) {
  return fetch(`${baseURL}/api/chat/message_list/?chat_id=${chat_id}`, {
    method: 'GET',
    credentials: 'include'
  })
}


// пока не настроен вебсокет
export function createChatMessage(chat_id, text, confirm) {
  let options = {
    method: 'POST',
    headers: HEADERS,
    body: JSON.stringify({
      chat_id: chat_id,
      text: text,
      confirm: confirm
    }),
    credentials: 'include'
  }
  return fetch(`${baseURL}/api/chat/message_list/`, options)
}
