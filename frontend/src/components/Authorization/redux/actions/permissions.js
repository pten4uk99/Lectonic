export function SwapLogin(logged) {
  return {type: "SWAP_LOGIN", payload: {logged: logged}}
}
export function SwapPerson(is_person) {
  return {type: "SWAP_PERSON", payload: {is_person: is_person}}
}
export function SwapLecturer(is_lecturer) {
  return {type: "SWAP_LECTURER", payload: {is_lecturer: is_lecturer}}
}
export function SwapCustomer(is_customer) {
  return {type: "SWAP_CUSTOMER", payload: {is_customer: is_customer}}
}
export function SwapUserId(user_id) {
  return {type: "SWAP_USER_ID", payload: {user_id: user_id}}
}
