import {baseURL} from "~/ProjectConstants";

export function login(signInData) {
  const options = {
    method: 'POST', 
    headers: {
      'Content-Type': 'application/json',
    },
    credentials: 'include', 
    body: JSON.stringify(signInData),
  }
  return fetch(`${baseURL}/api/auth/login/`, options)
}

export function emailConfirmation(email, reset_password='') {
  const options = {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(email),
      credentials: 'include',
    }
  return fetch(`${baseURL}/api/email/email_confirmation/?reset_password=${reset_password}`, options)
}

export function signUp(signUpData, reset) {
  const options = {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(signUpData),
      credentials: 'include',
    }
    if (reset) options.method = 'PATCH'
  return fetch(`${baseURL}/api/auth/signup/`, options)
}

