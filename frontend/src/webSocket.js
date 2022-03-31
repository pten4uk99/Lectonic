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
  socket.onmessage = (e) => {
    console.log(JSON.parse(e.data))
  }
}