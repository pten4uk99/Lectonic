export function ActivateModal() {
  return {type: "ACTIVATE_MODAL"}
}
export function DeactivateModal() {
  return {type: "DEACTIVATE_MODAL"}
}
export function ActiveProfileDropdown(active) {
  return {type: "SET_PROFILE_DROPDOWN", payload: {active: active}}
}
export function SetErrorMessage(message) {
  return {type: "SET_ERROR_MESSAGE", payload: {message: message}}
}
export function SetSelectedChat(chat_id) {
  return {type: "SET_SELECTED_CHAT_ID", payload: chat_id}
}