import {baseURL} from "~/ProjectConstants";

const HEADERS = {
  'Content-Type': 'application/json',
}

export function getEventsForLecturerMonth(year, month) {
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

export function getEventsForLecturerResponsesMonth(year, month) {
  const options = {
    method: 'GET',
    headers: HEADERS,
    credentials: 'include',
  }
  return fetch(
    `${baseURL}/api/workrooms/calendar/lecturer/responses/?year=${year}&month=${month}`,
    options
  )
}


export function getEventsForCustomerMonth(year, month) {
  const options = {
    method: 'GET',
    headers: HEADERS,
    credentials: 'include',
  }
  return fetch(
    `${baseURL}/api/workrooms/calendar/customer/?year=${year}&month=${month}`,
    options
  )
}

export function getEventsForCustomerResponsesMonth(year, month) {
  const options = {
    method: 'GET',
    headers: HEADERS,
    credentials: 'include',
  }
  return fetch(
    `${baseURL}/api/workrooms/calendar/customer/responses/?year=${year}&month=${month}`,
    options
  )
}
