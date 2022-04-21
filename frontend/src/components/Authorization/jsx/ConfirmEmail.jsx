import React, {useEffect} from 'react'

import { useSearchParams, useNavigate } from 'react-router-dom'
import { baseURL } from '~/ProjectConstants'
import {reverse} from "../../../ProjectConstants";


export default function ConfirmEmail() {
  const navigate = useNavigate()
  
  const [searchParams, setSearchParams] = useSearchParams()
  const emailToken = searchParams.get('key')
  
  useEffect(() => {
    fetch(`${baseURL}/api/email/email_confirmation?key=${emailToken}`, {
      method: 'GET', 
      credentials: 'include',
    })
      .then(response => response.json())
      .then(data => {
        if (data.status === 'error') navigate(reverse('404')) 
        else if (data.status === 'confirmed') {
          navigate(reverse('continue_signup'), {state: data.data[0].email})
        }
      })
      .catch(error => console.log('ERROR: ', error))
  }, [])

  return (
    <>
    </>
  )
}
