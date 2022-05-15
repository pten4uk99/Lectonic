const initialState = {
  performances_links: [],
  publication_links: [],
  diploma_photos: [],
  education: '',
  hall_address: '',
  equipment: ''
}

export default function lecturer(state=initialState, action) {
  switch (action.type) {
    case "ADD_PERF_LINK":
      return {
        ...state, 
        performances_links: [
          ...state.performances_links, 
          action.payload
        ]
      }
    case "DELETE_PERF_LINK":
      return {
        ...state, 
        performances_links: [
          ...state.performances_links.filter((elem) => action.payload != elem), 
        ]
      }
    case "ADD_PUB_LINK":
      return {
        ...state, 
        publication_links: [
          ...state.publication_links, 
          action.payload
        ]
      }
    case "DELETE_PUB_LINK":
      return {
        ...state, 
        publication_links: [
          ...state.publication_links.filter((elem) => action.payload != elem), 
        ]
      }
    case "UPDATE_DIPLOMA_PHOTOS":
      return {
        ...state, 
        diploma_photos: [
          ...state.diploma_photos, 
          action.payload.photo
        ]
      }
    case "UPDATE_PASSPORT_PHOTO":
      return {...state, passport_photo: action.payload.photo}    
    case "UPDATE_SELFIE_PHOTO":
      return {...state, selfie_photo: action.payload.photo}    
    case "UPDATE_EDUCATION":
      return {...state, education: action.payload.education}
    case "UPDATE_HALL_ADDRESS":
      return {...state, hall_address: action.payload.address}   
    case "UPDATE_EQUIPMENT":
      return {...state, equipment: action.payload.equipment}
      default:
        return state
  }
}