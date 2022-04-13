import {baseURL} from "~/ProjectConstants";

const HEADERS = {
  'Content-Type': 'application/json',
}

export function getEventsForLecturerMonth() {
  const options = {
    method: 'GET',
    headers: HEADERS,
    credentials: 'include',
  }
  return fetch(
    `${baseURL}/api/workrooms/calendar/lecturer/`,
    options
  )
}

export function getEventsForLecturerResponsesMonth() {
  const options = {
    method: 'GET',
    headers: HEADERS,
    credentials: 'include',
  }
  return fetch(
    `${baseURL}/api/workrooms/calendar/lecturer/responses/`,
    options
  )
}


export function getEventsForCustomerMonth() {
  const options = {
    method: 'GET',
    headers: HEADERS,
    credentials: 'include',
  }
  return fetch(
    `${baseURL}/api/workrooms/calendar/customer/`,
    options
  )
}

export function getEventsForCustomerResponsesMonth() {
  const options = {
    method: 'GET',
    headers: HEADERS,
    credentials: 'include',
  }
  return fetch(
    `${baseURL}/api/workrooms/calendar/customer/responses/`,
    options
  )
}
