let objectForCard = 
    // Для отображения нужной карточки, теперь в пропс передаем объект со след св-вами, 
    // последнее св-во, передаем нужный флаг, для отрисовки нужной карточки
    {
        src: '../../../assets/img/Workrooms/WorkroomCard/img_1.png',
        name: 'Петров \n Иван Иванович',
        description: 'Лекции: \n Лидеры-доноры',
        date: "20.03.2022 – 25.03.2022",
        city: "г. Санкт-Петербург",
        client: "Заказчик:",
        clientName: "ОАО «Какое-то очень длинное название",
        createLecture: true, // флаг - создать лекцию
        lectorCard: true, // флаг - карточка лектора
        potentialLecture: false, // флаг - потенциальная лекция
        createdLecture: false, // флаг - созданная лекция
        confirmedLecture: true // флаг - подтвержденная лекция
    }
   
export default objectForCard;