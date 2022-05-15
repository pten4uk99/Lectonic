const initialState = {
  modalActive: false,
  profileDropDownActive: false,
  chatDropdownActive: false,
  errorMessage: '',
  selectedChatId: null
}

export default function header(state=initialState, action) {
  switch (action.type) {
    case "ACTIVATE_MODAL":
      return {...state, modalActive: true}    
    case "DEACTIVATE_MODAL":
      return {...state, modalActive: false}    
    case "SET_PROFILE_DROPDOWN":
      return {...state, profileDropDownActive: action.payload.active, chatDropdownActive: false}       
    case "SET_CHAT_DROPDOWN":
      return {...state, profileDropDownActive: false, chatDropdownActive: action.payload.active}    
    case "SET_ERROR_MESSAGE":
      return {...state, errorMessage: action.payload.message}    
    case "SET_SELECTED_CHAT_ID":
      return {...state, selectedChatId: action.payload}
    default:
      return state
  }
}