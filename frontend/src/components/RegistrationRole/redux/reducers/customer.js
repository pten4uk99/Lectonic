const initialState = {
  isCompany: undefined,
  hall_address: '',
  equipment: '',
  company_name: '',
  company_description: '',
  company_site: '',
}

export default function customer(state=initialState, action) {
  switch (action.type) {
    case "SWAP_IS_COMPANY":
      return {...state, isCompany: action.payload.is_company}
    case "UPDATE_CUSTOMER_HALL_ADDRESS":
      return {...state, hall_address: action.payload.address}   
    case "UPDATE_CUSTOMER_EQUIPMENT":
      return {...state, equipment: action.payload.equipment}    
    case "UPDATE_COMPANY_NAME":
      return {...state, company_name: action.payload}    
    case "UPDATE_COMPANY_DESCRIPTION":
      return {...state, company_description: action.payload}    
    case "UPDATE_COMPANY_SITE":
      return {...state, company_site: action.payload}
    default:
      return state
  }
}