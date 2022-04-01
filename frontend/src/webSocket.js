import {hostURL} from "./ProjectConstants";

export function createNotificationsSocket(setSocket, userId) {
  let socket = new WebSocket(`ws://${hostURL}/connect/${userId}`)
  
  socket.onopen = (e) => {
    setSocket(socket);
    console.log('Соединение установлено')
  }
  socket.onclose = () => {
    setTimeout(() => createNotificationsSocket(setSocket, userId), 3000)
    console.log('Соединение разорвано')
  }
}

export function createChatSocket(setSocket, chatId) {
  let socket = new WebSocket(`ws://${hostURL}/chat/${chatId}`)
  
  socket.onopen = (e) => {
    setSocket(socket);
    console.log('Соединение с чатом установлено')
  }
  socket.onclose = () => {
    setTimeout(() => createChatSocket(setSocket, chatId), 3000)
    console.log('Соединение с чатом разорвано')
  }
}
