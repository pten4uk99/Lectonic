import {baseURL} from "~/ProjectConstants";

export function getCities(name) {
  return fetch(`${baseURL}/api/workrooms/city?name=${name}`, {
    method: 'GET',
    credentials: 'include',
  })
}

export function createProfile(formData) {
  let options = {
    method: 'POST',
    body: formData,
    credentials: 'include',
  }
  return fetch(`${baseURL}/api/workrooms/profile/`, options)
}
