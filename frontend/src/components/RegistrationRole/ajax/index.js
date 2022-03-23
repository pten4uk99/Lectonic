import {baseURL} from "~/ProjectConstants";

const HEADERS = {
  'Content-Type': 'application/json',
}

export function uploadDiplomaPhotos(formData) {
  const options = {
    method: 'POST',
    body: formData,
    credentials: 'include',
  }
  return fetch(
    `${baseURL}/api/workrooms/lecturer/diploma_photos/`,
    options
  )
}

export function uploadDocumentPhoto(formData) {
  const options = {
    method: 'POST',
    body: formData,
    credentials: 'include',
  }
  return fetch(
    `${baseURL}/api/workrooms/profile/document_photos/`,
    options
  )
}

export function createLecturer(formData) {
  const options = {
    method: 'POST',
    body: formData,
    credentials: 'include',
  }
  return fetch(
    `${baseURL}/api/workrooms/lecturer/`,
    options
  )
}