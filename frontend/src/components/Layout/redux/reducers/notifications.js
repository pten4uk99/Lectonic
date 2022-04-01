const initialState = []

export default function header(state=initialState, action) {
  switch (action.type) {
    case "UPDATE_NOTIFICATIONS":
      return [...action.payload]    
    case "ADD_NOTIFICATIONS":
      let newAddObj = [...state]
      newAddObj.map((elem) => {
        if (elem.id === action.payload.id) return state
      })
      return [action.payload, ...state]    
    case "REMOVE_NOTIFICATION":
      let newRemObj = [...state]
      
      newRemObj.forEach((elem, index) => {
        if (elem.id === action.payload.id) newRemObj.splice(index, 1)
      })
      return newRemObj
    default:
      return state
  }
}