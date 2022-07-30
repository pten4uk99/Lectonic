import {DateTime} from "luxon";

let today = DateTime.now()

const initialState = {
  photo: "",
  first_name: "",
  last_name: "",
  middle_name: "",
  is_lecturer: true,
  is_customer: false,
  birth_date: {
    year: today.year - 17,
    month: today.month,
    day: today.day
  }
}

export default function profile(state=initialState, action) {
  switch (action.type) {
    case "UPDATE_PROFILE":
      return {...state, ...action.payload}
    case "SWAP_TO_LECTURER":
      return {
        ...state,
        is_lecturer: true,
        is_customer: false
      }
    case "SWAP_TO_CUSTOMER":
      return {
        ...state,
        is_lecturer: false,
        is_customer: true
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