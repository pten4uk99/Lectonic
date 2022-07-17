import {reverse} from '../../../../ProjectConstants'

export function checkWorkroomPermissions(permissions, navigate) {
    if (!permissions.is_lecturer && !permissions.is_customer) {
      navigate(reverse('add_role'))
    }
  }