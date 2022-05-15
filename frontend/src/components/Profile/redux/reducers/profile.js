import {DateTime} from "luxon";

let today = DateTime.now()

const initialState = {
  photo: "",
  first_name: "",
  last_name: "",
  middle_name: "",
  is_lecturer: true,
  is_customer: false,
  utils: {
    lecturer: true,
    customer: false
  },
  birth_date: {
    year: today.year,
    month: today.month,
    day: today.day
  }
}

export default function profile(state=initialState, action) {
  switch (action.type) {
    case "UPDATE_PROFILE":
      return {
        ...action.payload, 
        utils: {...state.utils}
      }
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
    case "UPDATE_BIRTH_DATE":
      return {
        ...state,
        birth_date: {
          ...state.birth_date,
          ...action.payload
        }
      }
    default:
      return state
  }
}