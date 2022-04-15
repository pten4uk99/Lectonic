import {baseWS} from "./ProjectConstants";

let notificationsWs;


export function createNotificationsSocket(setSocket, userId, setFailConnection) {
  if (notificationsWs) return
  notificationsWs = new WebSocket(`${baseWS}/ws/connect/${userId}`)
  
  notificationsWs.onopen = (e) => {
    setSocket(notificationsWs);
    setFailConnection(false)
    console.log('Соединение установлено')
  }
  notificationsWs.onclose = (e) => {
    if (e.wasClean) {
      notificationsWs = null
      setFailConnection(false)
      console.log('Соединение завершено')
    } else {
      notificationsWs = null
      setFailConnection(true)
      setTimeout(() => createNotificationsSocket(setSocket, userId, setFailConnection), 3000)
      console.log('Соединение разорвано')
    }
  }
}

export function createChatSocket(setSocket, chatId) {
  let socket = new WebSocket(`${baseWS}/ws/chat/${chatId}`)
  
  socket.onopen = (e) => {
    setSocket(socket);
    console.log('Соединение с чатом установлено')
  }
  socket.onclose = (e) => {
    if (e.wasClean) {
      console.log('Соединение с чатом завершено')
    } else {
      setTimeout(() => createChatSocket(setSocket, chatId), 3000)
      console.log('Соединение с чатом разорвано')
    }
  }
}
