import {baseURL} from "~/ProjectConstants";

const HEADERS = {
  'Content-Type': 'application/json',
}

export function createLecturer(formData) {
  const options = {
    method: 'POST',
    headers: HEADERS,
    body: formData,
    credentials: 'include',
  }
  return fetch(
    `${baseURL}/api/workrooms/lecturer/`,
    options
  )
}