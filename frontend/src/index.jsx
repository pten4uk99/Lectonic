import React from 'react'
import ReactDOM from 'react-dom'
import { BrowserRouter } from 'react-router-dom'
import { combineReducers, createStore } from 'redux'
import { Provider } from 'react-redux'
import reportWebVitals from './reportWebVitals'
import App from '~/App'
import calendar from '~/components/WorkRooms/Calendar/redux/reducers/calendar'
import dateDetail from '~/components/WorkRooms/DateDetail/redux/reducers/dateDetail'
import '~/index.styl'

console.clear()

let reducer = combineReducers({
  calendar,
  dateDetail,
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
