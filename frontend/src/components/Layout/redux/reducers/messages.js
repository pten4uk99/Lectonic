const initialState = []

export default function messages(state=initialState, action) {
  switch (action.type) {
    case "UPDATE_MESSAGES":
      return [...action.payload]    
    case "ADD_MESSAGE":
      return [...state, action.payload]
    default:
      return state
  }
}