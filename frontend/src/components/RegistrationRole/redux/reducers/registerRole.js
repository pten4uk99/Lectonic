const initialState = {
  step: 1,
  performances_links: [],
  publication_links: [],
  diploma_photos: [],
  passport_photo: '',
  selfie_photo: '',
  education: '',
  hall_address: '',
  equipment: ''
}

export default function registerRole(state=initialState, action) {
  switch (action.type) {
    case "SWAP_STEP":
      return {...state, step: action.payload.step}  
    case "UPDATE_PERF_LINKS":
      let newPerfObj = {...state}
      newPerfObj.performances_links[action.payload.index] = action.payload.link
      return newPerfObj
    case "UPDATE_PUB_LINKS":
      let newPubObj = {...state}
      newPubObj.publication_links[action.payload.index] = action.payload.link
      return newPubObj
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