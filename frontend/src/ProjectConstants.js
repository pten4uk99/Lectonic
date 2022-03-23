export const baseURL = 'https://dev.lectonic.ru'; // случайно могу иногда забыть поменять на dev.lectonic.ru

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
} // сюда прописываем все роуты и их имена (имя: роут)

export function reverse(name) {
  return routes[name]
}


export const withoutPermissionsList = [
  reverse('index'),
  reverse('confirm_email'),
  reverse('continue_signup'),
  reverse('verify_email'),
  
  '*', // звездочка должна быть последней
]