const initialState = {
  modalActive: false,
}

export default function header(state=initialState, action) {
  switch (action.type) {
    case "ACTIVATE_MODAL":
      return {...state, modalActive: true}    
    case "DEACTIVATE_MODAL":
      return {...state, modalActive: false}
    default:
      return state
  }
}