export function checkNeedSwapToPrevMonth(touchedDate, currentDate, today) {
  if (touchedDate - today <= - 1000 * 60 * 60 * 24) return false
  return touchedDate - currentDate <= - 1000 * 60 * 60 * 24
}

export function checkNeedSwapToNextMonth(touchedDate, currentDate, today) {
  if (touchedDate.getFullYear() >= currentDate.getFullYear() &&
    touchedDate.getMonth() > currentDate.getMonth()) {
    
    if (touchedDate.getFullYear() === today.getFullYear() + 1) {
      if (currentDate.getFullYear() === today.getFullYear()) return true
      return touchedDate.getMonth() <= today.getMonth()
    } else return true
  }
  return touchedDate.getFullYear() > currentDate.getFullYear();
}

export function checkEqualDates(date1, date2) {
  if (date1 && date2) {
    return (
      date1.getFullYear() === date2.getFullYear() &&
      date1.getMonth() === date2.getMonth() &&
      date1.getDate() === date2.getDate()
    )
  } else return false
}
