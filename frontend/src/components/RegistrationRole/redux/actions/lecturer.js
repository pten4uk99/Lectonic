export function AddPerfLink(link) {
  return {type: "ADD_PERF_LINK", payload: link}
}
export function AddPubLink(link) {
  return {type: "ADD_PUB_LINK", payload: link}
}
export function UpdateDiplomaPhotos(photo) {
  return {type: "UPDATE_DIPLOMA_PHOTOS", payload: {photo: photo}}
}
export function UpdatePassportPhoto(photo) {
  return {type: "UPDATE_PASSPORT_PHOTO", payload: {photo: photo}}
}
export function UpdateSelfiePhoto(photo) {
  return {type: "UPDATE_SELFIE_PHOTO", payload: {photo: photo}}
}
export function UpdateEducation(education) {
  return {type: "UPDATE_EDUCATION", payload: {education: education}}
}
export function UpdateHallAddress(address) {
  return {type: "UPDATE_HALL_ADDRESS", payload: {address: address}}
}
export function UpdateEquipment(equipment) {
  return {type: "UPDATE_EQUIPMENT", payload: {equipment: equipment}}
}
