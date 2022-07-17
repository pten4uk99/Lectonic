const initialState = {
  photo: '',
  domain: [],
  type: 'online',
  place: false,
  equipment: false,
  payment: false
}

export default function event(state=initialState, action) {
  switch (action.type) {
    case 'UPDATE_PHOTO':
      return {...state, photo: action.payload.photo}    
    case 'UPDATE_DOMAIN':
      return {
        ...state, 
        domain: [
           ...state.domain,
           action.payload.domain,
        ]
      }
    case 'CLEAR_DOMAIN':
      return {...state, domain: []}
    case 'DELETE_DOMAIN':
      return {
        ...state, 
        domain: [
          ...state.domain.filter((elem, i) => action.payload.index != i), 
        ]
      }
    case 'SWAP_EVENT_TYPE':
      return {...state, type: action.payload.type}    
    case 'SWAP_PLACE':
      return {...state, place: action.payload.place}
    case 'SWAP_EQUIPMENT':
      return {...state, equipment: action.payload.equipment}
    case 'SWAP_PAYMENT':
      return {...state, payment: action.payload.payment}
        default:
      return state
  }
    
}