const initialState = {
  isCompany: undefined,
  hall_address: '',
  equipment: ''
}

export default function customer(state=initialState, action) {
  switch (action.type) {
    case "SWAP_IS_COMPANY":
      return {...state, isCompany: action.payload.is_company}
    case "UPDATE_CUSTOMER_HALL_ADDRESS":
      return {...state, hall_address: action.payload.address}   
    case "UPDATE_CUSTOMER_EQUIPMENT":
      return {...state, equipment: action.payload.equipment}
    default:
      return state
  }
}