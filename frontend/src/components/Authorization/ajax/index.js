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

export function emailConfirmation(email) {
  const options = {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(email),
      credentials: 'include',
    }
  return fetch(`${baseURL}/api/email/email_confirmation/`, options)
}

export function signUp(signUpData) {
  const options = {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(signUpData),
      credentials: 'include',
    }
  return fetch(`${baseURL}/api/auth/signup/`, options)
}

