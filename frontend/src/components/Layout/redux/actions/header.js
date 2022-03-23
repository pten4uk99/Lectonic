export function ActivateModal() {
  return {type: "ACTIVATE_MODAL"}
}
export function DeactivateModal() {
  return {type: "DEACTIVATE_MODAL"}
}
export function ActiveProfileDropdown(active) {
  return {type: "SET_PROFILE_DROPDOWN", payload: {active: active}}
}