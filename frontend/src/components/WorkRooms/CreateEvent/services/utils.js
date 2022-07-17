export function checkRequiredFields(obj, props) {
  console.log(obj)
  if ((props.store.event.domain.length < 1)) return true

  for (let field in obj) {
    if (!obj[field]) return true
  }
  return false
}

export function onlyNumber(e, maxLength) {
  if (isNaN(Number(e.target.value)) || e.target.value.length > maxLength) {
    e.target.value = e.target.value.slice(0, -1)
  } else if (e.target.value.length === 1 && e.target.value == 0) {
    e.target.value = e.target.value.slice(0, -1)
  }
}

export function addPhotoHandler(inputEvent, UpdatePhoto) {
  let file = inputEvent.target.files[0]
  let reader = new FileReader()
  reader.readAsDataURL(file)

  reader.onload = () => {
    UpdatePhoto(reader.result)
  }
}