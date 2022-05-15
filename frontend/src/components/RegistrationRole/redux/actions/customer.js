export function SwapIsCompany(is_company) {
  return {type: "SWAP_IS_COMPANY", payload: {is_company: is_company}}
}
export function UpdateCustomerType(type) {
  return {type: "UPDATE_CUSTOMER_TYPE", payload: {type: type}}
}
export function UpdateCustomerHallAddress(address) {
  return {type: "UPDATE_CUSTOMER_HALL_ADDRESS", payload: {address: address}}
}
export function UpdateCustomerEquipment(equipment) {
  return {type: "UPDATE_CUSTOMER_EQUIPMENT", payload: {equipment: equipment}}
}
export function UpdateCompanyName(name) {
  return {type: "UPDATE_COMPANY_NAME", payload: name}
}
export function UpdateCompanyDescription(description) {
  return {type: "UPDATE_COMPANY_DESCRIPTION", payload: description}
}
export function UpdateCompanySite(site) {
  return {type: "UPDATE_COMPANY_SITE", payload: site}
}
