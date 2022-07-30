import {DateTime} from 'luxon'

let today = new Date()

export function getDaysArr(year=today.getFullYear(), month=today.getMonth() + 1) {
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
  
  for (let i = currentYear - 17; i > currentYear - 100; i--) {
    arr.push(i)
  }
  return arr
}