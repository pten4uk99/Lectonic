export const baseURL = 'https://dev.lectonic.ru'; // случайно могу иногда забыть поменять на dev.lectonic.ru
const hostURL = baseURL.split('//')[1]
export const baseWS = 'wss://' + hostURL


const routes = {
  'index': '/',
  'verify_email': '/verify_email',
  'confirm_email': '/confirm_email',
  'continue_signup': '/continue_registration',
  
  'create_profile': '/create_profile',
  
  'add_role': '/add_role',
  'create_lecturer': '/add_role/lecturer',
  'create_customer': '/add_role/customer',
  
  'workroom': '/workroom',
  
  'create_event': '/create_event',
  'change_password': '/change_password',

  'role_page': '/role_page',
  'lecture': '/lecture',
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


export const withoutPermissionsList = [
  reverse('index'),
  reverse('confirm_email'),
  reverse('continue_signup'),
  reverse('verify_email'),
  
  '*', // звездочка должна быть последней
]