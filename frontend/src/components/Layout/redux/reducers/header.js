const initialState = {
  modalActive: false,
  profileDropDownActive: false,
  errorMessage: '',
}

export default function header(state=initialState, action) {
  switch (action.type) {
    case "ACTIVATE_MODAL":
      return {...state, modalActive: true}    
    case "DEACTIVATE_MODAL":
      return {...state, modalActive: false}    
    case "SET_PROFILE_DROPDOWN":
      return {...state, profileDropDownActive: action.payload.active}    
    case "SET_ERROR_MESSAGE":
      return {...state, errorMessage: action.payload.message}
    default:
      return state
  }
}