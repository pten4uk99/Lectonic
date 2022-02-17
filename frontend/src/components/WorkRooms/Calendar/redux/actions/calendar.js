export function SwapMonthToNext() {
    return {type: "NEXT_MONTH"}
}
export function SwapMonthToPrev() {
    return {type: "PREV_MONTH"}
}
export function SetCheckedDate(date) {
    return {type: "SET_ACTIVE_DATE", payload: {date: date}}
}
