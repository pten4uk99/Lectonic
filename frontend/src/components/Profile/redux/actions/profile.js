export function SwapToLecturer() {
  return {type: "SWAP_TO_LECTURER"}
}
export function SwapToCustomer() {
  return {type: "SWAP_TO_CUSTOMER"}
}
export function UpdateProfile(data) {
  return {type: "UPDATE_PROFILE", payload: data}
}
export function UpdateBirthDate(data) {
  return {type: "UPDATE_BIRTH_DATE", payload: data}
}