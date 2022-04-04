export function UpdateMessages(data) {
  return {type: "UPDATE_MESSAGES", payload: data}
}
export function AddMessage(message) {
  return {type: "ADD_MESSAGE", payload: message}
}