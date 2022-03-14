import {baseURL} from "~/ProjectConstants";

const HEADERS = {
  'Content-Type': 'application/json',
}

export function getEventsForMonth(year, month) {
  const options = {
    method: 'GET',
    headers: HEADERS,
    credentials: 'include',
  }
  return fetch(
    `${baseURL}/api/workrooms/calendar/lecturer/?year=${year}&month=${month}`,
    options
  )
}
