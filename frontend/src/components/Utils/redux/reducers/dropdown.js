const initialState = {
  id: '',
  timeStart: '',
}
  
export default function dropdown(state=initialState, action) {
  switch (action.type) {
    case "SET_ID_DROPDOWN":
      return {...state, id: action.id}
    case "SET_TIME_START_DROPDOWN":
      return {...state, timeStart: action.payload}
    default:
      return state;
  }
}