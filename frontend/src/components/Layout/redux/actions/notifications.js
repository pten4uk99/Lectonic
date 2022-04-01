export function UpdateNotifications(data) {
  return {type: "UPDATE_NOTIFICATIONS", payload: data}
}
export function AddNotifications(data) {
  return {type: "ADD_NOTIFICATIONS", payload: data}
}
export function RemoveNotification(chat_id) {
  return {type: "REMOVE_NOTIFICATION", payload: {id: chat_id}}
}
