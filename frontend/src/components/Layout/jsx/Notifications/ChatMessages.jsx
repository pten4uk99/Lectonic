import React, {useEffect, useRef, useState} from 'react'
import {connect} from 'react-redux'

import backArrow from '~/assets/img/back-arrow.svg'
import sendMessage from '~/assets/img/send-message-icon.svg'
import {AddMessage, ReadMessages, SetMessagesConfirmed} from '../../redux/actions/messages'
import {ActivateModal, DeactivateModal, SetSelectedChat} from '../../redux/actions/header'
import {
  cancelResponseOnLecture,
  confirmResponseOnLecture,
  rejectResponseOnLecture
} from '../../../WorkRooms/WorkRoom/ajax/workRooms'
import {RemoveNotification, SetConfirmNotification} from '../../redux/actions/notifications'
import Loader from '~@/Utils/jsx/Loader'
import {SetChatConn} from '../../redux/actions/ws'
import ConfirmAction from '../../../Utils/jsx/ConfirmAction'
import {getMonth} from '../../../WorkRooms/CreateEvent/jsx/CalendarModal'
import {useNavigate} from 'react-router-dom'
import {reverse} from '../../../../ProjectConstants'


function ChatMessages(props) {
  let navigate = useNavigate()
  let data = props.store.messages
  let selectedChatId = props.store.header.selectedChatId
  let messages = data.messages
  let onlineUsers = props.store.ws.onlineUsers
  let messagesBlock = useRef()
  let input = useRef()

  let [rejectRespondent, setRejectRespondent] = useState(null)

  useEffect(() => {
    if (messagesBlock && props.isLoaded) messagesBlock.current.scrollTop = messagesBlock.current.scrollHeight
  }, [messagesBlock?.current?.scrollHeight, props.isLoaded])

  useEffect(() => {
    let eventFunction = (e) => {
      let data = JSON.parse(e.data)
      if (data.type === 'chat_message') {
        if (data?.text) props.AddMessage(data)
        if (data.confirm !== null && data.confirm !== undefined) props.SetMessagesConfirmed(data.confirm)
        if (data.author !== props.store.permissions.user_id) props.ReadMessages()
      } else if (data.type === 'read_messages') props.ReadMessages()
    }
    props.socket?.addEventListener('message', eventFunction)
    return () => props.socket.removeEventListener('message', eventFunction)
  }, [props.socket])

  function handleArrowClick(params) {
    if ((data.confirm !== null && !data.confirm && !data.is_creator) || params.cancel_response) {
      props.socket.send(JSON.stringify({
        'type': 'read_reject_chat',
        'chat_id': props.store.header.selectedChatId
      }))
    }
    props.setArea(false)
    props.SetSelectedChat(null)
  }

  function handleSendMessage(e) {
    if (e.keyCode === 13 && e.target.value === '\n') e.target.value = ''
    if (e.keyCode === 13 && e.target.value) {
      let message = {
        'type': 'chat_message',
        'author': props.store.permissions.user_id,
        'text': e.target.value,
        'chat_id': selectedChatId
      }
      props.socket.send(JSON.stringify(message))
      e.target.value = ''
    }
  }

  function handleClickIcon() {
    if (input.current.value) {
      let message = {
        'type': 'chat_message',
        'author': props.store.permissions.user_id,
        'text': input.current.value,
        'chat_id': selectedChatId
      }
      props.socket.send(JSON.stringify(message))
      input.current.value = ''
    }
  }

  function handleTextareaSize(e) {
    if (e.target.clientHeight >= 112 && e.keyCode !== 8) return
    e.target.style.height = 'auto'
    let height = e.target.scrollHeight
    e.target.style.height = height + 'px'
  }

  function handleConfirmAction(e) {
    if (rejectRespondent) {
      rejectResponseOnLecture(data.lecture_id, data.talker_respondent, selectedChatId)
        .then(r => r.json())
        .then(data => {
          if (data.status === 'success') {
            props.DeactivateModal()
            props.setArea(false)
            props.SetSelectedChat(null)
            props.SetConfirmNotification(selectedChatId, false)
          }
        })
        .catch(() => {
          e.target.innerText = 'Ошибка...'
          setTimeout(() => e.target.innerText = 'Подтвердить', 2000)
        })
    } else {
      confirmResponseOnLecture(data.lecture_id, data.talker_respondent, selectedChatId)
        .then(r => r.json())
        .then(data => {
          if (data.status === 'success') {
            props.DeactivateModal()
          }
        })
        .catch(() => {
          e.target.innerText = 'Ошибка...'
          setTimeout(() => e.target.innerText = 'Подтвердить', 2000)
        })
    }
  }

  function handleToggleConfirm(reject) {
    setRejectRespondent(reject)
    props.ActivateModal()
  }

  function handleRejectResponse() {
    cancelResponseOnLecture(data.lecture_id)
      .then(r => r.json())
      .then(data => {
        if (data.status === 'success') {
          handleArrowClick({cancel_response: true})
          props.RemoveNotification(props.store.header.selectedChatId)
        }
      })
  }

  function handleClickRespondent() {
    let to
    if (data.creator_is_lecturer) {
      if (data.is_creator) to = 'customer'
      else to = 'lecturer'
    } else {
      if (data.is_creator) to = 'lecturer'
      else to = 'customer'
    }
    navigate(reverse('role_page', {[to]: data.talker_respondent}))
  }

  if (!props.isLoaded) return <Loader size={60} top="50%" left="50%" tX="-50%" tY="-50%"/>
  return (
    <>

      {selectedChatId && rejectRespondent !== null && (rejectRespondent ?
        <ConfirmAction text="Вы уверены, что хотите отклонить запрос на лекцию? 
        Данный пользователь больше не сможет откликнуться на выбранную дату."
                       onConfirm={(e) => handleConfirmAction(e)}
                       onCancel={() => setRejectRespondent(null)}/> :
        <ConfirmAction onCancel={() => setRejectRespondent(null)} onConfirm={handleConfirmAction}>
          <div className="confirm-dates__header">Подтверждение лекции</div>
          <div className="confirm-dates__underline"/>
          <div className="confirm-dates__block">
            {data.response_dates.map((elem, index) => {
              let dateStart = new Date(elem[0])
              let dateEnd = new Date(elem[1])
              return <div className="confirm-date" key={index}>
                <div className="calendar-modal__date ml-8">
                  {dateStart.getDate()} {getMonth(dateStart.getMonth())}
                </div>
                <span className="time">
                  {dateStart.getUTCHours().toString().padStart(2, '0')}:
                  {dateStart.getUTCMinutes().toString().padStart(2, '0')}-
                  {dateEnd.getUTCHours().toString().padStart(2, '0')}:
                  {dateEnd.getUTCMinutes().toString().padStart(2, '0')}
                </span>
              </div>
            })}
          </div>
        </ConfirmAction>)
      }

      <div className="chat-messages__block">
        <div className="actions__block">
          <div className="lecture">
            <div className="back-arrow" onClick={handleArrowClick}>
              <img src={backArrow} alt="назад"/>
            </div>
            <div className="text">
              <p className='lecture-name'
                 onClick={() => navigate(reverse('lecture', {id: data.lecture_id}))}>{data.lecture_name}</p>
              <p className='respondent-name' onClick={handleClickRespondent}>
                {data.talker_first_name} {data.talker_last_name}
                {onlineUsers.includes(data.talker_respondent) ?
                  <span className='is-online'>В сети</span> : <span className='is-offline'>Не в сети</span>}
              </p>
            </div>
          </div>
          <div className="buttons">
            {data.confirm === null ?
              data.is_creator ?
                <>
                  <button className="confirm" onClick={() => handleToggleConfirm(false)}>Принять</button>
                  <button className="reject" onClick={() => handleToggleConfirm(true)}>Отклонить</button>
                </> :
                <button className="reject-response" onClick={handleRejectResponse}>Отменить отклик</button> :
              data.confirm ?
                <div className="lecture-confirmed">Лекция подтверждена</div> :
                <div className="lecture-rejected">Лекция отклонена</div>
            }

          </div>
        </div>

        <div className="messages__block" ref={messagesBlock}>
          {messages && messages.length > 0 && messages.map((elem, index) => {
            if (elem.system_text && data.confirm !== false) return <div key={index} className="block-message">
              <div className="system-message">{elem.system_text}</div>
            </div>
            else if (elem.system_text && data.confirm === false) return <div key={index} className="block-message">
              <div className="reject-message">{elem.system_text}</div>
            </div>
            else return <div key={index} className="block-message">
                {props.store.permissions.user_id === elem.author ?
                  <div className="self-message">{elem.text} {elem.need_read && <div className="need-read"/>}</div> :
                  <div className="other-message">{elem.text}</div>}
              </div>
          })}
        </div>

        <div className="input__block">
          <textarea placeholder='Введите текст'
                    onKeyUp={(e) => handleSendMessage(e)}
                    onKeyDown={(e) => handleTextareaSize(e)}
                    rows={1}
                    disabled={data?.confirm != null && !data.confirm}
                    ref={input}/>
          <img src={sendMessage}
               alt="отправить"
               onClick={handleClickIcon}/>
        </div>
      </div>
    </>
  )
}


export default connect(
  state => ({store: state}),
  dispatch => ({
    AddMessage: (message) => dispatch(AddMessage(message)),
    ReadMessages: () => dispatch(ReadMessages()),
    SetConfirmNotification: (chat_id, confirm) => dispatch(SetConfirmNotification(chat_id, confirm)),
    ActivateModal: () => dispatch(ActivateModal()),
    DeactivateModal: () => dispatch(DeactivateModal()),
    SetChatConn: (connected) => dispatch(SetChatConn(connected)),
    RemoveNotification: (chat_id) => dispatch(RemoveNotification(chat_id)),
    SetSelectedChat: (chat_id) => dispatch(SetSelectedChat(chat_id)),
    SetMessagesConfirmed: (confirmed) => dispatch(SetMessagesConfirmed(confirmed)),
  })
)(ChatMessages)