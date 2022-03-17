const initialState = {
  logged_in: undefined
}

export default function permissions(state=initialState, action) {
  switch (action.type) {
    case "SWAP_LOGIN":
      return {...state, logged_in: action.payload.logged}
    
    default:
      return state
  }
}