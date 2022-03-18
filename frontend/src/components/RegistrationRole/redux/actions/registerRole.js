export function SwapSelectedRole(role) {
  return {type: "SWAP_SELECTED_ROLE", payload: {role: role}}
}
export function SwapStep(step) {
  return {type: "SWAP_STEP", payload: {step: step}}
}
export function UpdatePerfLinks(link) {
  return {type: "UPDATE_PERF_LINKS", payload: {link: link}}
}
export function UpdatePubLinks(link) {
  return {type: "UPDATE_PUB_LINKS", payload: {link: link}}
}
