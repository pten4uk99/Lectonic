import {DateTime} from "luxon";


export function getDaysArr(year, month) {
  let arr = []
  let date = DateTime.local(Number(year), Number(month)).daysInMonth
  
  for (let i = 1; i <= date; i++) {
    arr.push(i)
  }
  return arr
}

export function getMonthsArr() {
  return [
    'Января',
    'Февраля',
    'Марта',
    'Апреля',
    'Мая',
    'Июня',
    'Июля',
    'Августа',
    'Сентября',
    'Октября',
    'Ноября',
    'Декабря',
  ]
}

export function getYearsArr() {
  let currentYear = DateTime.now().year
  let arr = []
  
  for (let i = currentYear - 1; i > currentYear - 100; i--) {
    arr.push(i)
  }
  return arr
}