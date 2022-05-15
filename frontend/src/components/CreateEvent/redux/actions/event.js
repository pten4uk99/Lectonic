export function UpdatePhoto(photo) {
  return {type: "UPDATE_PHOTO", payload: {photo: photo}}
}
export function UpdateDomain(domain) {
  return {type: "UPDATE_DOMAIN", payload: {domain: domain}}
}
export function SwapEventType(type) {
  return {type: "SWAP_EVENT_TYPE", payload: {type: type}}
}
export function SwapPlace(place) {
  return {type: "SWAP_PLACE", payload: {place: place}}
}
export function SwapPayment(payment) {
  return {type: "SWAP_PAYMENT", payload: {payment: payment}}
}
