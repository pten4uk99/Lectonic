const initialState = []

export default function notifications(state=initialState, action) {
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
    case "SET_NEED_READ":
      let newNeedReadObj = [...state]
      newNeedReadObj.map((elem) => {
        if (elem.id === action.payload.id) elem.need_read = action.payload.need_read
        return elem
      })
      return newNeedReadObj
    default:
      return state
  }
}