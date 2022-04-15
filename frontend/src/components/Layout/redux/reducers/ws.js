const initialState = {
  chatConn: false,
  notifyConn: false,
  notifyConnFail: false,
}

export default function ws(state=initialState, action) {
  switch (action.type) {
    case "SET_NOTIFY_CONN":
      return {...state, notifyConn: action.payload}      
    case "SET_NOTIFY_CONN_FAIL":
      return {...state, notifyConnFail: action.payload}    
    case "SET_CHAT_CONN":
      return {...state, chatConn: action.payload}
    default:
      return state
  }
}