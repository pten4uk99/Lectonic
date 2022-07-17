import {createEvent, editEvent} from '../ajax/event'
import {reverse} from '../../../../ProjectConstants'

function getStrTime(hour, minute, duration) {
  let oldMinutes = hour * 60 + minute
  let newMinutes = oldMinutes + duration
  let newHour = newMinutes / 60
  let newMinute = newMinutes % 60

  if (newHour < 1) return `00:${newMinute}`
  else return `${Math.floor(newHour)}:${newMinute}`
}

function formatDate(date, duration) {
  return `${date.getFullYear()}-${date.getMonth() + 1}-${date.getDate()}T${date.getHours()}:${date.getMinutes()}` +
    ',' +
    `${date.getFullYear()}-${date.getMonth() + 1}-${date.getDate()}T${getStrTime(date.getHours(), date.getMinutes(), duration)}`
}

function setSvgNumber() {
  return String(1 + Math.floor(Math.random() * 10))
}

export function handleCreateEvent(
  e, setResponseLoaded, selectedDomains, chooseDates, eventType, 
  duration, role, navigate, setErrorMessages, lectureData) {
  
  setResponseLoaded(false)
  e.preventDefault()
  let formData = new FormData(e.target)

  selectedDomains.map((elem) => formData.append('domain', elem))
  for (let date of chooseDates) formData.append('datetime', formatDate(date, duration))
  formData.set('type', eventType)
  formData.set('svg', setSvgNumber())

  if (!lectureData) {
    createEvent(formData, role)
      .then(response => response.json())
      .then(data => {
        setResponseLoaded(true)
        if (data.status === 'created') navigate(reverse('workroom'))
        else {
          setErrorMessages({
            name: data?.name,
            datetime: data?.datetime,
            listeners: data?.listeners
          })
        }
      })
      .catch(() => e.target.innerText = 'Ошибка...')
    
  } else {
    formData.set('id', lectureData.id)
    
    editEvent(formData, role)
      .then(r => r.json())
      .then(data => {
        if (data.status === 'success') navigate(reverse('workroom')) 
        else {
          setErrorMessages({
            name: data?.name,
            datetime: data?.datetime,
            listeners: data?.listeners
          })
        }
      })
    .catch(() => e.target.innerText = 'Ошибка...')
  }
}