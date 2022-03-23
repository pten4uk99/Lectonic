const initialState = {
  isCompany: undefined,
  hall_address: '',
  equipment: ''
}

export default function customer(state=initialState, action) {
  switch (action.type) {
    case "SWAP_IS_COMPANY":
      return {...state, isCompany: action.payload.is_company}
    default:
      return state
  }
}