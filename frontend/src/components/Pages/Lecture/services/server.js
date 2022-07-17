import {getLectureDetail} from '../ajax/lecture'
import {reverse} from '../../../../ProjectConstants'
import {cancelResponseOnLecture, responseOnLecture} from '../../../WorkRooms/WorkRoom/ajax/workRooms'

export function getLectureData(
  userId, lectureId,
  setIsLoaded, setLectureData,
  setIsCreator, setConfirmedRespondent,
  navigate) {

  getLectureDetail(lectureId)
    .then(response => response.json())
    .then(data => {
      if (data.status === 'success') {
        setIsLoaded(true)
        setLectureData(data.data[0])
        setIsCreator(data.data[0].creator_user_id === userId)
        data.data[0].response_dates.forEach(elem => {
          if (elem.confirmed) setConfirmedRespondent(true)
        })
      } else if (data.status === 'error') navigate(reverse('404'))
    })
    .catch(e => console.log(e))
}

function handleResponseLoaded(responseLoaded, setResponseLoaded) {
  if (!responseLoaded) return false
  setResponseLoaded(false)
}

function formatDates(dates) {
  return dates.map(
    elem => `${elem.getFullYear()}-${elem.getMonth() + 1}-${elem.getDate()}T${elem.getHours()}:${elem.getMinutes()}`)
}

function makeResponse(event, lectureId, dates, setResponseLoaded, navigate) {
  responseOnLecture(lectureId, dates)
    .then(response => response.json())
    .then(data => {
      setResponseLoaded(true)
      if (data.status === 'success') {
        event.target.innerText = 'Отменить отклик'
        navigate(reverse('workroom'))
      }
    })
    .catch(() => event.target.innerText = 'Ошибка...')
}

function makeCancelResponse(
  event, lectureId, setResponseLoaded,
  UpdateLectureDetailChosenDates, RemoveNotification, navigate) {

  cancelResponseOnLecture(lectureId)
    .then(response => response.json())
    .then(data => {
      setResponseLoaded(true)
      if (data.status === 'success') {
        event.target.innerText = 'Откликнуться'
        if (data.data[0]?.type === 'remove_respondent') {
          UpdateLectureDetailChosenDates([])
          RemoveNotification(data.data[0].chat_id)
        }
        navigate(reverse('workroom'))
      }
    })
    .catch(() => event.target.innerText = 'Ошибка...')
}

export function onResponseButtonClick(
  event, lectureId, responseLoaded, setResponseLoaded,
  chosenDates, lectureData, UpdateLectureDetailChosenDates, 
  RemoveNotification, navigate) {

  if (!handleResponseLoaded(responseLoaded, setResponseLoaded)) return
  
  let dates = formatDates(chosenDates)

  if (lectureData) {
    if (lectureData.can_response) {
      makeResponse(event, lectureId, dates, setResponseLoaded, navigate)
    } else {
      makeCancelResponse(
        event, lectureId, setResponseLoaded, 
        UpdateLectureDetailChosenDates, RemoveNotification, navigate)
    }
  }
}