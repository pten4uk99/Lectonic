export function SetNotifyConn(connected) {
  return {type: "SET_NOTIFY_CONN", payload: connected}
}
export function SetNotifyConnFail(failed) {
  return {type: "SET_NOTIFY_CONN_FAIL", payload: failed}
}
export function SetChatConn(connected) {
  return {type: "SET_CHAT_CONN", payload: connected}
}
export function SetChatConnFail(failed) {
  return {type: "SET_CHAT_CONN_FAIL", payload: failed}
}
