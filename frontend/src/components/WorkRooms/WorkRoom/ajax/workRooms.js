import {baseURL} from "~/ProjectConstants";

const HEADERS = {
  'Content-Type': 'application/json',
}

export function getProfileInfo() {
  const options = {
    method: 'GET',
    headers: HEADERS,
    credentials: 'include',
  }
  return fetch(
    `${baseURL}/api/workrooms/profile/`,
    options
  )
}


export function getCreatedLecturesForLecturer(id='') {
  const options = {
    method: 'GET',
    headers: HEADERS,
    credentials: 'include',
  }
  return fetch(
    `${baseURL}/api/workrooms/lecture/as_lecturer/?id=${id}`,
    options
  )
}
export function getCreatedLecturesForCustomer(id='') {
  const options = {
    method: 'GET',
    headers: HEADERS,
    credentials: 'include',
  }
  return fetch(
    `${baseURL}/api/workrooms/lecture/as_customer/?id=${id}`,
    options
  )
}

export function deleteLecture(lecture_id) {
  const options = {
    method: 'DELETE',
    headers: HEADERS,
    credentials: 'include',
  }
  return fetch(
    `${baseURL}/api/workrooms/lecture/as_lecturer/?lecture_id=${lecture_id}`,
    options
  )
}

export function getAllLecturesForLecturer() {
  const options = {
    method: 'GET',
    headers: HEADERS,
    credentials: 'include',
  }
  return fetch(
    `${baseURL}/api/workrooms/lecturer/potential_lectures/`,
    options
  )
}

export function getAllLecturesForCustomer() {
  const options = {
    method: 'GET',
    headers: HEADERS,
    credentials: 'include',
  }
  return fetch(
    `${baseURL}/api/workrooms/customer/potential_lectures/`,
    options
  )
}

export function getAllLecturersForCustomer() {
  const options = {
    method: 'GET',
    headers: HEADERS,
    credentials: 'include',
  }
  return fetch(
    `${baseURL}/api/workrooms/customer/lecturers_list/`,
    options
  )
}


export function toggleResponseOnLecture(lecture_id, dates) {
  let datesParam = ''
  if (dates) {
    for (let date of dates) {
      datesParam += `&date=${date}`
    }
  }
  
  const options = {
    method: 'GET',
    headers: HEADERS,
    credentials: 'include',
  }
  return fetch(
    `${baseURL}/api/workrooms/lecture/response/?lecture=${lecture_id}${datesParam}`,
    options
  )
}

export function toggleConfirmResponseOnLecture(lecture_id, respondent_id, chat_id, reject) {
  const options = {
    method: 'GET',
    headers: HEADERS,
    credentials: 'include',
  }
  return fetch(
    `${baseURL}/api/workrooms/lecture/response/confirm/?lecture=${lecture_id}&chat_id=${chat_id}&respondent=${respondent_id}&reject=${reject}`,
    options
  )
}
