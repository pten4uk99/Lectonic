export function SwapIsCompany(is_company) {
  return {type: "SWAP_IS_COMPANY", payload: {is_company: is_company}}
}
export function UpdateCustomerHallAddress(address) {
  return {type: "UPDATE_CUSTOMER_HALL_ADDRESS", payload: {address: address}}
}
export function UpdateCustomerEquipment(equipment) {
  return {type: "UPDATE_CUSTOMER_EQUIPMENT", payload: {equipment: equipment}}
}
