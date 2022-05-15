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
    case "READ_MESSAGES":
      let newMessages = state.messages.map((elem) => {
        elem.need_read = false
        return elem
      })
      return {...state, messages: newMessages}    
    case "SET_MESSAGES_CONFIRMED":
      return {...state, confirmed: action.payload}
    default:
      return state
  }
}