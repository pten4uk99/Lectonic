import {hostURL} from "./ProjectConstants";

export function createNotificationsSocket(setSocket, userId) {
  let socket = new WebSocket(`ws://${hostURL}/connect/${userId}`)
  
  socket.onopen = (e) => {
    setSocket(socket);
    console.log('Соединение установлено')
  }
  socket.onclose = (e) => {
    if (e.wasClean) {
      console.log('Соединение завершено')
    } else {
      setTimeout(() => createNotificationsSocket(setSocket, userId), 3000)
      console.log('Соединение разорвано')
    }
  }
}

export function createChatSocket(setSocket, chatId) {
  let socket = new WebSocket(`ws://${hostURL}/chat/${chatId}`)
  
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
