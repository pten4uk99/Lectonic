export const baseURL = 'https://dev.lectonic.ru';

export const permissions = {
  isAuthenticated: 'logged_in',
  isPerson: 'is_person'
}

const routes = {
  'index': '/',
  'verify_email': '/verify_email',
  'confirm_email': '/confirm_email',
  'continue_signup': '/continue_registration',
  
  'create_profile': '/create_profile',
  
  'add_role': '/add_role/*',
  'create_lecturer': '/add_role/lecturer',
  
  'workroom': '/workroom',
  
  'create_event': '/create_event',
  'change_password': '/change_password',
}

export function reverse(name) {
  return routes[name]
}