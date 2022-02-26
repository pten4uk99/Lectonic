let date = new Date()

const initialState = {
  today: date,
  currentDate: date,
  checkedDate: date,
}

export default function calendar(state = initialState, action) {
  switch (action.type) {
    case 'NEXT_MONTH':
      return {
        ...state,
        currentDate: new Date(
          state.currentDate.getFullYear(),
          state.currentDate.getMonth() + 1
        ),
      }
    case 'PREV_MONTH':
      return {
        ...state,
        currentDate: new Date(
          state.currentDate.getFullYear(),
          state.currentDate.getMonth() - 1
        ),
      }
    case 'SET_ACTIVE_DATE':
      return {
        ...state,
        checkedDate: action.payload.date,
      }
    default:
      return state
  }
}
