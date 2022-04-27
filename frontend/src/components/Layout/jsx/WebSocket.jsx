import React from "react";
import {connect} from "react-redux";

import {useEffect} from "react";
import {createSocket} from "../../../webSocket";
import {getNotificationsList} from "../ajax";
import {SetNotifyConn, SetNotifyConnFail} from "../redux/actions/ws";
import {SetNeedRead, UpdateNotifications} from "../redux/actions/notifications";


function WebSocket(props) {
  let permissions = props.store.permissions
  let isCustomer = permissions.is_customer
  let isLecturer = permissions.is_lecturer
  let userId = permissions.user_id
  let selectedChatId = props.store.header.selectedChatId
  
  useEffect(() => {
    if (userId && (permissions.is_lecturer || permissions.is_customer)) {
      createSocket(props.setSocket, userId, props.SetNotifyConnFail)
    }
  }, [permissions])
  
  useEffect(() => {
    props.SetNotifyConn(Boolean(props.socket))
    let chatId = props.store.header.selectedChatId
    let eventFunction = (e) => {
      let data = JSON.parse(e.data)
      if (data.type === 'new_respondent') props.AddNotifications(data)
      if (data.type === 'remove_respondent') props.RemoveNotification(data.id)
      if (data.type === 'chat_message') {
        if (chatId !== data.chat_id) props.SetNeedRead(data.chat_id, true)
      }
      if (data.type === 'read_reject_chat') {
        if (data.response === 'deleted') chatSocket.close()
      }
    }
    props.socket?.addEventListener('message', eventFunction)
    return () => props.socket?.removeEventListener('message', eventFunction)
  }, [props.socket, selectedChatId])
  
  useEffect(() => {
    if ((isLecturer || isCustomer) && !props.store.ws.notifyConnFail && permissions.logged_in) {
      getNotificationsList()
        .then(r => r.json())
        .then(data => {
          if (data.status === 'success') props.UpdateNotifications(data.data)
        })
        .catch(e => {})
    }
  }, [isLecturer, isCustomer])
  
  return <></>
}

export default connect(
  state => ({store: state}),
  dispatch => ({
    SetNotifyConnFail: (connected) => dispatch(SetNotifyConnFail(connected)),
    SetNotifyConn: (connected) => dispatch(SetNotifyConn(connected)),
    SetNeedRead: (chat_id, need_read) => dispatch(SetNeedRead(chat_id, need_read)),
    UpdateNotifications: (data) => dispatch(UpdateNotifications(data)),
  })
)(WebSocket)