const initialState = {
  user_id: undefined,
  logged_in: undefined,
  is_person: undefined,
  is_lecturer: undefined,
  is_customer: undefined,
}

export default function permissions(state=initialState, action) {
  switch (action.type) {
    case "SWAP_LOGIN":
      return {...state, logged_in: action.payload.logged}    
    case "SWAP_USER_ID":
      return {...state, user_id: action.payload.user_id}
    case "SWAP_PERSON":
      return {...state, is_person: action.payload.is_person}
    case "SWAP_LECTURER":
      return {...state, is_lecturer: action.payload.is_lecturer}
    case "SWAP_CUSTOMER":
      return {...state, is_customer: action.payload.is_customer}
    
    default:
      return state
  }
}