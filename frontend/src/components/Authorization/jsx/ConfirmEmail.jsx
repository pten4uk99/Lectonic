import React from 'react'
import { useSearchParams, useNavigate, useParams } from 'react-router-dom'
// import '~/styles/ConfirmEmail.styl'
import { baseURL } from '~/ProjectConstants'

export default function ConfirmEmail() {
  const {title} = useParams();

  console.log('window.location.search: ', window.location.search)
  
 // const navigate = useNavigate()
  // const [confirmationError, setConfirmationError] = useState(false);

  //используем хук из react-router-dom, чтоб вытащить значение ключа query параметра в url
 const [searchParams, setSearchParams] = useSearchParams()
 const emailToken = searchParams.get('key')
 console.log('emailToken: ', emailToken)

  //отправляем запрос GET при загрузке страницы
 /*fetch(`${baseURL}/api/email/email_confirmation/?key=${emailToken}`, {
    method: 'GET',
    credentials: 'include',
  })
    .then(response => {
      console.log('RESPONSE: ', response)
      return response.json()
    })
    .then(data => {
      console.log('data: ', data)
      if (data.status == 'error') {
        //  setConfirmationError(true);
        navigate('/404')
      } else if (data.status == 'success') {
        navigate('/continue_registration')
      }
    })
    .catch(error => {
      console.log('ERROR: ', error)
    })*/

  return (
    <div>
      <h1>
        TestTestTest
      </h1>
      {/* confirmationError &&
                <div>
                    <h3>Произошла ошибка, вернитесь в почту и перейдите по ссылке ещё раз</h3>
                </div> */}
    </div>
  )
}
