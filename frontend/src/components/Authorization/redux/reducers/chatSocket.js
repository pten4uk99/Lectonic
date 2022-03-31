const initialState = {
  socket: {}
}

export default function permissions(state=initialState, action) {
  switch (action.type) {
    case "SWAP_SOCKET":
      return {...state, socket: action.payload.socket}
    default:
      return state
  }
}