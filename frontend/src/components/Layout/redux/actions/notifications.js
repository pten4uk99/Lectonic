export function UpdateNotifications(data) {
  return {type: "UPDATE_NOTIFICATIONS", payload: data}
}
export function AddNotifications(data) {
  return {type: "ADD_NOTIFICATIONS", payload: data}
}
export function RemoveNotification(chat_id) {
  return {type: "REMOVE_NOTIFICATION", payload: {id: chat_id}}
}
export function SetNeedRead(chat_id, need_read) {
  return {type: "SET_NEED_READ", payload: {id: chat_id, need_read: need_read}}
}
export function SetConfirmNotification(chat_id, confirm) {
  return {type: "SET_CONFIRM_NOTIFICATION", payload: {id: chat_id, confirm: confirm}}
}
