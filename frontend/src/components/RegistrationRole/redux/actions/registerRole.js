export function SwapStep(step) {
  return {type: "SWAP_STEP", payload: {step: step}}
}
export function UpdatePerfLinks(link ,index) {
  return {type: "UPDATE_PERF_LINKS", payload: {link: link, index: index}}
}
export function UpdatePubLinks(link, index) {
  return {type: "UPDATE_PUB_LINKS", payload: {link: link, index: index}}
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
