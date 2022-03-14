const initialState = {
  photo: "",
  first_name: "Никита",
  last_name: "Павленко",
  middle_name: "Михайлович",
  is_lecturer: true,
  is_customer: false,
  utils: {
    lecturer: true,
    customer: false
  }
}

export default function profile(state=initialState, action) {
  switch (action.type) {
    case "SWAP_TO_LECTURER":
      return {
        ...state,
        utils: {
          lecturer: true, 
          customer: false
        }
      }
    case "SWAP_TO_CUSTOMER":
      return {
        ...state,
        utils: {
          lecturer: false, 
          customer: true
        }
      }
    default:
      return state
  }
}