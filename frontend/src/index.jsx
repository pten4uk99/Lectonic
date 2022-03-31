import React from 'react'
import ReactDOM from 'react-dom'
import { BrowserRouter } from 'react-router-dom'
import { combineReducers, createStore } from 'redux'
import { Provider } from 'react-redux'
import reportWebVitals from './reportWebVitals'
import App from '~/App'
import calendar from '~/components/WorkRooms/FullCalendar/Calendar/redux/reducers/calendar'
import dateDetail from '~/components/WorkRooms/FullCalendar/DateDetail/redux/reducers/dateDetail'
import '~/index.styl'
import header from "~@/Layout/redux/reducers/header";
import profile from "~@/Profile/redux/reducers/profile";
import event from "~@/WorkRooms/CreateEvent/redux/reducers/event";
import permissions from "~@/Authorization/redux/reducers/permissions";
import addRole from "~@/RegistrationRole/redux/reducers/index"
import dropdown from "~@/Utils/redux/reducers/dropdown" 
import chatSocket from "~@/Authorization/redux/reducers/chatSocket"

console.clear()

let reducer = combineReducers({
  permissions,
  addRole: addRole,
  chatSocket,
  header,
  event,
  profile,
  calendar,
  dateDetail,
  dropdown,
})

const store = createStore(
  reducer,
  window.__REDUX_DEVTOOLS_EXTENSION__ && window.__REDUX_DEVTOOLS_EXTENSION__()
)

ReactDOM.render(
  <React.StrictMode>
    <BrowserRouter>
      <Provider store={store}>
        <App />
      </Provider>
    </BrowserRouter>
  </React.StrictMode>,
  document.getElementById('root')
)

// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
reportWebVitals()
