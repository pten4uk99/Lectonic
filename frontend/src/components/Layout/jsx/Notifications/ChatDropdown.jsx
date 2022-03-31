import React, {useState} from "react";
import {connect} from "react-redux";
import ChatMessages from "./ChatMessages";
import NotificationsList from "./NotificationsList";


function ChatDropdown(props) {
  let [messagesArea, setMessagesArea] = useState(false)
  
  return (
    <div className="chat-dropdown__block">
      {!messagesArea ? 
        <NotificationsList socket={props.notificationsSocket} 
                           setArea={setMessagesArea}/> : 
        <ChatMessages setArea={setMessagesArea}/>
      }
    </div>
  )
}


export default connect(
  state => ({store: state}),
  dispatch => ({})
)(ChatDropdown);