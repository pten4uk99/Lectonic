export function SwapMonthToNext() {
    return {type: "NEXT_MONTH"}
}
export function SwapMonthToPrev() {
    return {type: "PREV_MONTH"}
}
export function SetCheckedDate(date) {
    return {type: "SET_ACTIVE_DATE", payload: {date: date}}
}
export function DeactivateSwap() {
    return {type: "DEACTIVATE_SWAP"}
}
export function DeactivateSwapClass() {
    return {type: "DEACTIVATE_SWAP_CLASS"}
}
export function SetHoverDate(date) {
    return {type: "SET_HOVER_DATE", payload: {date: date}}
}


