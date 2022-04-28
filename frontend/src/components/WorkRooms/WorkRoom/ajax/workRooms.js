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


export function getConfirmedLectures(obj_name) {
  const options = {
    method: 'GET',
    headers: HEADERS,
    credentials: 'include',
  }
  return fetch(
    `${baseURL}/api/workrooms/lecture/confirmed_list/?obj_name=${obj_name}`,
    options
  )
}

export function getLecturesHistory(query_from) {
  const options = {
    method: 'GET',
    headers: HEADERS,
    credentials: 'include',
  }
  return fetch(
    `${baseURL}/api/workrooms/lecture/history_list/?query_from=${query_from}`,
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


export function responseOnLecture(lecture_id, dates) {
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

export function cancelResponseOnLecture(lecture_id) {
  const options = {
    method: 'GET',
    headers: HEADERS,
    credentials: 'include',
  }
  return fetch(
    `${baseURL}/api/workrooms/lecture/cancel_response/?lecture=${lecture_id}`,
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
