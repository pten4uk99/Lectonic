import {baseWS} from "./ProjectConstants";

let ws;

export function createSocket(setSocket, userId, setFailConnection) {
  if (ws) return
  ws = new WebSocket(`${baseWS}/ws/connect/${userId}`)
  
  ws.onopen = (e) => {
    setSocket(ws);
    setFailConnection(false)
    console.log('Соединение установлено')
  }
  ws.onclose = (e) => {
    if (e.wasClean) {
      ws = null
      setFailConnection(false)
      console.log('Соединение завершено')
    } else {
      ws = null
      setFailConnection(true)
      setTimeout(() => createSocket(setSocket, userId, setFailConnection), 1000)
    }
  }
}
