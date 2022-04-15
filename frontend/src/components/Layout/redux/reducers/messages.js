const initialState = []

export default function messages(state=initialState, action) {
  switch (action.type) {
    case "UPDATE_MESSAGES":
      return {...action.payload}  
    case "ADD_MESSAGE":
      return {
        ...state, 
        messages: [
          ...state.messages, 
          action.payload
        ]
      }
    case "SET_MESSAGES_CONFIRMED":
      return {...state, confirmed: action.payload}
    default:
      return state
  }
}