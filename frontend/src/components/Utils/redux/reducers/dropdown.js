const initialState = {
    id: '',
  }
  
  export default function dropdown(state=initialState, action) {
    switch (action.type) {
      case "SET_ID_DROPDOWN":
        return {id : action.id} 
      default:
        return state;
    }
  }