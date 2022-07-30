import {baseURL} from '~/ProjectConstants'

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


export function getConfirmedLectures(obj_name, city='', domain='') {
  const options = {
    method: 'GET',
    headers: HEADERS,
    credentials: 'include',
  }
  return fetch(
    `${baseURL}/api/workrooms/lecture/confirmed_list/?obj_name=${obj_name}&city=${city}&domain=${domain}`,
    options
  )
}

export function getLecturesHistory(query_from, obj_id) {
  const options = {
    method: 'GET',
    headers: HEADERS,
    credentials: 'include',
  }
  return fetch(
    `${baseURL}/api/workrooms/lecture/history_list/?query_from=${query_from}&obj_id=${obj_id}`,
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

export function getAllLecturesForLecturer(city='', domain='') {
  const options = {
    method: 'GET',
    headers: HEADERS,
    credentials: 'include',
  }
  return fetch(
    `${baseURL}/api/workrooms/lecturer/potential_lectures/?city=${city}&domain=${domain}`,
    options
  )
}

export function getAllLecturesForCustomer(city='', domain='') {
  const options = {
    method: 'GET',
    headers: HEADERS,
    credentials: 'include',
  }
  return fetch(
    `${baseURL}/api/workrooms/customer/potential_lectures/?city=${city}&domain=${domain}`,
    options
  )
}

export function getAllCustomersForLecturer(city='', domain='') {
  const options = {
    method: 'GET',
    headers: HEADERS,
    credentials: 'include',
  }
  return fetch(
    `${baseURL}/api/workrooms/lecturer/customers_list/?city=${city}&domain=${domain}`,
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

export function confirmResponseOnLecture(lecture_id, respondent_id, chat_id) {
  const options = {
    method: 'GET',
    headers: HEADERS,
    credentials: 'include',
  }
  return fetch(
    `${baseURL}/api/workrooms/lecture/confirm/?lecture=${lecture_id}&chat_id=${chat_id}&respondent=${respondent_id}`,
    options
  )
}

export function rejectResponseOnLecture(lecture_id, respondent_id, chat_id) {
  const options = {
    method: 'GET',
    headers: HEADERS,
    credentials: 'include',
  }
  return fetch(
    `${baseURL}/api/workrooms/lecture/reject/?lecture=${lecture_id}&chat_id=${chat_id}&respondent=${respondent_id}`,
    options
  )
}
