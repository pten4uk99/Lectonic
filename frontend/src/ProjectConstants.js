export const baseURL = 'http://127.0.0.1:8000'; // случайно могу иногда забыть поменять на dev.lectonic.ru
const [protocol, host] = baseURL.split('//')
export const baseWS = (protocol === 'https' ? 'wss://' : 'ws://') + host

const routes = {
  'index': '/',
  'verify_email': '/verify_email',
  'confirm_email': '/confirm_email',
  'continue_signup': '/continue_registration',
  
  'create_profile': '/create_profile',
  'set_profile': '/set_profile_info',
  
  'add_role': '/add_role',
  'create_lecturer': '/add_role/lecturer',
  'create_customer': '/add_role/customer',
  
  'workroom': '/workroom',
  
  'create_event': '/create_event',
  'change_password': '/change_password',

  'role_page': '/role_page',
  'lecture': '/lecture',
  
  '404': '/404',
} // сюда прописываем все роуты и их имена (имя: роут)

export function reverse(name, params=null) {
  let query = null
  
  if (params) {
    query = '?'
    for (let param in params) {
      query += `${param}=${params[param]}&`
    }
  }
  return query ? routes[name] + query : routes[name]
}

export function reverseEqual(name, pathname) {
  return pathname === reverse(name) || pathname === reverse(name) + '/'
}


export const withoutPermissionsList = [
  reverse('index'),
  reverse('confirm_email'),
  reverse('continue_signup'),
  reverse('verify_email'),
  reverse('change_password'),
  
  '*', // звездочка должна быть последней
]

export function getLecturePhoto(svgId) {
  let svgArr = [
    '/assets/img/default_lecture_photo/1.svg',
    '/assets/img/default_lecture_photo/2.svg',
    '/assets/img/default_lecture_photo/3.svg',
    '/assets/img/default_lecture_photo/4.svg',
    '/assets/img/default_lecture_photo/5.svg',
    '/assets/img/default_lecture_photo/6.svg',
    '/assets/img/default_lecture_photo/7.svg',
    '/assets/img/default_lecture_photo/8.svg',
    '/assets/img/default_lecture_photo/9.svg',
    '/assets/img/default_lecture_photo/10.svg',
  ]
  return svgArr[svgId - 1]
}