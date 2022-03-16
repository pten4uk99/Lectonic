const initialState = []

export default function dateDetail(state = initialState, action) {
  switch (action.type) {
    case "UPDATE_EVENTS":
      let newEvents = action.payload
      for (let date of newEvents) {
        date.date = new Date(date.date)
      }
      console.log(newEvents)
      return newEvents
    default:
      return state
  }
}
