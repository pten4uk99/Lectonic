const initialState = {
  step: 1,
  chooseRoleVisible: true
}

export function main(state=initialState, action) {
  switch (action.type) {
    case "SWAP_ADD_ROLE_STEP":
      return {...state, step: action.payload.step} 
    case "SET_CHOOSE_ROLE_VISIBLE":
      return {...state, chooseRoleVisible: action.payload.visible}
    default:
      return state
  }
}