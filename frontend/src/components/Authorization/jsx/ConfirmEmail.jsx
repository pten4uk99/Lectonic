import React from 'react'
import { useSearchParams, useNavigate } from 'react-router-dom'
// import '~/styles/ConfirmEmail.styl'
import { baseURL } from '~/ProjectConstants'
import {reverse} from "../../../ProjectConstants";

export default function ConfirmEmail() {
  const navigate = useNavigate()

  //используем хук из react-router-dom, чтоб вытащить значение ключа query параметра в url
 const [searchParams, setSearchParams] = useSearchParams()
 const emailToken = searchParams.get('key')

  //отправляем запрос GET при загрузке страницы
 fetch(`${baseURL}/api/email/email_confirmation?key=${emailToken}`, {
    method: 'GET',
    credentials: 'include',
  })
    .then(response => {
      console.log('RESPONSE: ', response)
      return response.json()
    })
    .then(data => {
      console.log('data: ', data)
      if (data.status === 'error') navigate('/404') 
      else if (data.status === 'confirmed') {
        navigate(reverse('continue_signup'), {state: data.data[0].email})
      }
    })
    .catch(error => {
      console.log('ERROR: ', error)
    })

  return (
    <>
    </>
  )
}
