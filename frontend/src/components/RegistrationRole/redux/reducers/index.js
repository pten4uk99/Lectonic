import {combineReducers} from "redux";
import lecturer from "./lecturer";
import {main} from "./main";
import customer from "./customer";


export default combineReducers({
  main,
  lecturer,
  customer
})