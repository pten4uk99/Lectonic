import {baseURL} from "~/ProjectConstants";


const body = JSON.stringify({
  email: "pten4ik99@yande.ru",
  password: "12345678"
})

const HEADERS = {
  'Content-Type': 'application/json',
}


export function getLecturerDetail(id) {
  const options = {
    method: 'GET',
    headers: HEADERS,
    credentials: 'include',
  }
  return fetch(
    `${baseURL}/api/workrooms/lecturer/?id=${id}`,
    options
  )
}