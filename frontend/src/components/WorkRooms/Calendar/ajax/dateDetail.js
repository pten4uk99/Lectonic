const HEADERS = {
  'Content-Type': 'application/json',
}


export function getEventsForMonth(year, month) {
  const options = {
    method: "GET",
    headers: HEADERS,
    credentials: "include"
  }
  return fetch(
    `http://127.0.0.1:8000/api/workrooms/calendar/lecturer/?year=${year}&month=${month}`,
    options
    )
}