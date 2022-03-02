export function ActivateDateDetail(date) {
    return {type: "ACTIVATE", payload: {date: date}}
}
export function DeactivateDateDetail(date) {
    return {type: "DEACTIVATE", payload: {date: date}}
}