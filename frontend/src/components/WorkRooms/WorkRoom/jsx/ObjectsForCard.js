let objectsForCard = [
    // Объект для карточки - Лектора
    {
        name: 'Петров \n Иван Иванович',
        description: 'Лекции: Лидеры-доноры',
        img: '../../../assets/img/Workrooms/WorkroomCard/img_1.png',
        lectorCard: true,
        createLection: false,
        lectionConfirm: false
    },
    // Объект для карточки - Лекции без помещений
    {
        name: 'Лидеры-доноры',
        description: 'Лекции от создателей проекта о донорстве',
        textBtn: 'Откликнуться',
        img: '../../../assets/img/Workrooms/WorkroomCard/img_2.png',
        lectorCard: false,
        createLection: false,
        lectionConfirm: false
    },
    // Объект для карточки - Потенциальные лекции
    {
        name: 'Научные субботы',
        description: 'Лекции от известных учёных о самых актуальных исследованиях',
        textBtn: 'Статус мероприятия',
        img: '../../../assets/img/Workrooms/WorkroomCard/img_3.png',
        lectorCard: false,
        createLection: false,
        lectionConfirm: true,
    },
    // Объект для карточки - Создать лекцию
    {
        name: 'Создать лекцию',
        lectorCard: false,
        createLection: true,
        lectionConfirm: false
    }
];

export default objectsForCard;