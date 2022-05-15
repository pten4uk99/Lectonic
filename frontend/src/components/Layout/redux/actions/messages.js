export function UpdateMessages(data) {
  return {type: "UPDATE_MESSAGES", payload: data}
}
export function AddMessage(message) {
  return {type: "ADD_MESSAGE", payload: message}
}
export function ReadMessages() {
  return {type: "READ_MESSAGES"}
}
export function SetMessagesConfirmed(confirmed) {
  return {type: "SET_MESSAGES_CONFIRMED", payload: confirmed}
}
