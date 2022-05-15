let initialState = {
  chosenDates: [],
}

export default function lectureDetail(state=initialState, action) {
  switch (action.type) {
    case "UPDATE_LECTURE_DETAIL_CHOSEN_DATES":
      return {...state, chosenDates: action.payload}
    default:
      return state
  }
}