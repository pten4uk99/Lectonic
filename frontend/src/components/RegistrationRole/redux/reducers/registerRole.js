const initialState = {
  selectedRole: '',
  step: 0,
  performances_links: [],
  publication_links: []
}

export default function registerRole(state=initialState, action) {
  switch (action.type) {
    case "SWAP_SELECTED_ROLE":
      return {...state, selectedRole: action.payload.role}
    case "SWAP_STEP":
      return {...state, step: action.payload.step}  
    case "UPDATE_PERF_LINKS":
      return {
        ...state, 
        performances_links: [
          ...state.performances_links,
          action.payload.link
        ]
      }  
    case "UPDATE_PUB_LINKS":
      return {
        ...state, 
        publication_links: [
          ...state.publication_links,
          action.payload.link
        ]
      }
  default:
    return state
  }
}