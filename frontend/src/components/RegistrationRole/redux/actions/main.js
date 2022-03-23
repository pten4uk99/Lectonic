export function SwapAddRoleStep(step) {
  return {type: "SWAP_ADD_ROLE_STEP", payload: {step: step}}
}
export function SwapChooseRoleVisible(visible) {
  return {type: "SET_CHOOSE_ROLE_VISIBLE", payload: {visible: visible}}
}